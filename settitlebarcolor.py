#!/usr/bin/python3

import sys, os
from desktoptheme import setTitlebarColors

def printHelp():
	print("python3 settitlebarcolor.py [red],[green],[blue]")
	print("\t[red/green/blue] are integers from 0-255")
	print("\tEg: python3 settitlebarcolor.py 0,0,0")
	print("python3 settitlebarcolor.py [bgColor] [textColor]")
	print("\tEg: python3 settitlebarcolor.py 0,0,0 239,240,241")

def parseColorStr(colorStr):
	r, g, b = map(int, colorStr.split(','))
	return "{},{},{}".format(r, g, b)

if __name__ == '__main__':
	try:
		if len(sys.argv) >= 3:
			bgColor = parseColorStr(sys.argv[1])
			textColor = parseColorStr(sys.argv[2])
			setTitlebarColors(bgColor, textColor)
		elif len(sys.argv) >= 2:
			bgColor = parseColorStr(sys.argv[1])
			setTitlebarColors(bgColor)
		else:
			printHelp()
			print()
			print("No color given. Using the default 0,0,0 (black).")
			setTitlebarColors('0,0,0')
	except Exception as e:
		print(e)
		printHelp()
		sys.exit(0)
