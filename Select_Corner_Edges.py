# Script by Georges Dahdouh
# Licence GPL 3.0
# This script assumes being used in Edit Mode, mesh object, at least 1 corner edge selected in and edge loop.
# Run this script in the script editor, then use F3 and search for select corner edges operator.
# Happy blending!

import bpy
import bmesh


def main(context):
    thresh = 0.01
    bpy.ops.object.mode_set(mode='OBJECT')

    mesh = bpy.context.object.data

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.loop_multi_select(ring=True)
    bpy.ops.object.mode_set(mode='OBJECT')

    bm = bmesh.new()
    bm.from_mesh(mesh)

    for e in bm.edges:
        if e.calc_face_angle() <= thresh:
            e.select = False
    
    bm.to_mesh(mesh)
    bm.free()
    bpy.ops.object.mode_set(mode='EDIT')


class SelectCornerEdges(bpy.types.Operator):
    """Tooltip"""
    bl_info = {"name": "Select Corner Edges", "category": "Object"}
    bl_idname = "object.select_corner_edges"
    bl_label = "Select Corner Edges"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SelectCornerEdges.bl_idname, text=SelectCornerEdges.bl_label)

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(SelectCornerEdges)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SelectCornerEdges)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

