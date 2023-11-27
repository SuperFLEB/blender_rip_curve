import bpy
from typing import Set
from bpy.types import Operator
from ..lib import pkginfo
from ..lib import rip_curve

if "_LOADED" in locals():
    import importlib

    for mod in (pkginfo, rip_curve):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = pkginfo.package_name()
get_selected_points_info = rip_curve.get_selected_points_info
split_on_point = rip_curve.split_on_point


class RIP_CURVE_OT_Rip(Operator):
    """Rip a Curve (split it in two at the selected vertex)"""
    bl_idname = "rip_curve.rip"
    bl_label = "Rip Curve"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def failcheck(cls):
        active_points = get_selected_points_info()
        active_points_ct = len(active_points)

        # This can occur if they selected the left or right control point. I _should_ handle this case, but I'm not yet.
        if active_points_ct == 0:
            return "No points selected. Select the center control point of a single point."

        # I am lazy and this is full of operator calls that mess with the selection, so it's only supporting a
        # single point for now.
        if active_points_ct > 1:
            return f"This operator can only rip a single point. {active_points_ct} are selected."

        active_spline = active_points[0][1]
        active_spline_points = active_spline.points if active_spline.points else active_spline.bezier_points

        if active_points[0][2] == active_spline_points[0]:
            return f"Ripping the first point in a spline will accomplish nothing."

        if active_points[0][2] == active_spline_points[-1]:
            return f"Ripping the last point in a spline will accomplish nothing."

    @classmethod
    def poll(cls, context) -> bool:
        if bpy.context.active_object.mode != "EDIT":
            cls.poll_message_set("Not in Edit mode")
            return False

        fail = cls.failcheck()
        if fail:
            cls.poll_message_set(fail)
            return False

        return True

    def execute(self, context) -> Set[str]:
        fail = self.failcheck()
        if fail:
            self.report({'ERROR'}, fail)
            return {'FINISHED'}

        active_points = get_selected_points_info()
        split_on_point(*active_points[0])
        return {'FINISHED'}


REGISTER_CLASSES = [RIP_CURVE_OT_Rip]
