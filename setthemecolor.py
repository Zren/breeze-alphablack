#!/usr/bin/python3

import configparser # Python 3 only
import os
import sys
import time

# KDE rc files differences:
#     Keys are cAsE sensitive
#     No spaces around the =
#     [Sections can have spaces and : colons]
# Also (NOT FIXED):
#     Can have [Sub][Sections]
class KdeConfig(configparser.ConfigParser):
	def __init__(self, filename):
		super().__init__()

		# Keep case sensitive keys
		# http://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case
		self.optionxform = str

		self.filename = filename
		self.read(self.filename)

	def save(self):	
		with open(self.filename, 'w') as fp:
			self.write(fp, space_around_delimiters=False)
		

def printHelp():
	print("python3 setthemecolor.py [red],[green],[blue]")
	print("\t[red/green/blue] are integers from 0-255")
	print("\tEg: python3 setthemecolor.py 0,0,0")

def setThemeColor(newColor='0,0,0'):
	#filename = os.path.abspath(os.path.expanduser('~/Code/kdeglobals'))
	filename = os.path.abspath(os.path.expanduser('~/.config/kdeglobals'))
	config = KdeConfig(filename)
	config['WM']['activeBackground'] = newColor
	config['WM']['inactiveBackground'] = newColor
	config['WM']['frame'] = newColor
	config['WM']['inactiveFrame'] = newColor
	config.save()

	#filename = os.path.abspath(os.path.expanduser('~/Code/colors'))
	filename = os.path.abspath(os.path.expanduser('~/.local/share/plasma/desktoptheme/breeze-alphablack/colors'))
	config = KdeConfig(filename)
	config['Colors:Window']['BackgroundNormal'] = newColor
	config.save()

	# Switch to another theme and back to apply the changes to breeze-alphablack.
	#filename = os.path.abspath(os.path.expanduser('~/Code/plasmarc'))
	filename = os.path.abspath(os.path.expanduser('~/.config/plasmarc'))
	config = KdeConfig(filename)

	# Make sure we're not already in the process of changing the theme.
	if config['Theme']['name'] == 'breeze-alphablack':
		config['Theme']['name'] = 'breeze-dark'
		config.save()
		time.sleep(1)
		config['Theme']['name'] = 'breeze-alphablack'
		config.save()

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		try:
			r,g,b = map(int, sys.argv[1].split(','))
			print("Red", r)
			print("Green", g)
			print("Blue", b)
			newColor = "{},{},{}".format(r, g, b)
			setThemeColor(newColor)
		except Exception as e:
			printHelp()
			sys.exit(0)
	else:
		printHelp()
		#sys.exit(0)
		print()
		print("No color given. Using the default 0,0,0 (black).")
		setThemeColor('0,0,0')
