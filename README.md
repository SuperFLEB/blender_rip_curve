# "Rip Bezier Curve" Blender Addon

https://github.com/SuperFLEB/blender_rip_bezier_curve

This Blender addon adds an option to the Edit Mode Bezier Point "X" (delete) menu to rip
the point. This will split the curve in two at the selected point (duplicating the point on
both).

## To install

Either install the ZIP file from the release or clone this repository and use the
build_release.py script to build a ZIP file that you can install into Blender.

## To use

Go into Edit mode on a Bezier curve, select a single point, and hit "X". Select the "Rip Curve"
menu item.

If more than one point is selected, the action will not be available. You cannot rip multiple points
at once with this addon.
