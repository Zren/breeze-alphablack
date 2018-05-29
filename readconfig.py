#!/usr/bin/python3

import os
import sys
import json
from desktoptheme import BreezeAlphaBlack

desktoptheme = BreezeAlphaBlack()
config = desktoptheme.themeConfig()
out = {}
for section in config.sections():
	out[section] = {}
	for name, value in config.items(section):
		out[section][name] = value
print(json.dumps(out, indent="\t"))
