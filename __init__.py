# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

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
    if "import_bf2mesh" in locals():
        importlib.reload(import_bf2mesh)
    if "export_bf2mesh" in locals():
        importlib.reload(export_bf2mesh)


import bpy
# remove
from bpy.props import (
        #BoolProperty,
        #EnumProperty,
        #FloatProperty,
        StringProperty,
        )
from bpy_extras.io_utils import (
        #ImportHelper,
        ExportHelper,
        #orientation_helper_factory,
        #axis_conversion,
        )


#IO3DSOrientationHelper = orientation_helper_factory("IO3DSOrientationHelper", axis_forward='Y', axis_up='Z')


class ExportBF2Mesh(bpy.types.Operator,
                    ExportHelper,
                    #IO3DSOrientationHelper):
                    ):
    """Export to Refractor2 mesh file format (.staticmesh)"""
    bl_idname = "export_scene.refractor2_mesh"
    bl_label = 'Export .staticmesh'

    filename_ext = "."
    filter_glob = StringProperty(
            default="*.staticmesh",
            options={'HIDDEN'},
            )

    def execute(self, context):
        from . import export_bf2mesh

        return export_bf2mesh.save(self, context, **keywords)


# Add to a menu
def menu_func_export(self, context):
    self.layout.operator(ExportBF2Mesh.bl_idname, text="Refractor2 staticmesh (.staticmesh)")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
