import pygame
from pygame import gfxdraw
import pygame_plus
import solver
from solver import Solver, Ball, Plane, Square, Triangle 
import math
import multiprocessing



#USER VARIABLES
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FRAMERATE = 60

#Initialize PyGame
pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#Framerate clock
engine_clock = pygame.time.Clock()


#GENERAL VARIABLES
delta_time = 1/FRAMERATE #lock it to 1s divided between frames to help stability

#objects
grav_objects = [Ball(display, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)]
no_grav_objects = [Ball(display, WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100)]
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            grav_objects[0].position[1] -= 10

    phys_solver.update(delta_time)


    #I should split these onto three other threads for better perf
    for object in grav_objects:
        object.draw_antialiased_wireframe()

    for object in no_grav_objects:
        object.draw_antialiased_wireframe()

    for object in rendered_objects:
        object.draw_antialiased_wireframe()

    pygame.display.flip()
#EXIT PROGRAM
pygame.quit()
raise SystemExit #the same as sys.exit(), to avoid importing sys