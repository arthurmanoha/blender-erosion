import bpy
import random
import bmesh

# infos erosion   
# https://youtu.be/eaXk97ujbPQ

print("---------------------------------------------------------------")

x = random.random()
terrain = bpy.data.objects["Plane"]
mesh = terrain.data
bm = None



# TODO V2: add data structure to store each vertex's neighbors


def get_neighbors(vertex_index):
    print("get_neighbors(" + str(vertex_index) + ")")
    
    result = []
           
    #for v in bm.verts:
    v = bm.verts[vertex_index]
    for e in v.link_edges:
        v_other = e.other_vert(v)
        #print("%d -> %d via edge %d" % (v.index, v_other.index, e.index))
        result.append(v_other)
    return result

# A border vertex has fewer than 4 neighbors.
def is_border(neighbors):
    return len(neighbors) < 4


# Find and return vertex with lower z-coordinate
def find_lowest_vertex(list):
    
    lowest_alt = 1000
    lowest_vertex = None
    for v in list:
        # print("     v:" + str(v))
        # print("     v index:" + str(v.index))
        current_index = v.index
        current_vertex = bm.verts[current_index]
        
        # print("co: " + str(bm.verts[current_index].co))
        current_alt = bm.verts[current_index].co[2]
        # print("alt: " + str(current_alt))
        
        if current_alt < lowest_alt:
            lowest_alt = current_alt
            lowest_vertex = v
            
    return v

def is_too_flat(vertex, neighbors):
    return False

def take_dirt_from_vertex(vertex):
    return 0

def drop_sediment(percentage):
    dropped_amount = percentage
    
def erode_one_drop():
    
    # Material carried by the current drop
    accumulated_dirt = 0

    # Choose a random vertex
    print("")
    print("Choosing a random vertex")
    print("")
    nb_vertices = len(mesh.vertices)
    vertex_index = random.randint(0, nb_vertices-1)
    current_vertex = bm.verts[vertex_index]
    print("vertex_index: " + str(vertex_index))
    #print("current_vertex: " + str(current_vertex))
    

    keep_looping = True
    while(keep_looping):
        
        print("LOOP")
        print("selecting vertex index " + str(vertex_index) + ", alt: " + str(current_vertex.co[2]))
        #print("current_vertex: " + str(current_vertex))
        neighbors = get_neighbors(vertex_index)
        if is_border(neighbors) or is_too_flat(current_vertex, neighbors):
            # drop all sediment
            drop_sediment(1.0)
            keep_looping = False
            if is_border(neighbors):
                print("reached border.")
            else:
                print("reached flat area")
        else:
            lowest_neighbor = find_lowest_vertex(neighbors)
            direction = lowest_neighbor.co - current_vertex.co
            accumulated_dirt += take_dirt_from_vertex(current_vertex)
            ## Move to neighbor
            vertex_index = lowest_neighbor.index
            current_vertex = lowest_neighbor
        

current_mode = bpy.context.object.mode 
if current_mode == 'OBJECT':
    print("Must be in edit mode")
else:
    bm = bmesh.from_edit_mesh(mesh)
    erode_one_drop()
print("End.")