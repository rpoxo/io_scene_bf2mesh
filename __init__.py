

bl_info = {
    "name": "DICE Refractor2 mesh format",
    "author": "Gotsko Nikita",
    "blender": (2, 78, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Refractor2 .staticmesh, .bundledmesh, ...",
    "warning": "",
    "category": "Import-Export"}

if "bpy" in locals():
    import importlib
    #if "import_bf2mesh" in locals():
    #    importlib.reload(import_bf2mesh)
    if "export_bf2mesh" in locals():
        importlib.reload(export_bf2mesh)


import bpy
# remove many shit
from bpy.props import (
        #BoolProperty,
        #EnumProperty,
        #FloatProperty,
        StringProperty,
        )
from bpy_extras.io_utils import (
        #ImportHelper,
        ExportHelper,
        orientation_helper_factory,
        axis_conversion,
        )


IO3DSOrientationHelper = orientation_helper_factory("IO3DSOrientationHelper", axis_forward='Y', axis_up='Z')


class ExportBF2Mesh(bpy.types.Operator,
                    ExportHelper,
                    #IO3DSOrientationHelper):
                    ):
    """Export to Refractor2 mesh file format (.staticmesh)"""
    bl_idname = "export_scene.bf2_mesh"
    bl_label = 'Export'

    filename_ext = ".staticmesh"
    filter_glob = StringProperty(
            default="*.staticmesh", # displays existing
            options={'HIDDEN'},
            )

    def execute(self, context):
        from . import export_bf2mesh
        
        keywords = self.as_keywords(ignore=(#"axis_forward",
                                            #"axis_up",
                                            "filter_glob",
                                            "check_existing",
                                            ))

        return export_bf2mesh.save(self, context, **keywords) # do i even need context?


# Add to a menu
def menu_func_export(self, context):
    self.layout.operator(ExportBF2Mesh.bl_idname, text="DICE BF2Mesh (.staticmesh), (.bundledmesh), (.skinnedmesh), (.collisionmesh)")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
