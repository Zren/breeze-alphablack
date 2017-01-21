# Breeze AlphaBlack

Breeze Light theme with minor improvements and a black panel/titlebar.

https://store.kde.org/p/1084931/

## Screenshots

![](https://cn.pling.com/img//hive/content-pre1/175800-1.png)

## Install

* System Settings > Desktop Theme
* Get New Themes...
* Search for "Breeze AlphaBlack", install it, then apply it.
* If you want the breeze window decorations in black, run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/setthemecolor.py 0,0,0`

## Customize Theme

#### Panel Opacity

Run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/setpanelopacity.py 0.75` where 0.75 means the panel is 75% visible.


#### Color Picker (installs `qml`)

Video: https://streamable.com/kcv1

Run `sh ~/.local/share/plasma/desktoptheme/breeze-alphablack/themeeditor` which will display a color picker for you to choose your theme color.


### Panel Color + Window Decorations (Just `python3`)

Run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/setthemecolor.py 255,255,255` where 255,255,255 is your desired RGB color.


## Window Decorations

To color the the default breeze window decorations (window titlebars). You can either:

1. Download a custom window decoration.
2. Use the Color Picker script above.
3. Use the System Settings > Colors > Colors section to color the titlebar background/foreground. You will not be able to color the frame color (bottom/left/right of the window) from this menu.
4. Add/set the following values in your `~/.config/kdeglobals` file to set the borders to black (when using the breeze window decorations).

```ini
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
```

## Misc

* Wiki for Editing Desktop Themes  
  https://techbase.kde.org/Development/Tutorials/Plasma5/ThemeDetails
