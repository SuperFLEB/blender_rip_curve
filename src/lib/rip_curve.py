import bpy
from bpy.types import Object, Spline, SplinePoint, BezierSplinePoint
from typing import Iterable, Sized

def get_selected_spline(obj: Object):
    """Return the first selected spline, or None if none is selected"""
    for spline in obj.data.splines:
        points = get_points_collection(spline)
        attr = 'select_control_point' if spline.type == "BEZIER" else 'select'
        for point in points:
            if getattr(point, attr):
                return spline
    return None


def copy_spline(obj: Object, spline: Spline) -> Spline:
    """Copy the given spline. Clears the current selection and causes all points of the new spline to be seleted.
       Returns the newly-created spline."""
    bpy.ops.curve.select_all(action='DESELECT')
    select_points(spline)
    bpy.ops.curve.duplicate_move()
    new_spline = get_selected_spline(obj)
    return new_spline


def get_selected_points_info() -> list[tuple[Object, Spline, SplinePoint | BezierSplinePoint]]:
    """Get all selected points. Returns an (obj, spline, point) tuple"""

    def is_sel(p: SplinePoint | BezierSplinePoint) -> bool:
        for prop in sel_props:
            if getattr(p, prop):
                return True
        return False

    tuples = []
    for ob in bpy.context.selected_objects:
        if ob.type != "CURVE":
            print("Unsupported object type", ob)
            continue
        for spl in ob.data.splines:
            if spl.type not in ["BEZIER", "POLY"]:
                print("Unsupported spline type", spl)
                continue
            all_points = get_points_collection(spl)
            sel_props = ["select_control_point", "select_left_handle", "select_right_handle"] if spl.type == "BEZIER" else ["select"]
            tuples.extend([(ob, spl, pt) for pt in all_points if is_sel(pt)])
    return tuples


def get_points_collection(spline: Spline) -> list[SplinePoint | BezierSplinePoint]:
    """Get the points in the spline, regardless of whether they're Bezier or Poly"""
    if spline.type == "BEZIER":
        return list(spline.bezier_points)
    return list(spline.points)

def select_points(spline: Spline, indices: Iterable[int] = ()):
    sel_props = {
        "BEZIER": "select_control_point",
        "POLY": "select"
    }

    if spline.type not in sel_props:
        return

    sel_prop = sel_props[spline.type]
    coll = get_points_collection(spline)
    indices = indices if indices else range(len(coll))

    for idx in indices:
        setattr(coll[idx], sel_prop, True)


def split_on_point(obj: Object, spline: Spline, point: SplinePoint | BezierSplinePoint):
    """Split the given obj's given spline on the given point. Changes the selection to the split point."""
    points = spline.points if spline.points else spline.bezier_points
    split_index = [idx for idx, pt in enumerate(points) if pt == point][0]
    new_spline = copy_spline(obj, spline)
    bpy.ops.curve.select_all(action='DESELECT')

    point_count = len(spline.points if spline.points else spline.bezier_points)

    # Select split_index+1 to len-1 of old spline for deletion, leaving 0--split_index
    select_points(spline, range(split_index + 1, point_count))
    # Select 0--(split_index-1) of new spline for deletion, leaving split_index--end
    select_points(new_spline, range(split_index))

    bpy.ops.curve.delete(type="VERT")

    # Select the split_index on the old spline so the "same" point is selected once the operator completes.
    select_points(spline, [split_index])
