#!/usr/bin/python3

import configparser # Python 3 only
import sys, os
import glob
import time
import shutil

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

	def set(self, section, option, value):
		if not self.has_section(section):
			self.add_section(section)
		super().set(section, option, str(value))

	def setProp(self, key, value):
		section, option = key.split('.', 1)
		return self.set(section, option, value)

	def getProp(self, key):
		section, option = key.split('.', 1)
		return self.get(section, option)

	def default(self, section, option, value):
		if not self.has_option(section, option):
			self.set(section, option, value)

	def save(self):	
		with open(self.filename, 'w') as fp:
			self.write(fp, space_around_delimiters=False)

def limit(minVal, val, maxVal):
	return min(max(minVal, val), maxVal)

def limitColor(val):
	return limit(0, val, 255)

def deltaColor(colorStr, delta):
	r, g, b = map(int, colorStr.split(','))
	if max(r, g, b) >= 128:
		d = -delta
	else:
		d = delta
	return '{},{},{}'.format(limitColor(r+d), limitColor(g+d), limitColor(b+d))




def setTitlebarColors(backgroundColor='0,0,0', textColor='255,255,255'):
	filename = os.path.abspath(os.path.expanduser('~/.config/kdeglobals'))
	kdeglobals = KdeConfig(filename)
	kdeglobals['WM']['activeBackground'] = backgroundColor
	kdeglobals['WM']['inactiveBackground'] = backgroundColor
	kdeglobals['WM']['frame'] = backgroundColor
	kdeglobals['WM']['inactiveFrame'] = backgroundColor
	kdeglobals['WM']['activeForeground'] = textColor
	kdeglobals['WM']['inactiveForeground'] = textColor
	kdeglobals.save()

def applyColorSchemeTitlebarColors(kdeglobals, colorScheme):
	# Default to Breeze.colors if the file leaves it undefined.
	activeBackgroundColor = colorScheme['Colors:Window'].get('BackgroundNormal', '239,240,241')
	kdeglobals['WM']['activeBackground'] = colorScheme['WM'].get('activeBackground', '71,80,87') 
	kdeglobals['WM']['inactiveBackground'] = colorScheme['WM'].get('inactiveBackground', '239,240,241')
	kdeglobals['WM']['frame'] = colorScheme['WM'].get('frame', activeBackgroundColor)
	kdeglobals['WM']['inactiveFrame'] = colorScheme['WM'].get('inactiveFrame', kdeglobals['WM']['frame'])
	kdeglobals['WM']['activeForeground'] = colorScheme['WM'].get('activeForeground', '252,252,252')
	kdeglobals['WM']['inactiveForeground'] = colorScheme['WM'].get('inactiveForeground', '189,195,199')
	kdeglobals.save()



def scanForColorScheme(colorSchemeName):
	def testColorSchemeName(colorScheme, colorSchemeName):
		return colorScheme['General'].get('Name', '') == colorSchemeName

	def scanColorSchemeDir(colorSchemeDir):	
		colorSchemeFilename = colorSchemeName + '.colors'
		dirFilenames = os.listdir(colorSchemeDir)

		# First check to see if the obvious filename exists.
		if colorSchemeFilename in dirFilenames:
			# If so, move it to the front.
			dirFilenames.insert(0, dirFilenames.pop(dirFilenames.index(colorSchemeFilename)))

		# Scan folder for the correct color scheme
		for filename in os.listdir(colorSchemeDir):
			colorSchemeFilepath = os.path.join(colorSchemeDir, filename)
			# print(colorSchemeFilepath)

			if not filename.endswith('.colors'):
				continue

			if not os.path.isfile(colorSchemeFilepath):
				continue

			colorScheme = KdeConfig(colorSchemeFilepath)
			if testColorSchemeName(colorScheme, colorSchemeName):
				return colorScheme

		# Color scheme was not found in this dir
		return None


	# 1st: Check the home color-scheme dir (downloads by the user).
	homeColorSchemeFilepath = os.path.abspath(os.path.expanduser('~/.local/share/color-schemes/'))
	colorScheme = scanColorSchemeDir(homeColorSchemeFilepath)
	if colorScheme:
		return colorScheme

	# 2nd: Check the root color-scheme dir.
	colorScheme = scanColorSchemeDir('/usr/share/color-schemes/')
	if colorScheme:
		return colorScheme

	# No color scheme fulfulled the conditions anywhere
	return None

def resetTitlebarColors():
	kdeglobalsFilename = os.path.abspath(os.path.expanduser('~/.config/kdeglobals'))
	kdeglobals = KdeConfig(kdeglobalsFilename)

	colorSchemeName = kdeglobals['General'].get('ColorScheme', 'Breeze')

	colorScheme = scanForColorScheme(colorSchemeName)
	if colorScheme:
		applyColorSchemeTitlebarColors(kdeglobals, colorScheme)

	# elif os.path.isfile(localDesktopThemeFilename):
	# elif os.path.isfile(rootDesktopThemeFilename):
		# The color scheme is probably in a desktop theme folder...
		# Whatever, user can reapply it.
	else:
		# Deleting the keys will use white + highlight color,
		# which isn't the same as the default Breeze colors.
		del kdeglobals['WM']['activeBackground']
		del kdeglobals['WM']['inactiveBackground']
		del kdeglobals['WM']['frame']
		del kdeglobals['WM']['inactiveFrame']
		del kdeglobals['WM']['activeForeground']
		del kdeglobals['WM']['inactiveForeground']
		kdeglobals.save()

class DesktopTheme:
	def __init__(self, themeName):
		self.themeName = themeName
		themeDir = os.path.abspath(os.path.expanduser('~/.local/share/plasma/desktoptheme'))
		self.themeDir = os.path.join(themeDir, themeName)
		self.dontReload = False

	def colorsConfig(self):
		filename = os.path.join(self.themeDir, 'colors')
		return KdeConfig(filename)

	def reloadTheme(self):
		if self.dontReload:
			# We're setting multiple properties at once,
			# and want to skip automatically reloading
			# after each change.
			return

		# Switch to another theme and back to apply the changes to breeze-alphablack.
		filename = os.path.abspath(os.path.expanduser('~/.config/plasmarc'))
		plasmarc = KdeConfig(filename)

		# Make sure we're not already in the process of changing the theme.
		if plasmarc['Theme']['name'] == self.themeName:
			plasmarc['Theme']['name'] = 'breeze-dark'
			plasmarc.save()
			time.sleep(1)
		plasmarc['Theme']['name'] = self.themeName
		plasmarc.save()

	def clearCache(self):
		wildcardPath='plasma-svgelements-{}_*'.format(self.themeName)
		cacheDir = os.path.realpath(os.path.expanduser('~/.cache/'))
		for file in glob.glob(os.path.join(cacheDir, wildcardPath)):
			print('Deleting cached theme file "{}"'.format(file))
			os.remove(file)

		wildcardPath='plasma_theme_{}_*.kcache'.format(self.themeName)
		for file in glob.glob(os.path.join(cacheDir, wildcardPath)):
			print('Deleting cached theme file "{}"'.format(file))
			os.remove(file)



class BreezeAlphaBlack(DesktopTheme):
	def __init__(self, themeName='breeze-alphablack'):
		super().__init__(themeName=themeName)
		self.configProps = [
			# (group, key, defaultValue, setterKey)
			('dialog', 'opacity', 0.9, 'setDialogOpacity'),
			('panel', 'opacity', 0.9, 'setPanelOpacity'),
			('panel', 'padding', 2, 'setPanelPadding'),
			('panel', 'taskStyle', 'inside', 'setTasksSvg'),
			('theme', 'accentColor', '0,0,0', 'setAccentColor'),
			('theme', 'textColor', '239,240,241', 'setTextColor'),
			('widget', 'opacity', 0.9, 'setWidgetOpacity'),
		]

	def themeConfig(self):
		filename = os.path.join(self.themeDir, 'config.ini')
		config = KdeConfig(filename)
		for (group, key, value, setterKey) in self.configProps:
			config.default(group, key, value)
		return config

	def useTemplate(self, inPath, outPath):
		templatePath = os.path.join(self.themeDir, '_templates', inPath)
		outPath = os.path.join(self.themeDir, outPath)
		shutil.copyfile(templatePath, outPath)
		self.reloadTheme()

	def renderTemplate(self, templatePath, **kwargs):
		inFilename = os.path.join(self.themeDir, '_templates', templatePath)
		outFilename = os.path.join(self.themeDir, templatePath)
		outDir = os.path.dirname(outFilename)
		os.makedirs(outDir, exist_ok=True)
		with open(inFilename, 'r') as fin:
			with open(outFilename, 'w') as fout:
				for line in fin:
					for a, b in kwargs.items():
						line = line.replace(a, b)
					fout.write(line)

	def renderDialogBackground(self, config):
		self.renderTemplate('dialogs/background.svg', **{
			'{{fillOpacity}}': str(config.getProp('dialog.opacity')),
		})

	def setDialogOpacity(self, newOpacity=0.9):
		config = self.themeConfig()
		config.set('dialog', 'opacity', newOpacity)
		self.renderDialogBackground(config)
		config.save()
		self.clearCache() # Not really necessary
		self.reloadTheme()

	def renderPanel(self, config):
		# inFilename = os.path.join(self.themeDir, '_templates/panel-background.svg')
		# outFilename = os.path.join(self.themeDir, 'widgets/panel-background.svgz')
		# buildFromTemplate(inFilename, outFilename, **{
		panelOpacity = config.getProp('panel.opacity')
		noPanelPadding = config.getint('panel', 'padding') == 0
		shadowOpacity = 1 if float(panelOpacity) >= 0.3 else 0
		self.renderTemplate('widgets/panel-background.svg', **{
			'{{panelOpacity}}': str(panelOpacity),
			'{{panelPadding}}': str(config.getProp('panel.padding')),
			'{{noPanelPadding}}': '<rect id="hint-no-border-padding"></rect>' if noPanelPadding else '',
			'{{shadowOpacity}}': str(shadowOpacity),
		})
		print('noPanelPadding', noPanelPadding)
		print('shadowOpacity', shadowOpacity)

	def setPanelOpacity(self, newOpacity=0.9):
		config = self.themeConfig()
		config.set('panel', 'opacity', newOpacity)
		self.renderPanel(config)
		config.save()
		self.clearCache() # Not really necessary
		self.reloadTheme()

	def setPanelPadding(self, newPadding=2):
		config = self.themeConfig()
		config.set('panel', 'padding', newPadding)
		self.renderPanel(config)
		config.save()
		self.clearCache() # Necessary
		self.reloadTheme()

	def renderWidgetBackground(self, config):
		# Breeze's widget/background.svg
		# fill: 0.9
		# shadows: 1.0 (Linear gradients)
		# corner shadows: 0.6 (Radial gradients)
		fillOpacity = float(config.getProp('widget.opacity'))
		if fillOpacity == 0:
			# Hide shadows completely if there's no fill
			shadowOpacity = 0
			cornerOpacity = 0
		else:
			shadowOpacity = min(fillOpacity + 0.1, 1)
			cornerOpacity = 0.6 * shadowOpacity
		
		self.renderTemplate('widgets/background.svg', **{
			'{{fillOpacity}}': str(fillOpacity),
			'{{shadowOpacity}}': str(shadowOpacity),
			'{{cornerOpacity}}': str(cornerOpacity),
		})

	def setWidgetOpacity(self, newOpacity=0.9):
		config = self.themeConfig()
		config.set('widget', 'opacity', newOpacity)
		self.renderWidgetBackground(config)
		config.save()
		self.clearCache() # Not really necessary
		self.reloadTheme()

	def applyColors(self, newColor='0,0,0', textColor='239,240,241'):
		altColor = deltaColor(newColor, 23)
		compColor = deltaColor(newColor, 17)

		print('BackgroundNormal: {}'.format(newColor))
		print('BackgroundAlternate: {}'.format(altColor))
		print('Complementary.BackgroundNormal: {}'.format(compColor))

		setTitlebarColors(newColor, textColor)

		colors = self.colorsConfig()
		colors['Colors:Button']['BackgroundNormal'] = compColor
		colors['Colors:Button']['BackgroundAlternate'] = altColor
		colors['Colors:Button']['ForegroundNormal'] = textColor
		colors['Colors:View']['BackgroundNormal'] = newColor
		colors['Colors:View']['BackgroundAlternate'] = altColor
		colors['Colors:View']['ForegroundNormal'] = textColor
		colors['Colors:Window']['BackgroundNormal'] = newColor
		colors['Colors:Window']['BackgroundAlternate'] = altColor
		colors['Colors:Window']['ForegroundNormal'] = textColor
		colors['Colors:Complementary']['BackgroundNormal'] = compColor
		colors['Colors:Complementary']['BackgroundAlternate'] = altColor
		colors['Colors:Complementary']['ForegroundNormal'] = textColor
		colors.save()

		config = self.themeConfig()
		config.set('theme', 'accentColor', newColor)
		config.set('theme', 'textColor', textColor)
		config.save()

		self.reloadTheme()

	def setAccentColor(self, accentColor='0,0,0'):
		config = self.themeConfig()
		textColor = config.get('theme', 'textColor')
		self.applyColors(accentColor, textColor)

	def setTextColor(self, textColor):
		config = self.themeConfig()
		accentColor = config.get('theme', 'accentColor')
		self.applyColors(accentColor, textColor)

	def setTasksSvg(self, taskTheme):
		templatePath = "tasks-{}.svg".format(taskTheme)
		self.useTemplate(templatePath, 'widgets/tasks.svg')

		config = self.themeConfig()
		config.set('panel', 'taskStyle', taskTheme)
		config.save()

		self.reloadTheme()

	def resetToDefaults(self):
		self.dontReload = True
		for (group, key, value, setterKey) in self.configProps:
			print("===[ {}.{}: {} ]===".format(group, key, value))
			setter = getattr(self, setterKey)
			setter(value)

		self.dontReload = False
		self.reloadTheme()
