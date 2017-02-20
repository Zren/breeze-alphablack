#!/usr/bin/python3

from setthemecolor import reloadTheme
import os
import sys
import time
import gzip

def printHelp():
	print("python3 setpanelopacity.py [opacity]")
	print("\t[opacity] is a real number from 0.0 to 1.0")
	print("\tEg: python3 setpanelopacity.py 0.6")

def buildFromTemplate(inFilename, outFilename, **kwargs):
	with open(inFilename, 'r') as fin:
		# with open(outFilename, 'w') as fout:
		with gzip.open(outFilename, 'wb') as fout:
			for line in fin:
				for a, b in kwargs.items():
					line = line.replace(a, b)
				# fout.write(line)
				fout.write(line.encode('utf-8'))


def setPanelOpacity(newOpacity=0.6):
	themeDir = os.path.dirname(os.path.realpath(__file__))
	inFilename = os.path.join(themeDir, '_templates/panel-background.svg')
	outFilename = os.path.join(themeDir, 'widgets/panel-background.svgz')
	buildFromTemplate(inFilename, outFilename, **{
		'{{panelOpacity}}': str(newOpacity),
	})

	reloadTheme()


if __name__ == '__main__':
	if len(sys.argv) >= 2:
		try:
			setPanelOpacity(sys.argv[1])
		except Exception as e:
			print(e)
			printHelp()
			sys.exit(0)
	else:
		printHelp()
		#sys.exit(0)
		print()
		print("No opacity given.")
