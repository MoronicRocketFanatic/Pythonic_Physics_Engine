import pygame
from pygame import Vector2
from pygame import gfxdraw
import pygame_plus  # noqa: F401
import math


class PhysicsObject():
    """Main branch for physics objects to specialize off into."""

    def __init__(self, surface:pygame.Surface, x:int = 0, y:int = 0, color:pygame.Color = (200, 200, 200), rotation:int = 0, rotation_center:Vector2 = Vector2(0,0), permanent_rotation:int = 0, anchored:bool = False) -> None:
        """_summary_

        Args:
            surface (pygame.Surface): _description_
            x (int, optional): _description_. Defaults to 0.
            y (int, optional): _description_. Defaults to 0.
            color (pygame.Color, optional): _description_. Defaults to (200, 200, 200).
            rotation (int, optional): _description_. Defaults to 0.
            rotation_center (Vector2, optional): _description_. Defaults to Vector2(0,0).
            permanent_rotation (int, optional): _description_. Defaults to 0.
            anchored (bool, optional): _description_. Defaults to False.
        """        
        self.surface = surface

        self.position = Vector2(x, y)
        self.last_position = Vector2(x, y)
        self.rotation = rotation
        self.rotation_center = rotation_center
        self.permanent_rotation = permanent_rotation
        self.anchored = anchored

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

    def __init__(self, surface: pygame.Surface, x: int = 0, y: int = 0, radius:float = 10, color: pygame.Color = (200, 200, 200), rotation: int = 0, rotation_center: Vector2 = Vector2(0, 0), anchored:bool = False) -> None:
        super().__init__(surface, x, y, color, rotation, rotation_center, 0, anchored)

        self.radius = radius
        # self.render = pygame_plus.Circle(self.x, self.y, self.radius, self.surface, self.color, self.rotation)


    def draw_antialiased_wireframe(self) -> bool:
        try:
            gfxdraw.aacircle(self.surface, int(self.position[0]), int(self.position[1]), self.radius, self.color)
        except OverflowError:
            print(f"OBJECT KILLED: {self}")
            return True
        # self.render.update(self.position[0], self.position[1], self.radius)
        # self.render.color = self.color
        # self.render.draw_antialiased_wireframe()

    
    



class Line(PhysicsObject):
    """Lines of..."""

    def __init__(self, surface: pygame.Surface, x: int = 0, y: int = 0, x_2: int = 0, y_2: int = 0, color: pygame.Color = (200, 200, 200), rotation: int = 0, rotation_center: Vector2 = Vector2(0, 0), permanent_rotation: int = 0, anchored: bool = False) -> None:
        """The x_2 and y_2 are for the second point of the line because lazy"""
        super().__init__(surface, x, y, color, rotation, rotation_center, permanent_rotation, anchored)
        self.position_2 = Vector2(x_2, y_2)
        self.last_position_2 = Vector2(x_2, y_2)


    def update_position(self, delta_time: float) -> None:
        self.displacement_2 = self.position_2 - self.last_position_2

        self.last_position_2 = self.position_2

        self.position_2 = self.position_2 + self.displacement_2 + self.acceleration * (delta_time*delta_time) #position = position + displacement + acceleration * (delta_time * delta_time)
        
        super().update_position(delta_time)
    

    def draw_antialiased_wireframe(self) -> bool:
        try:
            gfxdraw.line(self.surface, int(self.position[0]), int(self.position[1]), int(self.position_2[0]), int(self.position_2[1]), self.color)
        
        except OverflowError:
            print(f"OBJECT KILLED: {self}")
            return True



class Square(PhysicsObject):
    pass



class Triangle(PhysicsObject):
    pass






class Solver():
    """The brain behind the physics engine."""

    def __init__(self, grav_objects:list[PhysicsObject], no_grav_objects:list[PhysicsObject], subsets:int = 8, gravity:float = 1000) -> None:
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
        # subset_grav = self.gravity/self.subsets #Kinda useless from what it seems

        for subset in range(self.subsets): #surely there's a better way?
            self.apply_gravity(self.gravity)
            self.solve_collisions()
            self.update_positions(subset_delta_time)


    
    def update_positions(self, delta_time:float) -> None:
        for object in self.all_objects:
            object.update_position(delta_time)


    def apply_gravity(self, gravity) -> None:
        """Applies the gravity to all specified gravity objects."""
        for object in self.grav_objects:
            object.accelerate(Vector2(0, gravity))


    def solve_collisions(self) -> None:
        for object_1 in self.all_objects:
            object_1_type = type(object_1)

            for object_2 in self.all_objects: #we improve this via multithreading (split the loop into 4 for 4 seperate threads to work on) and we need a better algorithm
                
                if object_1 == object_2:
                    continue
                
                object_2_type = type(object_2)

                if (object_1_type == Ball) and (object_2_type == Ball):
                    self.ball_on_ball(object_1, object_2)
                    continue

                elif ((object_1_type == Line) and (object_2_type == Ball)) or ((object_1_type == Ball) and (object_2_type == Line)):
                    if (object_1_type == Line) and (object_2_type == Ball):
                        self.line_on_ball(object_1, object_2)
                        continue
                    else:
                        self.line_on_ball(object_2, object_1)
                        continue
                        
                elif (object_1_type == Line) and (object_2_type == Line):
                    self.line_on_line(object_1, object_2)
                    continue



    
    def ball_on_ball(self, ball_1:Ball, ball_2:Ball) -> bool:
        collision_axis = ball_1.position - ball_2.position
        distance = collision_axis.length()
        if distance < ball_1.radius + ball_2.radius:
            try:
                n = collision_axis / distance
            except ZeroDivisionError:
                n = Vector2()
            delta = ball_1.radius + ball_2.radius - distance
            ball_1.position += (0.5 * delta * n) * (not ball_1.anchored)
            ball_2.position -= (0.5 * delta * n) * (not ball_2.anchored)
            return True


    def line_on_point(self, line: Line, point: Vector2) -> bool:
        line_length = math.dist(line.position, line.position_2)
        distance_1 = math.dist(point, line.position)
        distance_2 = math.dist(point, line.position_2)

        buffer = 0.1

        if ((distance_1 + distance_2) >= (line_length - buffer)) and ((distance_1 + distance_2) >= (line_length + buffer)):
            return True

    
    def line_on_ball(self, line: Line, ball: Ball) -> bool:
        
        collision_axis = line.position - ball.position
        collision_axis_2 = line.position_2 - ball.position

        distance = collision_axis.length()
        distance_2 = collision_axis_2.length()

        if (distance < ball.radius):
            try:
                n = collision_axis / distance
            except ZeroDivisionError:
                n = Vector2()
            delta = ball.radius - distance
            line.position += (0.5 * delta * n) * (not line.anchored)
            line.position_2 += (0.5 * delta * n) * (not line.anchored)
            ball.position -= (0.5 * delta * n) * (not ball.anchored)
            return True

        elif (distance_2 < ball.radius):
            try:
                n = collision_axis_2 / distance_2
            except ZeroDivisionError:
                n = Vector2()
            delta = ball.radius - distance_2
            line.position += (0.5 * delta * n) * (not line.anchored)
            line.position_2 += (0.5 * delta * n) * (not line.anchored)
            ball.position -= (0.5 * delta * n) * (not ball.anchored)
            return True

        # line_x_distance = line.position[0] - line.position_2[0]
        # line_y_distance = line.position[1] - line.position_2[1]
        line_length = math.dist(line.position, line.position_2)
        dot_product = (((ball.position[0] - line.position[0]) * (line.position_2[0] - line.position[0])) + ((ball.position[1] - line.position[1]) * (line.position_2[1] - line.position[1]))) / math.pow(line_length, 2)
        closest_x = line.position[0] + (dot_product * (line.position_2[0] - line.position[0]))
        closest_y = line.position[1] + (dot_product * (line.position_2[1] - line.position[1]))
        
        segment_collision = self.line_on_point(line, Vector2(closest_x, closest_y))
        if segment_collision:
            return False
        ball_x_distance = closest_x - ball.position[0]
        ball_y_distance = closest_y - ball.position[1]
        ball_distance = math.sqrt((ball_x_distance * ball_x_distance) + (ball_y_distance * ball_y_distance))

        if ball_distance <= ball.radius:
            ball_collision_axis = Vector2(closest_x, closest_y) - ball.position
            try:
                n = ball_collision_axis / ball_distance
            except ZeroDivisionError:
                n = Vector2()
            delta = ball.radius - ball_distance
            line.position += (0.5 * delta * n) * (not line.anchored)
            line.position_2 += (0.5 * delta * n) * (not line.anchored)
            ball.position -= (0.5 * delta * n) * (not ball.anchored)
            return True

        return False

    
    def line_on_line(self, line_1: Line, line_2: Line) -> bool:
        x_1 = line_1.position[0]
        x_2 = line_1.position_2[0]
        y_1 = line_1.position[1]
        y_2 = line_1.position_2[1]
        
        x_3 = line_2.position[0]
        x_4 = line_2.position_2[0]
        y_3 = line_2.position[1]
        y_4 = line_2.position_2[1]
        
        # intersect_distance_1 = ((x_4-x_3)*(y_1-y_3) - (y_4-y_3)*(x_1-x_3)) / ((y_4-y_3)*(x_2-x_1) - (x_4-x_3)*(y_2-y_1))
        # intersect_distance_2 = ((x_2-x_1)*(y_1-y_3) - (y_2-y_1)*(x_1-x_3)) / ((y_4-y_3)*(x_2-x_1) - (x_4-x_3)*(y_2-y_1))
        
        # if (not self.line_on_point(line_2, line_1.position)) and (not self.line_on_point(line_2, line_1.position_2)):
        try:
            intersect_distance_1 = ((x_4-x_3)*(y_1-y_3) - (y_4-y_3)*(x_1-x_3)) / ((y_4-y_3)*(x_2-x_1) - (x_4-x_3)*(y_2-y_1))
            intersect_distance_2 = ((x_2-x_1)*(y_1-y_3) - (y_2-y_1)*(x_1-x_3)) / ((y_4-y_3)*(x_2-x_1) - (x_4-x_3)*(y_2-y_1))
        except ZeroDivisionError:
            line_1.position[1] -= 1
            line_1.position_2[1] -= 1
            line_2.position[1] += 1
            line_2.position_2[1] += 1
            # print("parallel")
            return True
        
        # else:
        #     print("parallel")
        #     return True
        
        
        if (intersect_distance_1 < 0 or intersect_distance_1 > 1) or (intersect_distance_2 < 0  or intersect_distance_2 > 1):
            return False
        
        intersection_position = Vector2(x_1 + (intersect_distance_1 * (x_2 - x_1)), y_1 + (intersect_distance_1 * (y_2 - y_1)))
        gfxdraw.aacircle(line_1.surface, int(intersection_position[0]), int(intersection_position[1]), 5, (255, 0, 0))
        
        # print(f"intersect {intersection_position}")

        # try:
        #     n = collision_axis / intersect_distance_1
        # except ZeroDivisionError:
        #     n = Vector2()
        
        # delta = None
        # line_1.position = line_1.position - line_1.last_position
        # line_1.position_2 = line_1.position_2 - line_1.last_position_2

        # line_2.position = line_2.position - line_2.last_position
        # line_2.position_2 = line_2.position_2 - line_2.last_position_2
        
        # line_1.position += (0.5 * delta * n) * (not line_1.anchored)
        # line_1.position_2 += (0.5 * delta * n) * (not line_1.anchored)
        # line_2.position -= (0.5 * delta * n) * (not line_2.anchored)
        # line_2.position_2 -= (0.5 * delta * n) * (not line_2.anchored)    
        
        
        return True
        