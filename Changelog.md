## v13 - October 12 2018

* Hide the panel shadow when the panel opacity is set below 30% (`0.3`).
* Update the desktop widget background to use the same look as breeze.
* Fix `resettitlebarcolor.py` not working for color schemes installed in the home directory (`~/.local/share/color-scheme/`. It previously only worked for color schemes in the root directory (`/usr/share/color-scheme/`). This fix also scans all color schemes when the color scheme filename is not the typical `{ColorSchemeName}.colors` (Eg: "Breeze Solarized Light" uses "BreezeSolarizedLight.colors").

## v12 - July 26 2018

* Add settitlebarcolor.py and resettitlebarcolor.py to easily reset the titlebar color. v3 of the widget has buttons that will run these scripts.

## v11 - June 24 2018

* Remove the opache and transparent folders which don't appear to do anything (they aren't overriding breeze).
* Add new templates + scripts to set the panel popups/dialog opacity, and the desktop widget opacity. The new scripts are setdialogopacity.py and setwidgetopacity.py. Both work the same as setpanelopacity.py.

## v10 - May 29 2018

* Follow color scheme when compositor is off. Gets rid of white outline when compositor is off.
* Add breeze's widgets/tabbar.svg, as Plasma doesn't allow it to "inherit" this svg. This fixes/adds the "popup is open" blue line.
* Add alternative tasks.svg where the line is on the outside/edge of the screen line Windows 10. Use the config widget, or the settasksvg.py script, to change to it.
* "Unzip" the svgz into svg, and cleanup the xml.

## v9 - February 20 2017

* Fix panel opacity script so it can be run anywhere.

## v8 - January 21 2017

* Add a script to set the panel opacity.

## v7

* Fix the minimized tasks svg (showed nothing instead of looking like a "normal" task)
* Use a hardcoded #f67400 orange for highlighted tasks instead of the NeutralText color from the color scheme.

## v6

* Use the Breeze 5.8 tasks.svg (thinner line), but with minimized tasks looking the same as a normal task.

## v5

* Add script to change the color.


## v3 - June 16 2016

* Theme progressbar in tasks.

## v2 - June 15 2016

* Got rid of the white line at the top of the panel
* Got rid of the pink spot in the pager
