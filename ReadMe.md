# Breeze AlphaBlack

Breeze Light theme with minor improvements and a black panel/titlebar.

## Screenshots

![](http://kdelook.org/CONTENT/content-pre1/175800-1.png)

## Install

* System Settings > Desktop Theme
* Get New Themes...
* Search for "Breeze AlphaBlack", install it, then apply it.
* If you want the breeze window decorations in black, run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/setthemecolor.py 0,0,0`

## Customize Theme

### Panel Color + Window Decorations

Run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/setthemecolor.py 255,255,255` where 255,255,255 is your desired RGB color.


#### Color Picker

Video: https://zippy.gfycat.com/SizzlingSecondaryBovine.webm

Run `sh ~/.local/share/plasma/desktoptheme/breeze-alphablack/themeeditor` which will display a color picker for you to choose your theme color.

### Panel Color (Manually)

First go to: `~/.local/share/plasma/desktoptheme/breeze-alphablack/`.

Note: To apply the your changes to the theme, you'll need to apply another theme, then switch back to this theme since it doesn't detect when the theme files change.

Edit `BackgroundNormal=0,0,0` under `[Colors:Window]` in the `colors` file.

### Window Decorations (Manually)

To color the the default breeze window decorations (window titlebars). You can either:

1. Download a custom window decoration.
2. Use the System Settings > Colors > Colors section to color the titlebar background/foreground. You will not be able to color the frame color (bottom/left/right of the windw) from this menu.
3. Add/set the following values in your `~/.config/kdeglobals` file.

	[WM]
	activeBackground=0,0,0
	activeBlend=17,17,17
	activeFont=Noto Sans,10,-1,5,50,0,0,0,0,0
	activeForeground=239,240,241
	inactiveBackground=8,8,8
	inactiveBlend=75,71,67
	inactiveForeground=189,195,199
	frame=0,0,0
	inactiveFrame=8,8,8


Note that #3 allows you to set the frame color (to black).
