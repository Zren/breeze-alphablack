#!/usr/bin/python3

import sys, os
from desktoptheme import BreezeAlphaBlack

def printHelp():
	print("python3 setpanelpadding.py [pixels]")
	print("\t[opacity] is an integer from 0 to 40")
	print("\tEg: python3 setpanelpadding.py 2")

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		try:
			desktopTheme = BreezeAlphaBlack()
			desktopTheme.setPanelPadding(sys.argv[1])
		except Exception as e:
			print(e)
			printHelp()
			sys.exit(0)
	else:
		printHelp()
		print()
		print("No padding given.")
