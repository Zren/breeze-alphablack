#!/usr/bin/python3

import sys, os
from desktoptheme import BreezeAlphaBlack

scriptFilename = 'settextcolor.py'
defaultColorName = 'white'
defaultColorStr = '239,240,241'

def printHelp():
	print("python3 {} [red],[green],[blue]".format(scriptFilename))
	print("\t[red/green/blue] are integers from 0-255")
	print("\tEg: python3 {} {}".format(scriptFilename, defaultColorStr))

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		try:
			r, g, b = map(int, sys.argv[1].split(','))
			newColor = "{},{},{}".format(r, g, b)
			desktopTheme = BreezeAlphaBlack()
			desktopTheme.setTextColor(newColor)
		except Exception as e:
			print(e)
			printHelp()
			sys.exit(0)
	else:
		printHelp()
		print()
		print("No color given. Using the default {} ({}).".format(defaultColorStr, defaultColorName))
		desktopTheme = BreezeAlphaBlack()
		desktopTheme.setTextColor(defaultColorStr)
