### Panel Color

Edit `BackgroundNormal=0,0,0` under `[Colors:Window]` in the `colors` file.

### Window Decorations

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
