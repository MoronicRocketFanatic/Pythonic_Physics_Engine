import pygame
from pygame import Vector2 # noqa: F401
from pygame import gfxdraw  # noqa: F401
import pygame_plus # noqa: F401
import solver # noqa: F401
from solver import Solver, Line, Ball, Polygon # noqa: F401
import math # noqa: F401
import multiprocessing # noqa: F401
from random import randint # noqa: F401


#USER VARIABLES
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FRAMERATE = 100

#Initialize PyGame
pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#Framerate clock
engine_clock = pygame.time.Clock()


#GENERAL VARIABLES
delta_time = 1/FRAMERATE #lock it to 1s divided between frames to help stability

#objects
# grav_objects = [Ball(display, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)]
# grav_objects = [Ball(display, WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100, 30), Line(display, WINDOW_WIDTH/3, WINDOW_HEIGHT/2, WINDOW_WIDTH/3*2, WINDOW_HEIGHT/2), Line(display, WINDOW_WIDTH/3+50, WINDOW_HEIGHT/2-1000, WINDOW_WIDTH/3+50, WINDOW_HEIGHT/2-100)]
# grav_objects = [Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100), 30), Line(display, Vector2(WINDOW_WIDTH/3, WINDOW_HEIGHT/2), Vector2(WINDOW_WIDTH/3*2, WINDOW_HEIGHT/2))]

# grav_objects = [Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100), 30), Line(display, Vector2(438.0, 260.0), Vector2(826.0, 649.0), anchored=False)]
# grav_objects =[Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100), 30), Line(display, Vector2(249.0, 426.0), Vector2(1011.0, 186.0), anchored=False)]
# grav_objects =[Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100), 30), Polygon(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)), Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))]
# grav_objects = [Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+200), 10)]
grav_objects = []

# no_grav_objects = [Line(display, 0, 0, 0, WINDOW_HEIGHT-1, anchored=True), Line(display, 0, WINDOW_HEIGHT-1, WINDOW_WIDTH-1, WINDOW_HEIGHT-1, anchored=True), Line(display, WINDOW_WIDTH-1, WINDOW_HEIGHT-1, WINDOW_WIDTH-1, 0, anchored=True), Line(display, 0, 0, WINDOW_WIDTH-1, 0, anchored=True)] BOX
no_grav_objects = [Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100), anchored=True), Ball(display, Vector2(WINDOW_WIDTH/3, WINDOW_HEIGHT/2+100), anchored=True), Ball(display, Vector2(WINDOW_WIDTH/3*2, WINDOW_HEIGHT/2+100), anchored=True), Line(display, Vector2(WINDOW_WIDTH/3-20, WINDOW_HEIGHT/4), Vector2(WINDOW_WIDTH/3-20, WINDOW_HEIGHT/2*1.5), anchored=True)]

# not_mouse_objects = [Line(display, Vector2(728.0, 959.0), Vector2(1366.0, 511.0), anchored=True)]
not_mouse_objects = [Polygon(display, Vector2(WINDOW_WIDTH/2-400, WINDOW_HEIGHT/2), radius= 50, point_amount= 4, anchored=True), Polygon(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), radius= 30, point_amount= 3, anchored=True)]

# not_mouse_objects = [Line(display, Vector2(646.0, 413.0), Vector2(660.0, 832.0), anchored=True)]
box = [Line(display, Vector2(0, 0), Vector2(0, WINDOW_HEIGHT-2), anchored=True), Line(display, Vector2(0, WINDOW_HEIGHT-1), Vector2(WINDOW_WIDTH-1, WINDOW_HEIGHT-1), anchored=True), Line(display, Vector2(WINDOW_WIDTH-1, WINDOW_HEIGHT-1), Vector2(WINDOW_WIDTH-1, 0+1), anchored=True), Line(display, Vector2(0, 0), Vector2(WINDOW_WIDTH-1, 0), anchored=True)]
not_mouse_objects = not_mouse_objects + box

invisible_physics_objects = [] #for invisible walls, etc
rendered_objects = [] #rendered but without collisions, gui maybe?

mouse_objects = []
temp_start = pygame.Vector2(0, 0)
temp_end = pygame.Vector2(0, 0)
drawing = False

phys_solver = Solver(grav_objects, no_grav_objects, gravity=1000)


#Functions

#MAIN LOOP
engine_running = True
while engine_running:
    display.fill((0,0,0))
    engine_clock.tick(FRAMERATE)
    pygame.display.set_caption(f"Pythonic Physics Engine  |  Frames Per Second: {int(engine_clock.get_fps())}, Target FPS: {FRAMERATE}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            engine_running = False
            print("Attempting exit...")

        elif event.type == pygame.MOUSEBUTTONDOWN: #Draw start
            mouse_pos = pygame.mouse.get_pos()
            temp_start = pygame.Vector2(mouse_pos[0], mouse_pos[1])
            drawing = True
        
        elif event.type == pygame.MOUSEBUTTONUP: #Draw finish
            mouse_pos = pygame.mouse.get_pos()
            temp_end = pygame.Vector2(mouse_pos[0], mouse_pos[1])
            mouse_objects.append(Line(display, Vector2(temp_start[0], temp_start[1]), Vector2(temp_end[0], temp_end[1]), anchored=False))
            drawing = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: #Manuever "player"
                # grav_objects[0].position[1] -= 1
                not_mouse_objects[0].position[1] -=.25
                
            elif event.key == pygame.K_DOWN:
                # grav_objects[0].position[1] += 1
                not_mouse_objects[0].position[1] +=.25

            elif event.key == pygame.K_LEFT:
                # grav_objects[0].position[0] -= 1
                not_mouse_objects[0].position[0] -=.25

            elif event.key == pygame.K_RIGHT:
                # grav_objects[0].position[0] += 1
                not_mouse_objects[0].position[0] +=.25
            
            elif event.key == pygame.K_p: #print drawn objects for copying
                temp_list = []
                for line in mouse_objects:
                    if type(line) == Line:
                        temp_list.append(f"Line(display, Vector2({line.position[0]}, {line.position[1]}), Vector2({line.position_2[0]}, {line.position_2[1]}), anchored={line.anchored})")
                print(temp_list)
                    
            elif event.key == pygame.K_1:
                mouse_pos = pygame.mouse.get_pos()
                mouse_objects.append(Ball(display, Vector2(mouse_pos[0], mouse_pos[1]), 20))
                
        
    no_grav_objects = not_mouse_objects + mouse_objects + invisible_physics_objects
    phys_solver.no_grav_objects = no_grav_objects
    phys_solver.update(delta_time)


    #I should split these onto three other threads for better perf?
    for object in grav_objects:
        object.draw_antialiased_wireframe()
    
    for object in no_grav_objects:
        object.draw_antialiased_wireframe()

    for object in rendered_objects:
        object.draw_antialiased_wireframe()
        
    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        mouse_vector = Vector2(mouse_pos[0], mouse_pos[1])
        gfxdraw.line(display, int(temp_start[0]), int(temp_start[1]), int(mouse_pos[0]), int(mouse_pos[1]), (165, 165, 165))
        print(temp_start.angle_to(mouse_vector))
        normals = [Vector2((-1*(mouse_vector[1] - temp_start[1]), (mouse_vector[0] - temp_start[0]))), Vector2(((mouse_vector[1] - temp_start[1]), -1*(mouse_vector[0] - temp_start[0])))]
        gfxdraw.aacircle(display, int(normals[0][0]), int(normals[0][1]), 10, (255, 165, 0))
        gfxdraw.aacircle(display, int(normals[1][0]), int(normals[1][1]), 10, (0, 165, 255))

    pygame.display.flip()
#EXIT PROGRAM
pygame.quit()
raise SystemExit #the same as sys.exit(), to avoid importing sys