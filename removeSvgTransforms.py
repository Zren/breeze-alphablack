#!/usr/bin/python3

import sys, os
from bs4 import BeautifulSoup, NavigableString, Tag
import re
import math

# s = '4.500'
# while len(s) > 2:
# 	if s[-1] == '0':
# 		print(s, s[0:-1])
# 		s = s[0:-1]
# sys.exit(0)

def bringToFront(arr, value):
	try:
		i = arr.index(value)
		arr.insert(0, arr.pop(i))
	except ValueError:
		pass # Not in the list

def bringAllToFront(arr, keys):
	for key in reversed(keys):
		bringToFront(arr, key)

def sortedAttrs(el):
	keys = el.attrs.keys()
	keys = sorted(keys)
	bringAllToFront(keys, [
		"id",
		"class",
		"x",
		"y",
		"width",
		"height",
		"style",
	])
	for key in keys:
		yield key, el.attrs[key]


def dent(indent):
	return "  " * indent

def nl(indent):
	return "\n" + dent(indent)

def renderTag(el, indent=0):
	# s += (" " * indent)
	# print(dent(indent), el.name, type(el))
	if type(el) == Tag or type(el) == BeautifulSoup:
		if el.name == 'metadata':
			return "" # Skip it (it has annoying namespaces and we don't need it anyways)

		s = ""
		s += "<" + el.name
		for key, value in sortedAttrs(el):
			s += nl(indent+1) + " " + str(key) + "=\"" + str(value) + "\""

		childrenStr = ""
		childCount = 0
		for child in el.children:
			childStr = renderTag(child, indent+1)
			if len(childStr) > 0:
				childrenStr += nl(indent+1) + childStr
				childCount += 1

		if childCount == 0:
			s += " /"
		s += ">"

		s += childrenStr
		if childCount > 0:
			s += nl(indent) + "</" + el.name + ">"
		return s
	elif type(el) == NavigableString:
		s = str(el)
		if s.strip() == '':
			return ""
		else:
			# print("LOG", s)
			return s
	else:
		print("ERROR", type(el), el)
		return ""

def renderSvg(svg):
	s = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
	s += renderTag(svg)
	s += '\n'
	return s

def parseArgs(s):
	left = s.index('(') + 1
	right = s.index(')')
	s = s[left:right]
	# print(s)
	tokens = s.split(',')
	args = map(float, tokens)
	args = list(args)
	# print(args)
	return args

def transformChildren(parent, func, *args):
	for el in parent.children:
		if type(el) == Tag:
			# print('\t', el)
			func(el, *args)

def roundIfNeeded(a):
	# return a
	b = round(a)
	if a < b and b <= a + 0.01:
		return b # a ~= 0.99
	elif a - 0.01 <= b and b <= a:
		return b # a ~= 1.01
	else:
		return a

def applyTranslate(el, dx, dy):
	# First check if the el has a tranlsate() that negates (dx,dy).
	transform = el.attrs.get('transform')
	if transform is not None and 'translate(' in transform:
		args = parseArgs(transform)
		dx2, dy2 = args
		if math.isclose(dx, -dx2) and math.isclose(dy, -dy2):
			del el.attrs['transform']
			return

	# If not, shift all coordinates of the el.
	if el.name == 'g':
		transformChildren(el, applyTranslate, dx, dy)
	elif el.name == 'path':
		applyMatrixToPath(el, 1, 0, 0, 1, dx, dy)
	elif el.name == 'rect':
		applyTranslateToRect(el, dx, dy)
	else:
		raise Exception("Cannot applyTranslate to <{}>".format(el.name))

def formatNumber(x):
	if type(x) == float:
		s = str(x)
		a,b = s.split('.')
		if len(b) > 3: # significance >3
			s = "{:.3f}".format(x)
			while s[-1] == '0':
				# print(s, s[0:-1])
				s = s[0:-1]
			return s
		else:
			return s
	else:
		return str(x)

def applyTranslateToRect(el, dx, dy):
	x = float(el["x"])
	y = float(el["y"])

	x += dx
	y += dy
	# print("\t\t({}, {}) => ({}, {})".format(el["x"], el["y"], x, y))
	
	x = formatNumber(roundIfNeeded(x))
	y = formatNumber(roundIfNeeded(y))
	# print("\t\t({}, {}) => ({}, {})".format(el["x"], el["y"], x, y))

	el["x"] = x
	el["y"] = y


def applyMatrix(el, a, b, c, d, e, f):
	if el.name == 'rect':
		applyMatrixToRect(el, a, b, c, d, e, f)
	elif el.name == 'path':
		applyMatrixToPath(el, a, b, c, d, e, f)
	else:
		raise Exception("Cannot applyMatrix to <{}>".format(el.name))

def applyMatrixToRect(el, a, b, c, d, e, f):
	# print("\t{}".format(el.parent['id']))
	x1 = float(el["x"])
	y1 = float(el["y"])
	w1 = float(el["width"])
	h1 = float(el["height"])
	x2 = x1 + w1
	y2 = y1 + h1
	# print("\t\t({}, {}, {}, {})".format(el["x"], el["y"], el["width"], el["height"]))
	
	# https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
	x3, y3 = applyMatrixToPoint(x1, y1, a, b, c, d, e, f)
	x4, y4 = applyMatrixToPoint(x2, y2, a, b, c, d, e, f)
	w2 = x4 - x3
	h2 = y4 - y3
	# print("\t\t\t=> ({}, {}, {}, {})".format(x3, y3, w2, h2))

	if w2 < 0:
		x3 = x4
		# x3 += w2
		w2 *= -1
	if h2 < 0:
		y3 = y4
		# y3 += h2
		h2 *= -1

	x3 = roundIfNeeded(x3)
	y3 = roundIfNeeded(y3)
	w2 = roundIfNeeded(w2)
	h2 = roundIfNeeded(h2)
	# print("\t\t\t=> ({}, {}, {}, {})".format(x3, y3, w2, h2))

	el["x"] = formatNumber(x3)
	el["y"] = formatNumber(y3)
	el["width"] = formatNumber(w2)
	el["height"] = formatNumber(h2)

def applyScaleToRect(el, sx, sy):
	applyMatrixToRect(el, sx, 0, 0, sy, 0, 0)


# def applyMatrixToPoint(x1, y1, a, b, c, d, e, f):
# 	x1 = float(x1)
# 	y1 = float(y1)
	
# 	# https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
# 	x2 = a*x1 + c*y1 + e
# 	y2 = b*x1 + d*y1 + f

# 	x2 = roundIfNeeded(x2)
# 	y2 = roundIfNeeded(y2)

# 	x2 = formatNumber(x2)
# 	y2 = formatNumber(y2)
# 	# print("\t\t({}, {})  => ({}, {})".format(x1, y1, x2, y2))
	
# 	return x2, y2

def applyMatrixToPoint(x1, y1, a, b, c, d, e, f):
	# https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
	x2 = a*x1 + c*y1 + e
	y2 = b*x1 + d*y1 + f
	return x2, y2

def applyMatrixToPath(el, a, b, c, d, e, f):
	# print("\t{}".format(el.parent['id']))
	# print("matrix({}, {}, {}, {}, {}, {})".format(a, b, c, d, e, f))
	path = el['d']
	path = path.replace(',', ' ')
	tokens = path.split(' ')
	out = []
	lastCommand = ''
	command = ''

	tokenIter = iter(tokens)
	commandUseCount = 0
	arcX1 = 0
	arcY1 = 0
	arcX2 = 0
	arcY2 = 0
	for token in tokenIter:
		# print('\t\t' + token)
		
		if token in ['m', 'l', 'h', 'v', 'z', 'c', 's', 'q', 't', 'a']:
			commandUseCount = 0
			lastCommand = command
			command = token
			if command == 'z': # Close Path
				out.append('z')
			continue

		commandUseCount += 1
		if command == 'm' or command == 'l':
			# Move To x,y
			# Line to x,y
			x = token
			y = next(tokenIter)
			x1 = float(x)
			y1 = float(y)

			if commandUseCount == 1:
				# Remember original x,y positions
				arcX1 = x1
				arcY1 = y1
			elif commandUseCount >= 2:
				# x,y is delta dx,dy
				x1 = arcX1 + x1
				y1 = arcY1 + y1
				arcX1 = x1
				arcY1 = y1

			x2, y2 = applyMatrixToPoint(x1, y1, a, b, c, d, e, f)

			if commandUseCount == 1:
				# Remember matrixed x,y positions
				arcX2 = x2
				arcY2 = y2
				x2 = formatNumber(roundIfNeeded(x2))
				y2 = formatNumber(roundIfNeeded(y2))
				commandStr = "{} {},{}".format(command, x2, y2)
			elif commandUseCount >= 2:
				# Generate matrixed delta dx,dy
				dx = x2 - arcX2
				dy = y2 - arcY2
				dx = formatNumber(roundIfNeeded(dx))
				dy = formatNumber(roundIfNeeded(dy))
				arcX2 = x2
				arcY2 = y2
				commandStr = "{},{}".format(dx, dy)
			# print("\t\t[{}] ({},{}) => ({})".format(command, x, y, commandStr))
			out.append(commandStr)
		elif command == 'h': # Horizontal to x
			raise Exception("Implement path h/v")
		elif command == 'v': # Vertical to y
			raise Exception("Implement path h/v")
		elif command == 'z': # Close Path
			raise Exception('Close Path does not use arguments')
		elif command == 'c': # Cubic Bezier curve to
			# C x1 y1, x2 y2, x y
			raise Exception("Implement path Bezier Curves")
		elif command == 's': # Continue Cubic Bezier curve
			# S x2 y2, x y
			raise Exception("Implement path Bezier Curves")
		elif command == 'q': # Quadratic Bezier curve
			# Q x1 y1, x y
			raise Exception("Implement path Bezier Curves")
		elif command == 't': # Continue Quadratic Bezier curve
			# T x y
			raise Exception("Implement path Bezier Curves")
		elif command == 'a': # Arc to
			# A rx ry x-axis-rotation large-arc-flag sweep-flag x y
			# a 4.5,4.5 0 0 0 -4.5,4.5
			rx = token
			ry = next(tokenIter)
			xAxisRotation = next(tokenIter)
			largeArcFlag = next(tokenIter)
			sweepFlag = next(tokenIter)
			x = next(tokenIter)
			y = next(tokenIter)

			rx1 = float(rx)
			ry1 = float(ry)
			x1 = float(x)
			y1 = float(y)
			

			if commandUseCount >= 2 or lastCommand == 'm':
				# x,y is delta dx,dy
				x1 = arcX1 + x1
				y1 = arcY1 + y1
				arcX1 = x1
				arcY1 = y1
			else: # commandUseCount == 1
				# Remember original x,y positions
				arcX1 = x1
				arcY1 = y1
				# pass

			# rx2, ry2 = applyMatrixToPoint(rx1, ry1, a, b, c, d, e, f)
			rx2 = a*rx1 + c*ry1
			ry2 = b*rx1 + d*ry1
			# rx2 = a*rx1
			# ry2 = d*ry1
			x2, y2 = applyMatrixToPoint(x1, y1, a, b, c, d, e, f)

			if rx2 < 0:
				rx2 *= -1
				x2 -= rx2 * 2
			if ry2 < 0:
				ry2 *= -1
				y2 -= ry2 * 2

			if commandUseCount >= 2 or lastCommand == 'm':
				# Generate matrixed delta dx,dy
				dx = x2 - arcX2
				dy = y2 - arcY2
				dx = formatNumber(roundIfNeeded(dx))
				dy = formatNumber(roundIfNeeded(dy))
				rx2 = formatNumber(roundIfNeeded(rx2))
				ry2 = formatNumber(roundIfNeeded(ry2))
				arcX2 = x2
				arcY2 = y2
				commandStr = "{},{} {} {} {} {},{}".format(rx2, ry2, xAxisRotation, largeArcFlag, sweepFlag, dx, dy)
			else: # commandUseCount == 1
				# Remember matrixed x,y positions
				arcX2 = x2
				arcY2 = y2
				x2 = formatNumber(roundIfNeeded(x2))
				y2 = formatNumber(roundIfNeeded(y2))
				rx2 = formatNumber(roundIfNeeded(rx2))
				ry2 = formatNumber(roundIfNeeded(ry2))
				commandStr = "{},{} {} {} {} {},{}".format(rx2, ry2, xAxisRotation, largeArcFlag, sweepFlag, x2, y2)

			if lastCommand != 'a':
				commandStr = 'a ' + commandStr

			# print("\t\t({},{} ... {},{}) => ({})".format(rx, ry, x, y, commandStr))
			# print("\t\t[a] ({},{}) => ({})".format(x, y, commandStr))
			out.append(commandStr)

			# raise Exception("Implement path Arc to")


	el['d'] = ' '.join(out)


def removeGroupTransforms(svg):
	for g in svg.find_all('g'):
		transform = g.attrs.get('transform')
		# print(transform)
		# TODO: Support multiple functions in 1 tag.
		if transform is None or transform.strip() == '':
			continue
		elif 'translate(' in transform:
			# translateChildren()
			args = parseArgs(transform)
			transformChildren(g, applyTranslate, *args)
			del g.attrs['transform']
		elif 'matrix(' in transform:
			# translateChildren()
			args = parseArgs(transform)
			transformChildren(g, applyMatrix, *args)
			del g.attrs['transform']
		else:
			raise Exception('Unsupported transform', transform)

def removeRectTransforms(svg):
	for rect in svg.find_all('rect'):
		# print(rect)
		transform = rect.attrs.get('transform')
		# print(transform)
		# TODO: Support multiple functions in 1 tag.
		if transform is None or transform.strip() == '':
			continue
		elif 'scale(' in transform:
			args = parseArgs(transform)
			applyScaleToRect(rect, *args)
			del rect.attrs['transform']
		elif 'matrix(' in transform:
			args = parseArgs(transform)
			applyMatrixToRect(rect, *args)
			del rect.attrs['transform']
		else:
			raise Exception('Unsupported transform', transform)

def removeTransforms(svg):
	removeRectTransforms(svg)
	removeGroupTransforms(svg)


def printHelp():
	print('python3 removeSvgTransforms.py [svgFile]')
	print('\tEg: python3 removeSvgTransforms.py _templates/tasks-outside.svg')

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		inSvgPath = sys.argv[1]
		outSvgPath = sys.argv[1]
	else:
		if False:
			inSvgPath = '_templates/tasks-outside.svg'
			outSvgPath = 'test.svg'
		else:
			printHelp()
			sys.exit(1)

	with open(inSvgPath, 'r') as fin:
		soup = BeautifulSoup(fin, 'xml')
		svg = soup.find('svg')
		removeTransforms(svg)
		s = renderSvg(svg)
	# print(s)

	with open(outSvgPath, 'w') as fout:
		fout.write(s)
