import pygame
from pygame import gfxdraw  # noqa: F401
import pygame_plus # noqa: F401
import solver # noqa: F401
from solver import Solver, Ball, Line, Square, Triangle # noqa: F401
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
grav_objects = [Ball(display, WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 30), Line(display, WINDOW_WIDTH/3, WINDOW_HEIGHT/3, WINDOW_WIDTH/3*2, WINDOW_HEIGHT/3), Line(display, WINDOW_WIDTH/3-10, WINDOW_HEIGHT/3, WINDOW_WIDTH/3*2, WINDOW_HEIGHT/3)]
# no_grav_objects = [Line(display, 0, 0, 0, WINDOW_HEIGHT-1, anchored=True), Line(display, 0, WINDOW_HEIGHT-1, WINDOW_WIDTH-1, WINDOW_HEIGHT-1, anchored=True), Line(display, WINDOW_WIDTH-1, WINDOW_HEIGHT-1, WINDOW_WIDTH-1, 0, anchored=True), Line(display, 0, 0, WINDOW_WIDTH-1, 0, anchored=True)] BOX
no_grav_objects = [Ball(display, WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100, anchored=True), Ball(display, WINDOW_WIDTH/3, WINDOW_HEIGHT/2+100, anchored=True), Ball(display, WINDOW_WIDTH/3*2, WINDOW_HEIGHT/2+100, anchored=True), Line(display, WINDOW_WIDTH/3-20, WINDOW_HEIGHT/4, WINDOW_WIDTH/3-20, WINDOW_HEIGHT/2*1.5, anchored=True)]
invisible_physics_objects = [] #for invisible walls, etc
rendered_objects = [] #rendered but without collisions, gui maybe?

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                grav_objects[0].position[1] -= 1
                
            elif event.key == pygame.K_DOWN:
                grav_objects[0].position[1] += 1

            elif event.key == pygame.K_LEFT:
                grav_objects[0].position[0] -= 1

            elif event.key == pygame.K_RIGHT:
                grav_objects[0].position[0] += 1

    phys_solver.update(delta_time)


    #I should split these onto three other threads for better perf?
    for object in grav_objects:
        if object.draw_antialiased_wireframe():
            grav_objects.remove(object)
            del object
            continue
    
    for object in no_grav_objects:
        if object.draw_antialiased_wireframe():
            no_grav_objects.remove(object)
            del object
            continue

    for object in rendered_objects:
        if object.draw_antialiased_wireframe():
            rendered_objects.remove(object)
            del object
            continue

    pygame.display.flip()
#EXIT PROGRAM
pygame.quit()
raise SystemExit #the same as sys.exit(), to avoid importing sys