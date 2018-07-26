#!/usr/bin/python3

import sys, os
from desktoptheme import setTitlebarColors

def printHelp():
	print("python3 settitlebarcolor.py [red],[green],[blue]")
	print("\t[red/green/blue] are integers from 0-255")
	print("\tEg: python3 settitlebarcolor.py 0,0,0")

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		try:
			r, g, b = map(int, sys.argv[1].split(','))
			newColor = "{},{},{}".format(r, g, b)
			setTitlebarColors(newColor)
		except Exception as e:
			print(e)
			printHelp()
			sys.exit(0)
	else:
		printHelp()
		print()
		print("No color given. Using the default 0,0,0 (black).")
		setTitlebarColors('0,0,0')
