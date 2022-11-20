# "Rip Curve" Blender Addon

https://github.com/SuperFLEB/blender_rip_curve

This Blender addon adds an action to the Curve Edit Mode Point Delete ("X") menu to "rip"
the point. This will split the curve in two splines at the selected point, cloning the selected point on
both the old and new. It does not separate the curve to a new Object, only a new Spline within the Curve Object.

Bezier and Polygonal curves are supported. Other curve types, such as NURBS, are not supported.

## To install

Either install the ZIP file from the release or clone this repository and use the
build_release.py script to build a ZIP file that you can install into Blender.

## To use

Go into Edit mode on a curve, select a single point, and hit "X". Select the "Rip Curve" menu item.

If more than one point is selected, the action will not be available. You cannot rip multiple points
at once with this addon.
