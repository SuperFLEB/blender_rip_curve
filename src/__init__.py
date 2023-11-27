from typing import Callable
import bpy
from .operator import rip

if "_LOADED" in locals():
    import importlib

    for mod in (rip,):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = __package__

bl_info = {
    "name": "Rip Curve",
    "description": "Rip a Bezier or Polygonal Curve (split it in two at the selected vertex)",
    "author": "FLEB (a.k.a. SuperFLEB)",
    "version": (0, 1, 3),
    "blender": (3, 4, 0),
    "location": "View3D > Object",
    "warning": "",  # used for warning icon and text in addons panel
    "doc_url": "https://github.com/SuperFLEB/blender_rip_curve",
    "tracker_url": "https://github.com/SuperFLEB/blender_rip_curve/issues",
    "support": "COMMUNITY",
    "category": "3D View",
}


def menuitem(cls: bpy.types.Operator | bpy.types.Menu, operator_context: str = "EXEC_DEFAULT") -> Callable:
    if issubclass(cls, bpy.types.Operator):
        def operator_fn(self, context):
            self.layout.operator_context = operator_context
            self.layout.operator(cls.bl_idname)

        return operator_fn
    if issubclass(cls, bpy.types.Menu):
        def submenu_fn(self, context):
            self.layout.menu(cls.bl_idname)

        return submenu_fn
    raise Exception(f"Rip Curve: Unknown menu type for menu {cls}. The developer screwed up.")


# Registerable modules have a REGISTER_CLASSES list that lists all registerable classes in the module
registerable_modules = [
    rip
]

classes = []

menus = [
    # Curve edit mode "X" menu
    ["VIEW3D_MT_edit_curve_delete", menuitem(rip.RIP_CURVE_OT_Rip)],
]


def get_classes() -> list:
    # Uses a set to prevent doubles, and a list to preserve order
    all_classes = classes.copy()
    known_classes = set(classes)
    for module in [m for m in registerable_modules if hasattr(m, "REGISTER_CLASSES")]:
        for cls in [c for c in module.REGISTER_CLASSES if c not in known_classes]:
            all_classes.append(cls)
            known_classes.add(cls)
    return all_classes


def register() -> None:
    all_classes = get_classes()

    for c in all_classes:
        # Attempt to clean up if the addon broke during registration.
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass
        bpy.utils.register_class(c)
        print("Rip Curve registered class:", c)
    for m in menus:
        getattr(bpy.types, m[0]).append(m[1])


def unregister() -> None:
    all_classes = get_classes()
    for m in menus[::-1]:
        getattr(bpy.types, m[0]).remove(m[1])
    for c in all_classes[::-1]:
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
