#!/usr/bin/python3

import sys, os
from desktoptheme import BreezeAlphaBlack

def printHelp():
	print("python3 settasksvg.py [style]")
	print("\t[style] can be 'inside' (like Breeze) or 'outside' (like Win10)")
	print("\tEg: python3 settasksvg.py outside")

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		try:
			desktopTheme = BreezeAlphaBlack()
			desktopTheme.setTasksSvg(sys.argv[1])
		except Exception as e:
			print(e)
			printHelp()
			sys.exit(0)
	else:
		printHelp()
		print()
		print("No theme given.")
