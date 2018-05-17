import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
    polygons = []
    edges = []

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
        print commands
        for x in commands:
            line = x[0]
            if line == 'push':
                stack.append( [x[:] for x in stack[-1]] )
                
            elif line == 'pop':
                stack.pop()

            elif line == 'display':
                display(screen)

            elif line == 'save':
                save_extension(screen, x[1] + x[2]) 

            elif line == 'move':
                t = make_translate(float(x[1]), float(x[2]), float(x[3]))
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]

            elif line == 'rotate':
                theta = float(x[2]) * (math.pi / 180)
                if x[1] == 'x':
                    t = make_rotX(theta)
                elif x[1]  == 'y':
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]                

            elif line == 'scale':
                t = make_scale(float(x[1]), float(x[2]), float(x[3]))
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]
                
            elif line == 'box':
                add_box(polygons,
                        float(x[1]), float(x[2]), float(x[3]),
                        float(x[4]), float(x[5]), float(x[6]))
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
                
            elif line == 'sphere':
                add_sphere(polygons,
                       float(x[1]), float(x[2]), float(x[3]),
                       float(x[4]), step_3d)
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
                
            elif line == 'torus':
                add_torus(polygons,
                      float(x[1]), float(x[2]), float(x[3]),
                      float(x[4]), float(x[5]), step_3d)
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
                
            elif line == 'line':
                add_edge( edges,
                      float(x[1]), float(x[2]), float(x[3]),
                      float(x[4]), float(x[5]), float(x[6]) )
                matrix_mult( stack[-1], edges )
                draw_lines(edges, screen, zbuffer, color)
                edges = []

            else:
                print "Parsing failed."
                return
