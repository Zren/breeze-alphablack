#!/usr/bin/python3

import sys, os
from desktoptheme import BreezeAlphaBlack

def printHelp():
	print("python3 settextcolor.py [red],[green],[blue]")
	print("\t[red/green/blue] are integers from 0-255")
	print("\tEg: python3 settextcolor.py 239,240,241")

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
		print("No color given. Using the default 239,240,241 (white).")
		desktopTheme = BreezeAlphaBlack()
		desktopTheme.setTextColor('239,240,241')
