#!/usr/bin/python3

import sys, os
from desktoptheme import BreezeAlphaBlack

def printHelp():
	print("python3 resettodefaults.py")

if __name__ == '__main__':
	desktopTheme = BreezeAlphaBlack()
	desktopTheme.resetToDefaults()
