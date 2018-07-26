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

### "AlphaBlack Control" Widget

![](https://i.imgur.com/TYxCBnc.jpg)

v10 introduced an accompying widget to easily change the theme's accent color, panel opacity, or change the taskbar to look a bit more like Windows 10.

You can [download the widget here](https://store.kde.org/p/1237963/), or install it via the GUI:

1. Right click the Panel > Add Widgets
2. Get New Widgets > Download
3. Search for "AlphaBlack Control" and install it.

After installing, the widget should appear in your system tray. If you lock your widgets, it will hide in the system tray popup.


### Command Line

#### Panel Opacity

Run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/setpanelopacity.py 0.75` where 0.75 means the panel is 75% visible.


#### Panel Color + Window Decorations

Run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/setthemecolor.py 255,255,255` where 255,255,255 is your desired RGB color.


#### Window Decorations

Run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/settitlebarcolor.py 255,255,255` where 255,255,255 is your desired RGB color.

Run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/resettitlebarcolor.py` to reapply the colors from your seleted color scheme.

#### Task Manager Theme

Run `python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/settasksvg.py outside` where 'outside' draws the line on the edge of the screen like Windows 10, or 'inside' like Breeze.



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
