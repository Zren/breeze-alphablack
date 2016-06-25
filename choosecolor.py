#!/usr/bin/python2
import gtk # Python2 only?
import sys
# Credit to: https://gist.github.com/keitheis/2986210


csd = gtk.ColorSelectionDialog('Gnome Color Chooser')
cs = csd.colorsel
# cs.set_has_opacity_control(True)
# cs.set_current_alpha(65536)
if csd.run() != gtk.RESPONSE_OK:
   print('No color selected.')
   sys.exit(1)
c = cs.get_current_color()

newColor = "{},{},{}".format(c.red/256, c.green/256, c.blue/256)
print(newColor)
