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
		# self.set(section, option, value)
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



class DesktopTheme:
	def __init__(self, themeName):
		self.themeName = themeName
		themeDir = os.path.abspath(os.path.expanduser('~/.local/share/plasma/desktoptheme'))
		self.themeDir = os.path.join(themeDir, themeName)

	def colorsConfig(self):
		filename = os.path.join(self.themeDir, 'colors')
		return KdeConfig(filename)

	def reloadTheme(self):
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

	def themeConfig(self):
		filename = os.path.join(self.themeDir, 'config.ini')
		config = KdeConfig(filename)
		config.default('dialog', 'opacity', 0.9)
		config.default('panel', 'opacity', 0.9)
		config.default('panel', 'padding', 2)
		config.default('panel', 'taskStyle', 'inside')
		config.default('theme', 'accentColor', '#000000')
		config.default('widget', 'opacity', 0.9)
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
		self.renderTemplate('widgets/panel-background.svg', **{
			'{{panelOpacity}}': str(config.getProp('panel.opacity')),
			'{{panelPadding}}': str(config.getProp('panel.padding')),
			'{{noPanelPadding}}': '<rect id="hint-no-border-padding"></rect>' if config.getint('panel', 'padding') == 0 else '',
		})
		print('noPanelPadding', config.getint('panel', 'padding') == 0)

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
		self.renderTemplate('widgets/background.svg', **{
			'{{fillOpacity}}': str(config.getProp('widget.opacity')),
		})

	def setWidgetOpacity(self, newOpacity=0.9):
		config = self.themeConfig()
		config.set('widget', 'opacity', newOpacity)
		self.renderWidgetBackground(config)
		config.save()
		self.clearCache() # Not really necessary
		self.reloadTheme()

	def setAccentColor(self, newColor='0,0,0'):
		textColor = '255,255,255'
		altColor = deltaColor(newColor, 23)
		compColor = deltaColor(newColor, 17)

		print('BackgroundNormal: {}'.format(newColor))
		print('BackgroundAlternate: {}'.format(altColor))
		print('Complementary.BackgroundNormal: {}'.format(compColor))

		setTitlebarColors(newColor)

		colors = self.colorsConfig()
		colors['Colors:Button']['BackgroundNormal'] = compColor
		colors['Colors:Button']['BackgroundAlternate'] = altColor
		colors['Colors:View']['BackgroundNormal'] = newColor
		colors['Colors:View']['BackgroundAlternate'] = altColor
		colors['Colors:Window']['BackgroundNormal'] = newColor
		colors['Colors:Window']['BackgroundAlternate'] = altColor
		colors['Colors:Complementary']['BackgroundNormal'] = compColor
		colors['Colors:Complementary']['BackgroundAlternate'] = altColor
		colors.save()

		config = self.themeConfig()
		config.set('theme', 'accentColor', newColor)
		config.save()

		self.reloadTheme()

	def setTasksSvg(self, taskTheme):
		templatePath = "tasks-{}.svg".format(taskTheme)
		self.useTemplate(templatePath, 'widgets/tasks.svg')

		config = self.themeConfig()
		config.set('panel', 'taskStyle', taskTheme)
		config.save()

		self.reloadTheme()


