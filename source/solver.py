import pygame
from pygame import Vector2
from pygame import gfxdraw
import pygame_plus
import math


class PhysicsObject():
    """Main branch for physics objects to specialize off into."""

    def __init__(self, surface:pygame.Surface, x:int = 0, y:int = 0, color:pygame.Color = (200, 200, 200), rotation:int = 0, rotation_center:Vector2 = Vector2(0,0), permanent_rotation:int = 0) -> None:
        self.surface = surface

        self.x = x
        self.y = y
        self.position = Vector2(x, y)
        self.last_position = Vector2(x, y)
        self.rotation = rotation
        self.rotation_center = rotation_center
        self.permanent_rotation = permanent_rotation

        self.color = color
        self.acceleration = Vector2(0,0)


    def update_position(self, delta_time: float) -> None:

        self.displacement = self.position - self.last_position

        self.last_position = self.position

        self.position = self.position + self.displacement + self.acceleration * (delta_time*delta_time) #position = position + displacement + acceleration * (delta_time * delta_time)
        
        self.acceleration = Vector2(0, 0)



    def accelerate(self, acceleration:Vector2) -> None:
        """Use to accelerate an object"""
        self.acceleration += acceleration



class Ball(PhysicsObject):
    """And he said, "let there be balls!" and there was balls. The simplest and easiest to compute."""

    def __init__(self, surface: pygame.Surface, x: int = 0, y: int = 0, radius:float = 10, color: pygame.Color = (200, 200, 200), rotation: int = 0, rotation_center: Vector2 = Vector2(0, 0)) -> None:
        super().__init__(surface, x, y, color, rotation, rotation_center, 0)

        self.radius = radius
        self.render = pygame_plus.Circle(self.x, self.y, self.radius, self.surface, self.color, self.rotation)


    def draw_antialiased_wireframe(self):
        self.render.update(self.position[0], self.position[1], self.radius)
        self.render.color = self.color
        self.render.draw_antialiased_wireframe()

    
    



class Plane(PhysicsObject):
    """Lines of..."""

    def __init__(self, surface: pygame.Surface, x: int = 0, y: int = 0, color: pygame.Color = (200, 200, 200), rotation: int = 0, rotation_center: Vector2 = Vector2(0, 0), permanent_rotation: int = 0) -> None:
        super().__init__(surface, x, y, color, rotation, rotation_center, permanent_rotation)



class Square(PhysicsObject):
    pass



class Triangle(PhysicsObject):
    pass






class Solver():
    """The brain behind the physics engine."""

    def __init__(self, grav_objects:list[PhysicsObject], no_grav_objects:list[PhysicsObject], subsets:int = 2, gravity:float = 1000) -> None:
        """Here we go"""
        self.gravity = gravity
        self.grav_objects = grav_objects
        self.no_grav_objects = no_grav_objects #we need to save as much perf as possible
        self.all_objects = self.grav_objects + self.no_grav_objects
        self.subsets = subsets
        
        self.time_elapsed = 0

    
    def update(self, delta_time:float) -> None:
        self.time_elapsed += delta_time
        subset_delta_time = delta_time/self.subsets #we need to distribute time accordingly so that time isn't screwed up
        self.all_objects = self.grav_objects + self.no_grav_objects #we need to constantly update this to account for all sorts of changes
        subset_grav = self.gravity/self.subsets #

        for subset in range(self.subsets): #surely there's a better way?
            self.apply_gravity(subset_grav)
            self.solve_collisions()
            self.update_positions(subset_delta_time)


    
    def update_positions(self, delta_time:float):
        for object in self.all_objects:
            object.update_position(delta_time)


    def apply_gravity(self, subset_grav):
        """Applies the gravity to all specified gravity objects."""
        for object in self.grav_objects:
            object.accelerate(Vector2(0, subset_grav))


    def solve_collisions(self):
        for object_1 in self.all_objects:
            object_1_type = type(object_1)

            for object_2 in self.all_objects: #we improve this via multithreading (split the loop into 4 for 4 seperate threads to work on) and we need a better algorithm
                
                if object_1 == object_2:
                    continue
                
                object_2_type = type(object_2)

                if (object_1_type == Ball) and (object_2_type == Ball):
                    self.ball_on_ball(object_1, object_2)
                    continue


                if ((object_1_type == Plane) and (object_2_type == Ball)) or ((object_1_type == Ball) and (object_2_type == Plane)):
                    if (object_1_type == Plane) and (object_2_type == Ball):
                        self.line_on_ball(object_1, object_2)
                    else:
                        self.line_on_ball(object_2, object_1)



    
    def ball_on_ball(self, ball_1:Ball, ball_2:Ball):
        collision_axis = ball_1.position - ball_2.position
        distance = collision_axis.length()
        if distance < ball_1.radius + ball_2.radius:
            try:
                n = collision_axis / distance
            except ZeroDivisionError:
                n = Vector2()
            delta = ball_1.radius + ball_2.radius - distance
            ball_1.position += 0.5 * delta * n
            ball_2.position -= 0.5 * delta * n


    
    def line_on_ball(self, line, ball):
        line_x1 = line.position[0]
        line_y1 = line.position[1]
        line_x2 = line.position2[0]
        line_y2 = line.position2[1]