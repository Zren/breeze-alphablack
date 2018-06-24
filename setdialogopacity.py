#!/usr/bin/python3

import sys, os
from desktoptheme import BreezeAlphaBlack

def printHelp():
	print("python3 setdialogopacity.py [opacity]")
	print("\t[opacity] is a real number from 0.0 to 1.0")
	print("\tEg: python3 setdialogopacity.py 0.6")

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		try:
			desktopTheme = BreezeAlphaBlack()
			desktopTheme.setDialogOpacity(sys.argv[1])
		except Exception as e:
			print(e)
			printHelp()
			sys.exit(0)
	else:
		printHelp()
		print()
		print("No opacity given.")
