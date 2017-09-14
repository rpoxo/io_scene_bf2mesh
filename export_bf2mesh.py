import bpy
from . import modmesh

class BF2StaticMesh:

    def __init__(self):
        self.vmesh = modmesh.StdMesh()
        self._create_header(self.vmesh)
        self._create_u1_bfp4f_version(self.vmesh)
        self._create_geomtable(self.vmesh)
        self._create_vertattrib_table(self.vmesh)
        self._create_vertices(self.vmesh)
        self._create_indices(self.vmesh)
        self._create_u2(self.vmesh)
        self._create_nodes(self.vmesh)
        self._create_materials(self.vmesh)
        

    def _create_header(self, vmesh):
        vmesh.head = modmesh.bf2head()
        vmesh.head.u1 = 0
        vmesh.head.version = 11
        vmesh.head.u3 = 0
        vmesh.head.u4 = 0
        vmesh.head.u5 = 0

    def _create_u1_bfp4f_version(self, vmesh):
        vmesh.u1 = 0

    def _create_geomtable(self, vmesh):
        vmesh.geomnum = 1
        vmesh.geoms = [modmesh.bf2geom() for i in range(vmesh.geomnum)]
        vmesh.geoms[0].lodnum = 1
        for geom in vmesh.geoms:
            for i in range(geom.lodnum):
                geom.lods = [modmesh.bf2lod() for i in range(geom.lodnum)]

    def _create_vertattrib_table(self, vmesh):
        attrib_array = [
            (0, 0, 2, 0), # flag:used, offset=0, float3, position
            (0, 12, 2, 3), # flag:used, offset=12\4, float3, normal
            (0, 24, 4, 2), # flag:used, offset=24\4, d3dcolor, blend indice
            (0, 28, 1, 5), # flag:used, offset=28\4, float2, uv1
            (0, 32, 2, 6), # flag:used, offset=0, float3, tangent
            #(255, 0, 17, 0), # flag:unused, offset=0, unused, position
            ]

        vmesh.vertattribnum = len(attrib_array)
        vmesh.vertattrib = [modmesh.vertattrib() for i in range(vmesh.vertattribnum)]
        for i in range(vmesh.vertattribnum):
            vmesh.vertattrib[i].flag = attrib_array[i][0]
            vmesh.vertattrib[i].offset = attrib_array[i][1]
            vmesh.vertattrib[i].vartype = attrib_array[i][2]
            vmesh.vertattrib[i].usage = attrib_array[i][3]
            #print('{}: \n{}'.format(i, vmesh.vertattrib[i]))
        
        vmesh.vertformat = 4
        vmesh.vertstride = sum([modmesh.BIN.d3dtypes_lenght[attrib.vartype]*vmesh.vertformat for attrib in vmesh.vertattrib])

    def _create_vertices(self, vmesh):
        vmesh.vertices = tuple(())
        vmesh.vertnum = len(vmesh.vertices)
    
    def _create_indices(self, vmesh):
        vmesh.index = ()
        vmesh.indexnum = len(vmesh.index)

    def _create_u2(self, vmesh):
        vmesh.u2 = 8
    
    def _create_nodes(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.version = 11
                lod.min = (-1.0, -1.0, -1.0)
                lod.max = (1.0, 1.0, 1.0)
                #lod.pivot = None # already assigned to None for new modmesh
                lod.nodenum = 1
                lod.nodes = [
                    1.0, 0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0, 0.0,
                    0.0, 0.0, 1.0, 0.0,
                    0.0, 0.0, 0.0, 1.0] # no idea what is this shit in matrix4 ?
                lod.polycount = 0
                
    def _create_materials(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.matnum = 1
                lod.materials = [modmesh.bf2mat() for i in range(lod.matnum)]
                for material in lod.materials:
                    material.alphamode = 0
                    material.fxfile = b'StaticMesh.fx'
                    material.technique = b'Base'
                    material.mapnum = 1
                    material.maps = []
                    for i in range(material.mapnum):
                        material.maps.insert(i, b'readme/assets/apps/python3/mesher/tests/samples/evil_box/textures/evil_box_c.dds')
                    material.vstart = 0
                    material.istart = 0
                    material.inum = 36
                    material.vnum = 24
                    material.u4 = 0
                    material.u5 = 0
                    material.nmin = (-1.0, -1.0, -1.0)
                    material.nmax = (1.0, 1.0, 1.0)
                    lod.polycount = lod.polycount + material.inum / 3

    def write_vertices(self, vertices):
        self.vmesh.vertices = tuple(vertices)
        self.vmesh.vertnum = int(len(self.vmesh.vertices) / int(self.vmesh.vertstride / self.vmesh.vertformat))
        #self.vmesh.vertnum = 24 # box
    
    def write_indices(self, indices):
        self.vmesh.index = tuple(indices)
        self.vmesh.indexnum = len(self.vmesh.index)


class BF2VertexObject:

    def __init__(self, bpy_vert):
        self.bpy_vert = bpy_vert
        self.position = bpy_vert.co
        self.normal = None
        self.blend_index = (0.0)
        self.uv0 = None
        self.tangent = None


def export_index_data(bf2object):
    indices = []
    for id_face, face in enumerate(bf2object.data.polygons):
        # triangulating face for indexing
        triorder = [2, 1, 0, 0, 3, 2]
        for id_vertex in triorder:
            index = id_face * 4 + id_vertex
            indices.append(index)
    return indices

def export_vertex_data(bf2object):
    vertices = []
    for id_face, face in enumerate(bf2object.data.polygons):
        for id_vertex, id_loop in zip(face.vertices, face.loop_indices):
            bf2vertex = BF2VertexObject(bf2object.data.vertices[id_vertex])
            bf2vertex.normal = face.normal
            bf2vertex.uv0 = bf2object.data.uv_layers[0].data[id_loop].uv
            bf2vertex.tangent = bf2object.data.loops[id_loop].tangent

            vertices.append(bf2vertex)
    
    vertarray = []
    for vertex in vertices:
        for data in vertex.position:
            vertarray.append(round(data, 1))
        for data in vertex.normal:
            vertarray.append(round(data, 1))
        vertarray.append(vertex.blend_index)
        for data in vertex.uv0:
            vertarray.append(data)
        for data in vertex.tangent:
            vertarray.append(data)
    return vertarray


def save(operator,
         context, filepath="",
         use_selection=True,
         global_matrix=None,
         ):
    bf2mesh = BF2StaticMesh()

    for object in bpy.data.objects:
        if object.name.startswith('root_'):
            for geom in object.children:
                for lod in geom.children:
                    for bf2object in lod.children:
                        vertices = export_vertex_data(bf2object)
                        indices = export_index_data(bf2object)
                        bf2mesh.write_vertices(vertices)
                        bf2mesh.write_indices(reversed(indices)) # bf2 need reverted order
    
    print('Exporting to {}'.format(filepath))
    bf2mesh.vmesh.save(filepath)
    return {'FINISHED'}










