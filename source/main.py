import pygame
from pygame import Vector2 # noqa: F401
from pygame import gfxdraw  # noqa: F401
import pygame_plus # noqa: F401
import solver # noqa: F401
from solver import Solver, Line, Ball, Polygon # noqa: F401
import math # noqa: F401
import multiprocessing # noqa: F401
from random import randint # noqa: F401
import sys

#USER VARIABLES
WINDOW_WIDTH = int(sys.argv[1])
WINDOW_HEIGHT = int(sys.argv[2])
FRAMERATE = 100

#Initialize PyGame
pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#Framerate clock
engine_clock = pygame.time.Clock()


#GENERAL VARIABLES
delta_time = 1/FRAMERATE #lock it to 1s divided between frames to help stability

#objects
grav_objects = [Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), 30, (255, 0, 0))]
# grav_objects = [Ball(display, WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100, 30), Line(display, WINDOW_WIDTH/3, WINDOW_HEIGHT/2, WINDOW_WIDTH/3*2, WINDOW_HEIGHT/2), Line(display, WINDOW_WIDTH/3+50, WINDOW_HEIGHT/2-1000, WINDOW_WIDTH/3+50, WINDOW_HEIGHT/2-100)]
# grav_objects = [Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100), 30), Line(display, Vector2(WINDOW_WIDTH/3, WINDOW_HEIGHT/2), Vector2(WINDOW_WIDTH/3*2, WINDOW_HEIGHT/2))]

# grav_objects = [Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100), 30), Line(display, Vector2(438.0, 260.0), Vector2(826.0, 649.0), anchored=False)]
# grav_objects =[Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100), 30), Line(display, Vector2(249.0, 426.0), Vector2(1011.0, 186.0), anchored=False)]
# grav_objects =[Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-100), 30), Polygon(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)), Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))]
# grav_objects = [Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+200), 10)]
grav_objects = [Polygon(display, Vector2(WINDOW_WIDTH/3, WINDOW_HEIGHT/3), radius=30, point_amount=3, anchored=False)]
grav_objects = [Ball(display, Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), 20)]
grav_objects = []

# no_grav_objects = [Line(display, 0, 0, 0, WINDOW_HEIGHT-1, anchored=True), Line(display, 0, WINDOW_HEIGHT-1, WINDOW_WIDTH-1, WINDOW_HEIGHT-1, anchored=True), Line(display, WINDOW_WIDTH-1, WINDOW_HEIGHT-1, WINDOW_WIDTH-1, 0, anchored=True), Line(display, 0, 0, WINDOW_WIDTH-1, 0, anchored=True)] BOX
no_grav_objects = [Ball(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100), anchored=True), Ball(display, Vector2(WINDOW_WIDTH/3, WINDOW_HEIGHT/2+100), anchored=True), Ball(display, Vector2(WINDOW_WIDTH/3*2, WINDOW_HEIGHT/2+100), anchored=True), Line(display, Vector2(Vector2(WINDOW_WIDTH/3-20, WINDOW_HEIGHT/4) - Vector2(WINDOW_WIDTH/3-20, WINDOW_HEIGHT/2*1.5)), [Vector2(WINDOW_WIDTH/3-20, WINDOW_HEIGHT/4), Vector2(WINDOW_WIDTH/3-20, WINDOW_HEIGHT/2*1.5)], anchored=True)]

not_mouse_objects = [Ball(display, Vector2(WINDOW_WIDTH/4, WINDOW_HEIGHT/4), 40, (85, 255, 85), True), Ball(display, Vector2(WINDOW_WIDTH/4, WINDOW_HEIGHT/4*3), 40, (85, 255, 85), True), Ball(display, Vector2(WINDOW_WIDTH/4*3, WINDOW_HEIGHT/4*3), 40, (85, 255, 85), True), Ball(display, Vector2(WINDOW_WIDTH/4*3, WINDOW_HEIGHT/4), 40, (85, 255, 85), True)]
# not_mouse_objects = [Line(display, Vector2(728.0, 959.0), Vector2(1366.0, 511.0), anchored=True)]
# not_mouse_objects = [Polygon(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), radius=50, point_amount=5, anchored=True)]
# not_mouse_objects = [Polygon(display, Vector2(WINDOW_WIDTH/3, WINDOW_HEIGHT/3), radius=30, point_amount=3, anchored=False), Polygon(display, Vector2(200, 200), radius=50, point_amount=5, anchored=True)]
not_mouse_objects = [Polygon(display, Vector2(150, 150), [Vector2(100, 100), Vector2(200, 100), Vector2(200, 200), Vector2(100, 200)], anchored=False, motor=0.1), Polygon(display, Vector2(350, 360), [Vector2(300, 400), Vector2(350, 300), Vector2(400, 400)], anchored=False)]
# not_mouse_objects = [Polygon(display, Vector2(150, 150), [Vector2(100, 100), Vector2(200, 100), Vector2(200, 200), Vector2(100, 200)], anchored=False)]
not_mouse_objects = [Polygon(display, Vector2(WINDOW_WIDTH//3, WINDOW_HEIGHT//2), radius=300, point_amount=4, anchored=True, motor=0.005), Polygon(display, Vector2(WINDOW_WIDTH//3*2, WINDOW_HEIGHT//2), radius=300, point_amount=4, anchored=True, motor=-0.005)]
# not_mouse_objects = [Polygon(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), [Vector2(1023, 10), Vector2(129, 123), Vector2(1202, 564), Vector2(654, 456)], anchored=True)]
# othergon = Polygon(display, Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2), radius=30, point_amount=3, anchored=False)

# not_mouse_objects = [Line(display, Vector2(646.0, 413.0), Vector2(660.0, 832.0), anchored=True)]
box = [Line(display, Vector2(1, WINDOW_HEIGHT//2), [Vector2(0, 0), Vector2(0, WINDOW_HEIGHT-2)], anchored=True), 
       Line(display, Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT-1), [Vector2(0, WINDOW_HEIGHT-1), Vector2(WINDOW_WIDTH-1, WINDOW_HEIGHT-1)], anchored=True), 
       Line(display, Vector2(WINDOW_WIDTH-1, WINDOW_HEIGHT//2), [Vector2(WINDOW_WIDTH-1, WINDOW_HEIGHT-1), Vector2(WINDOW_WIDTH-1, 0+1)], anchored=True), 
       Line(display, Vector2(WINDOW_WIDTH//2, 0), [Vector2(0, 0), Vector2(WINDOW_WIDTH-1, 0)], anchored=True)]
# box = [Ball(display, Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), 20)]
# box = []
#v2
# box = [Polygon(display, Vector2(0, WINDOW_HEIGHT//2), [Vector2(0, 1), Vector2(0, WINDOW_HEIGHT-2), Vector2(-2, WINDOW_HEIGHT-2), Vector2(-2, 1)], color=(255, 255, 255), anchored=True), 
#        Polygon(display, Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT), [Vector2(0, WINDOW_HEIGHT-1), Vector2(WINDOW_WIDTH, WINDOW_HEIGHT-1), Vector2(WINDOW_WIDTH, WINDOW_HEIGHT+1), Vector2(0, WINDOW_HEIGHT+1)], color=(255, 255, 255), anchored=True),
#        Polygon(display, Vector2(WINDOW_WIDTH, WINDOW_HEIGHT//2), [Vector2(WINDOW_WIDTH-1, WINDOW_HEIGHT-2), Vector2(WINDOW_WIDTH-1, 1), Vector2(WINDOW_WIDTH+1, 1), Vector2(WINDOW_WIDTH+1, WINDOW_HEIGHT-2)], color=(255, 255, 255), anchored=True),
#        Polygon(display, Vector2(WINDOW_WIDTH//2, -1), [Vector2(0, -2), Vector2(WINDOW_WIDTH, -2), Vector2(WINDOW_WIDTH, 0), Vector2(0, 0)], color=(255, 255, 255), anchored=True)
#        ]
not_mouse_objects = not_mouse_objects + box

invisible_physics_objects = [] #for invisible walls, etc
rendered_objects = [] #rendered but without collisions, gui maybe?

mouse_objects = []
temp_start = pygame.Vector2(0, 0)
temp_end = pygame.Vector2(0, 0)
drawing = False
perf_font = pygame.font.SysFont("Arial", 16)

phys_solver = Solver(grav_objects, no_grav_objects, gravity=1000)

follow_mouse = False

#Functions
def average_calculator(averages:list) -> float:
    average = 0
    for i in averages:
        average += i
    
    average /= len(averages)
    return average


def perf_render(surface: pygame.Surface, font:pygame.Font, performance_dict:list) -> None:
    collision_average = round(average_calculator(performance_dict["Collisions"])*8, 2)
    position_average = round(average_calculator(performance_dict["Position_Updates"])*8, 2)
    gjk_epa_average = round(average_calculator(performance_dict["GJK/EPA"]), 2)
    line_ball_average = round(average_calculator(performance_dict["Line/Ball"]), 2)
    ball_ball_average = round(average_calculator(performance_dict["Ball/Ball"]), 2)
    
    surface.blit(font.render(str("Collisions: ~" + str(collision_average)+"ms"), True, (0, 255, 0)), (0, 30))
    surface.blit(font.render(str("Position Updates: ~" + str(position_average)+"ms"), True, (0, 255, 0)), (0, 60))
    surface.blit(font.render(str("GJK/EPA: ~" + str(gjk_epa_average)+"ms"), True, (0, 255, 0)), (0, 90))
    surface.blit(font.render(str("Line/Ball: ~" + str(line_ball_average)+"ms"), True, (0, 255, 0)), (0, 120))
    surface.blit(font.render(str("Ball/Ball: ~" + str(ball_ball_average)+"ms"), True, (0, 255, 0)), (0, 150))


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
            mouse_objects.append(Line(display, Vector2(temp_start[0] - temp_end[0], temp_start[1] - temp_end[1]), [Vector2(temp_start[0], temp_start[1]), Vector2(temp_end[0], temp_end[1])], anchored=False))
            drawing = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: #Manuever "player"
                try:
                    grav_objects[0].position[1] -= .1
                except IndexError:
                    try:
                        not_mouse_objects[0].position[1] -=.1
                    except IndexError:
                        print("index Errror")
                        continue
                
            elif event.key == pygame.K_DOWN:
                try:
                    grav_objects[0].position[1] += .1
                except IndexError:
                    try:
                        not_mouse_objects[0].position[1] +=.1
                    except IndexError:
                        continue

            elif event.key == pygame.K_LEFT:
                try:
                    grav_objects[0].position[0] -= .1
                except IndexError:
                    try:
                        not_mouse_objects[0].position[0] -=.1
                    except IndexError:
                        continue

            elif event.key == pygame.K_RIGHT:
                try:
                    grav_objects[0].position[0] += .1
                except IndexError:
                    try:
                        not_mouse_objects[0].position[0] +=.1
                    except IndexError:
                        continue
            
            elif event.key == pygame.K_p: #print drawn objects for copying
                temp_list = []
                for line in mouse_objects:
                    if type(line) == Line:
                        temp_list.append(f"Line(display, Vector2({line.position[0]}, {line.position[1]}), [Vector2({line.points[0][0]}, {line.points[0][1]}), Vector2({line.points[1][0]}, {line.points[1][1]})], anchored={line.anchored})")
                print(temp_list)
                    
            elif event.key == pygame.K_1:
                mouse_pos = pygame.mouse.get_pos()
                grav_objects.append(Ball(display, Vector2(mouse_pos[0], mouse_pos[1]), 60))
            
            elif event.key == pygame.K_m:
                follow_mouse = not follow_mouse
                
        
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
        
    # othergon.draw_antialiased_wireframe()
    
    if follow_mouse:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = Vector2(mouse_pos[0], mouse_pos[1])
        not_mouse_objects[0].position = mouse_pos
        not_mouse_objects[0].last_position = mouse_pos
    
    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        mouse_vector = Vector2(mouse_pos[0], mouse_pos[1])
        gfxdraw.line(display, int(temp_start[0]), int(temp_start[1]), int(mouse_pos[0]), int(mouse_pos[1]), (165, 165, 165))
        # print(temp_start.angle_to(mouse_vector))
        # normals = [Vector2((-1*(mouse_vector[1] - temp_start[1]), (mouse_vector[0] - temp_start[0]))), Vector2(((mouse_vector[1] - temp_start[1]), -1*(mouse_vector[0] - temp_start[0])))]
        # gfxdraw.aacircle(display, int(normals[0][0]), int(normals[0][1]), 10, (255, 165, 0))
        # gfxdraw.aacircle(display, int(normals[1][0]), int(normals[1][1]), 10, (0, 165, 255))


    # print(f"POLYGON 1 |  X: {no_grav_objects[0].position[0]}, Y: {no_grav_objects[0].position[0]}.   |  POINTS:  {no_grav_objects[0].points}")
    # print(f"POLYGON 2 |  X: {grav_objects[0].position[0]}, Y: {grav_objects[0].position[0]}.   |  POINTS:  {grav_objects[0].points}")
    try:
        perf_render(display, perf_font, phys_solver.performance_analytics)
    except ZeroDivisionError:
        pass
    pygame.display.flip()
#EXIT PROGRAM
pygame.quit()
raise SystemExit #the same as sys.exit(), to avoid importing sys