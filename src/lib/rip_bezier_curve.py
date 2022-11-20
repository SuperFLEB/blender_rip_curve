import bpy


def get_selected_spline(obj: bpy.types.Object):
    """Return the first selected Bezier spline, or None if none is selected"""
    for spline in obj.data.splines:
        for point in spline.bezier_points:
            if point.select_control_point:
                return spline
    return None


def copy_spline(obj: bpy.types.Object, spline: bpy.types.Spline):
    """Copy the given Bezier spline. Clears the current selection and causes all points of the new spline to be seleted.
       Returns the newly-created spline."""
    bpy.ops.curve.select_all(action='DESELECT')
    for p in spline.bezier_points:
        p.select_control_point = True
    bpy.ops.curve.duplicate_move()
    new_spline = get_selected_spline(obj)
    return new_spline


def get_active_points():
    """Get all active Bezier points. Returns an (obj, spline, point) tuple"""
    points = []
    for ob in bpy.context.selected_objects:
        if ob.type != "CURVE":
            continue
        for spl in ob.data.splines:
            if spl.type != "BEZIER":
                continue
            for pt in spl.bezier_points:
                if pt.select_control_point:
                    points.append((ob, spl, pt))
    return points


def split_on_point(obj: bpy.types.Object, spline: bpy.types.Spline, point: bpy.types.BezierSplinePoint):
    """Split the given obj's given spline on the given point. Changes the selection to the split point."""
    split_index = [idx for idx, pt in enumerate(spline.bezier_points) if pt == point][0]
    new_spline = copy_spline(obj, spline)
    bpy.ops.curve.select_all(action='DESELECT')
    for idx, _ in enumerate(spline.bezier_points):
        # The lack of handling = is intentional. If it's equal to the split_index, the point stays on both.
        if idx < split_index:
            new_spline.bezier_points[idx].select_control_point = True
        if idx > split_index:
            spline.bezier_points[idx].select_control_point = True
    bpy.ops.curve.delete(type="VERT")
    spline.bezier_points[split_index].select_control_point = True
