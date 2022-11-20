import bpy
from typing import Set
from bpy.types import Operator
from ..lib import pkginfo
from ..lib import rip_bezier_curve

if "_LOADED" in locals():
    import importlib

    for mod in (pkginfo, rip_bezier_curve):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = pkginfo.package_name()
get_active_points = rip_bezier_curve.get_active_points
split_on_point = rip_bezier_curve.split_on_point


class RipOperator(Operator):
    """Rip a Bezier Curve (split it in two at the selected vertex)"""
    bl_idname = "rip_bezier_curve.rip"
    bl_label = "Rip Bezier Curve"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def failcheck(cls):
        active_points = get_active_points()
        active_points_ct = len(active_points)

        # I am lazy and this is full of operator calls that mess with the selection, so it's only supporting a
        # single point for now.
        if active_points_ct > 1:
            return f"This operator can only rip a single point. {active_points_ct} are selected."

        if active_points[0][2] == active_points[0][1].bezier_points[0]:
            return f"Ripping the first point in a curve will accomplish nothing."

        if active_points[0][2] == active_points[0][1].bezier_points[-1]:
            return f"Ripping the last point in a curve will accomplish nothing."

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
        active_points = get_active_points()
        fail = self.failcheck()
        if fail:
            self.report({'ERROR'}, fail)
            return {'FINISHED'}

        split_on_point(*active_points[0])
        return {'FINISHED'}


REGISTER_CLASSES = [RipOperator]
