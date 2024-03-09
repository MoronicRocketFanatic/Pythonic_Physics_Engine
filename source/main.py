import pygame
from pygame import gfxdraw
import pygame_plus
import solver
import math



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
physics_objects = [pygame_plus.Box()]
invisible_physics_objects = [] #for invisible walls, etc
rendered_objects = [] #rendered but without collisions, gui maybe?


#Functions





#MAIN LOOP
engine_running = True
while engine_running:
    display.fill(0,0,0)
    engine_clock.tick(FRAMERATE)
    pygame.display.set_caption(f"Pythonic Physics Engine  |  Frames Per Second: {int(engine_clock.get_fps())}, Target FPS: {FRAMERATE}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            engine_running = False
            print("Attempting exit...")



    for object in physics_objects:
        object.draw_antialiased_wireframe(display)
    
    pygame.display.flip()
#EXIT PROGRAM
pygame.quit()
raise SystemExit #the same as sys.exit(), to avoid importing sys