from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         sphere: add a sphere to the edge matrix - 
	    takes 4 arguemnts (cx, cy, cz, r)
         torus: add a torus to the edge matrix - 
	    takes 5 arguemnts (cx, cy, cz, r1, r2)
         box: add a rectangular prism to the edge matrix - 
	    takes 6 arguemnts (x, y, z, width, height, depth)	    
	 circle: add a circle to the edge matrix - 
	    takes 3 arguments (cx, cy, r)
	 hermite: add a hermite curve to the edge matrix -
	    takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
	 bezier: add a bezier curve to the edge matrix -
	    takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)
         line: add a line to the edge matrix - 
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix - 
	 scale: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 move: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
         clear: clear the edge matrix of points
	 apply: apply the current transformation matrix to the 
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing
See the file script for an example of the file format
"""
ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus','color' ]

def parse_file( fname, edges, transform, screen, color ):

    f = open(fname)
    lines = f.readlines()

    shape = new_matrix()
    ident(shape)
    stack = [shape]

    step = 0.1
    c = 0
    while c < len(lines):
        line = lines[c].strip()
#        print ':' + line + ':'

        #print str(stack[-1])

        if line in ARG_COMMANDS:            
            c+= 1
            args = lines[c].strip().split(' ')
            #print 'args\t' + str(args)
        
        if line == 'push':
            print "PUSH"
            shape = stack[len(stack)-1]
            foo = new_matrix()
            ident(foo)
            matrix_mult(shape ,foo)
            stack.append(foo)

        elif line == 'pop':
            print "POP"
            stack.pop()
        if line == 'sphere':
            print 'SPHERE\t' + str(args)
            shape = []
            add_sphere(shape,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step, color)
            #print str(temp_poly)
            matrix_mult(stack[len(stack)-1] ,shape)
            draw_polygons(shape, screen, color)
            
        elif line == 'torus':
            print 'TORUS\t' + str(args)
            shape = []
            add_torus(shape,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step, color)
            matrix_mult(stack[len(stack)-1] ,shape)
            draw_polygons(shape, screen, color)

        elif line == 'box':
            print 'BOX\t' + str(args)
            shape = []
            add_box(shape, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(stack[-1] ,shape)
            draw_polygons(shape, screen, color)
        elif line == 'circle':
            #print 'CIRCLE\t' + str(args)
            shape = []
            add_circle(shape, float(args[0]), float(args[1]), float(args[2]), float(args[3]), step)
            matrix_mult(stack[-1] ,shape)
            draw_lines(shape, screen,color)
        elif line == 'hermite' or line == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            shape = []
            add_curve(shape, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), step, line)            
            matrix_mult(stack[-1] ,shape)          
            draw_lines(shape, screen,color)
        elif line == 'line':            
            #print 'LINE\t' + str(args)
            shape = []
            add_edge( shape, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(stack[-1] ,shape)
            draw_lines(shape, screen,color)
        elif line == 'scale':
            print 'SCALE\t' + str(args)
            scale = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[len(stack)-1], scale)
            stack[-1] = scale
        elif line == 'move':
            print 'MOVE\t' + str(args)
            translate = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[len(stack)-1], translate)
            stack[-1] = translate
        elif line == 'rotate':
            print 'ROTATE\t' + str(args)
            angle = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                rotation = make_rotX(angle)
            elif args[0] == 'y':
                rotation = make_rotY(angle)
            else:
                rotation = make_rotZ(angle)
            matrix_mult(stack[len(stack)-1], rotation)
            stack[-1] = rotation
        elif line == 'clear':
            edges = []
        elif line == "color":
            color = [args[0],args[1],args[2]]
        elif line == 'ident':
            ident(transform)
        elif line == 'apply':
            matrix_mult( transform, edges )
        elif line == 'display' or line == 'save':
            #clear_screen(screen)
            #draw_polygons(edges, screen, color)
            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
        c+= 1
