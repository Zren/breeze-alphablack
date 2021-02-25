## v19 - February 25 2021

* Refactor `panel-background.svg` to reuse the `dialog/background.svg`.
* Add thick margins to the panel svg to support Plasma 5.21's Margin Separator widgets. A 24px panel will have a 1px thick margin. A 30px panel will have a 4px thick margin. A 38px panel will have a 8px thick margin.

## v18 - December 11 2020

* Fix pale popups caused by the Background Contrast Desktop Effect (Issue #21). Added `ContrastEffect` properties in `metadata.desktop` in an attempt to fix it, however the proper fix was to ship a pre-generated `dialogs/background.svg`.
* Refactor `background.svg` to add `dialog.radius` which doesn't really work well.
* Fix `resettitlebarcolors` mentioned in AlphaBlackControl's Issue 2.
* Only use blue shifted DecorationFocus for Complementary colors (Issue #20)
* Set Header color group to fix white `plasmoidheading.svg` in Plasma 5.20

## v17 - June 16 2020

* Added `widgets/plasmoidheading.svg` to show the solid notification heading like Breeze. It's only displayed if the current theme has the svg, it does not inherit this svg.
* Removed all deprecated `set___color.py` scripts. Use the `desktoptheme.py` subcommands.

## v16 - March 15 2020

* Move `set___color.py` etc into `desktoptheme.py` as subcommands. Eg: `python3 desktoptheme.py set dialog.opacity 0.7`. The existing scripts are deprecated and will be removed in the next version.
* Add ability to set dialog padding with `python3 desktoptheme.py set dialog.padding 2`. Note that you need to close a popup and reopen it to see the change in padding. You may need to run the command a few times for it to take effect.

## v15 - March 17 2019

* Cleanup the desktop widget background svg coordinates (`widget/background.svg`).
* Use Breeze's rectangle new rounded corner popup dialog svg from KDE Frameworks 5.56.
* Fix the dialog popup color (when using a custom opacity) broken by the Qt 5.12.2 update. The default dialog popups and tooltips will be fixed in KDE Frameworks 5.56.2 or 5.57.0.

## v14 - December 15 2018

* Use Breeze's rectangle corner popup svg. Somewhere along the line this theme ended up using a different svg with round corners for some reason.
* Add `sethighlightcolor.py` to set the selection/highlight color.

## v13 - October 12 2018

* Hide the panel shadow when the panel opacity is set below 30% (`0.3`).
* Update the desktop widget background to use the same look as breeze.
* Add `settextcolor.py` to change the panel/widget/titlebar text color.
* Fix `resettitlebarcolor.py` not working for color schemes installed in the home directory (`~/.local/share/color-scheme/`. It previously only worked for color schemes in the root directory (`/usr/share/color-scheme/`). This fix also scans all color schemes when the color scheme filename is not the typical `{ColorSchemeName}.colors` (Eg: "Breeze Solarized Light" uses "BreezeSolarizedLight.colors").
* Add `resettodefaults.py` script to revert all changes.

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
