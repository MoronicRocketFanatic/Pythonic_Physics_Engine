from time import perf_counter   # noqa: F401
import pygame
from pygame import Vector2
from pygame import gfxdraw
import math

# start = perf_counter()
# print(f"""Function time: (secs): {perf_counter() - start} (millisecs): {(perf_counter() - start)*1000}""")
class PhysicsObject():
    """Main branch for physics objects to specialize off into."""

    def __init__(self, surface:pygame.Surface, position:Vector2, color:pygame.Color = (200, 200, 200), anchored:bool = False) -> None:
        """Main physics object class for others to inherit.

        Args:
            surface (pygame.Surface): Surface to draw onto.
            position (Vector2): Center of the object.
            color (pygame.Color, optional): Color of the object. Defaults to (200, 200, 200) (light gray).
            anchored (bool, optional): If the object is anchored into place or not. Defaults to False.
        """        
        self.position = position
        self.last_position = position
        self.anchored = anchored

        self.surface = surface
        self.color = color
        self.acceleration = Vector2(0,0)


    def update_position(self, delta_time: float) -> None:
        """Updates the position of the object.

        Args:
            delta_time (float): The amount of time passed since this was last called.
        """        

        self.displacement = self.position - self.last_position

        self.last_position = self.position

        self.position = self.position + self.displacement + self.acceleration * (delta_time*delta_time) #position = position + displacement + acceleration * (delta_time * delta_time)
        
        self.acceleration = Vector2(0, 0)



    def accelerate(self, acceleration:Vector2) -> None:
        """Adds to the object's current acceleration force.

        Args:
            acceleration (Vector2): Amount of acceleration.
        """        
        """Use to accelerate an object"""
        self.acceleration += acceleration



class Ball(PhysicsObject):
    """And he said, "let there be balls!" and there was balls. The simplest and easiest to compute."""

    def __init__(self, surface: pygame.Surface, position:Vector2, radius:float = 10, color: pygame.Color = (200, 200, 200), anchored:bool = False) -> None:
        """Balls, a simple and robust collision mesh.

        Args:
            surface (pygame.Surface): Surface to draw onto.
            position (Vector2): Center of the ball.
            radius (float, optional): Radius of the ball. Defaults to 10.
            color (pygame.Color, optional): Color of the ball. Defaults to (200, 200, 200) (light gray).
            anchored (bool, optional): If the ball is anchored into place or not. Defaults to False.
        """        
        super().__init__(surface, position, color, anchored)
        self.radius = radius


    def draw_antialiased_wireframe(self) -> bool:
        """Draws the antialiased wireframe of the object.

        Returns:
            bool: Returns if the object was too far out in the case of an overflow error.
        """        
        try:
            gfxdraw.aacircle(self.surface, int(self.position[0]), int(self.position[1]), self.radius, self.color)
        except OverflowError:
            print(f"OBJECT [{self}] OUT OF BOUNDS, MOVING TO 0, 0 AND KILLING VELOCITY.")
            
            self.position = Vector2(0, 0)
            self.last_position = Vector2(0, 0)
            
            gfxdraw.aacircle(self.surface, int(self.position[0]), int(self.position[1]), self.radius, self.color)
            return True

    
    



class Line(PhysicsObject):
    """Lines of..."""

    def __init__(self, surface: pygame.Surface, position: Vector2, position_2: Vector2, color: pygame.Color = (200, 200, 200), anchored: bool = False) -> None:
        """Lines, the building blocks of all polygons.

        Args:
            surface (pygame.Surface): Surface to draw onto.
            position (Vector2): Start of the line.
            position_2 (Vector2): End of the line.
            color (pygame.Color, optional): Color of the line. Defaults to (200, 200, 200) (light gray).
            anchored (bool, optional): If the line is anchored into place or not. Defaults to False.
        """        
        super().__init__(surface, position, color, anchored)
        self.position_2 = position_2
        self.last_position_2 = position_2
        self.segment_vector = self.position_2 - self.position
        self.normal = self.segment_vector.rotate(90)


    def update_position(self, delta_time: float) -> None:  
        self.displacement_2 = self.position_2 - self.last_position_2

        self.last_position_2 = self.position_2

        self.position_2 = self.position_2 + self.displacement_2 + self.acceleration * (delta_time*delta_time) #position = position + displacement + acceleration * (delta_time * delta_time)
        
        super().update_position(delta_time)
    

    def draw_antialiased_wireframe(self) -> bool:
        """Draws the antialiased wireframe of the object.

        Returns:
            bool: Returns if the object was too far out in the case of an overflow error.
        """        
        try:
            gfxdraw.line(self.surface, int(self.position[0]), int(self.position[1]), int(self.position_2[0]), int(self.position_2[1]), self.color)
        
        except OverflowError:
            print(f"OBJECT [{self}] OUT OF BOUNDS, MOVING TO 0, 0 AND KILLING VELOCITY.")
            
            adjusted_position_2 = self.position_2 - self.position #so that line doesn't lose length or rotation
            
            self.position = Vector2(0, 0)
            self.last_position = Vector2(0, 0)
            self.position_2 = adjusted_position_2
            self.last_position_2 = adjusted_position_2
            
            gfxdraw.line(self.surface, int(self.position[0]), int(self.position[1]), int(self.position_2[0]), int(self.position_2[1]), self.color)
            return True



class Square(PhysicsObject):
    pass



class Triangle(PhysicsObject):
    pass






class Solver():
    """The brain behind the physics engine."""

    def __init__(self, grav_objects:list[PhysicsObject], no_grav_objects:list[PhysicsObject], subsets:int = 8, gravity:float = 1000) -> None:
        """Here we go

        Args:
            grav_objects (list[PhysicsObject]): A list of physics objects that have collisions and gravity
            no_grav_objects (list[PhysicsObject]): A list of physics objects that have collisions
            subsets (int, optional): The amount of subsets that the Solver will go over in an update() cycle. Defaults to 8.
            gravity (float, optional): Strength of the gravity, default is similiar to Earth. Defaults to 1000.
        """        
        self.gravity = gravity
        self.grav_objects = grav_objects
        self.no_grav_objects = no_grav_objects #we need to save as much perf as possible
        self.all_objects = self.grav_objects + self.no_grav_objects
        self.subsets = subsets
        
        self.time_elapsed = 0

    
    def update(self, delta_time:float) -> None:
        """Applies gravity, updates, and solves collisions between all Solver objects.

        Args:
            delta_time (float): The amount of time passed since last call.
        """        
        self.time_elapsed += delta_time
        subset_delta_time = delta_time/self.subsets #we need to distribute time accordingly so that time isn't screwed up
        
        self.all_objects = self.grav_objects + self.no_grav_objects #we need to constantly update this to account for all sorts of changes

        for subset in range(self.subsets): #surely there's a better way?
            self.apply_gravity(self.gravity)
            self.solve_collisions()
            self.update_positions(subset_delta_time)


    
    def update_positions(self, delta_time:float) -> None:
        """Updates the positions of all objects in the Solver object.

        Args:
            delta_time (float): The amount of time passed since last update.
        """        
        for object in self.all_objects:
            object.update_position(delta_time)


    def apply_gravity(self, gravity) -> None:
        """Applies gravity to all gravity affected objects in the Solver object.

        Args:
            gravity (_type_): The amount of gravity to apply.
        """        
        """Applies the gravity to all specified gravity objects."""
        for object in self.grav_objects:
            object.accelerate(Vector2(0, gravity))


    def solve_collisions(self) -> None:
        """Solves the collisions between all objects stored in the Solver object.
        """        
        for object_1 in self.all_objects:
            object_1_type = type(object_1)

            for object_2 in self.all_objects: #NEEDS BETTER ALGO. THE CONSTANT LOOP + A LOT OF IFS IS PERFORMANCE HEAVY
                
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
        """Resolves and detects collisions between two Ball objects.

        Args:
            ball_1 (Ball): Ball one of collision.
            ball_2 (Ball): Ball two of collision.

        Returns:
            bool: True or false of collision.
        """        
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
        return False
    

    def line_on_point(self, line: Line, point: Vector2) -> bool:
        """Detects collision between a point and a line.

        Args:
            line (Line): Line of collision.
            point (Vector2): Point of collision.

        Returns:
            bool: True or false of collision.
        """        
        line_length = math.dist(line.position, line.position_2)
        distance_1 = math.dist(point, line.position)
        distance_2 = math.dist(point, line.position_2)

        buffer = 0.1

        if ((distance_1 + distance_2) >= (line_length - buffer)) and ((distance_1 + distance_2) >= (line_length + buffer)):
            return True
        return False

    
    def line_on_ball(self, line: Line, ball: Ball) -> bool:
        """Detects and resolves collision between a Ball and a Line.

        Args:
            line (Line): Line of collision.
            ball (Ball): Ball of collision.

        Returns:
            bool: True or false of collision.
        """        
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

        line_length = math.dist(line.position, line.position_2)
        
        dot_product = (((ball.position[0] - line.position[0]) * (line.position_2[0] - line.position[0])) + ((ball.position[1] - line.position[1]) * (line.position_2[1] - line.position[1]))) / math.pow(line_length, 2)
        
        closest_x = line.position[0] + (dot_product * (line.position_2[0] - line.position[0]))
        closest_y = line.position[1] + (dot_product * (line.position_2[1] - line.position[1]))
        
        if self.line_on_point(line, Vector2(closest_x, closest_y)):
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
        """Detects and resolves collision between two Line objects.

        Args:
            line_1 (Line): Line one of collision.
            line_2 (Line): Line two of collision.

        Returns:
            bool: True or false of collision.
        """        
        x_1 = line_1.position[0] #set x's and y's for easier experience
        x_2 = line_1.position_2[0]
        y_1 = line_1.position[1]
        y_2 = line_1.position_2[1]
        
        x_3 = line_2.position[0]
        x_4 = line_2.position_2[0]
        y_3 = line_2.position[1]
        y_4 = line_2.position_2[1]
        
        try: #avoid parallel lines
            intersect_distance_1 = ((x_4-x_3)*(y_1-y_3) - (y_4-y_3)*(x_1-x_3)) / ((y_4-y_3)*(x_2-x_1) - (x_4-x_3)*(y_2-y_1))
            intersect_distance_2 = ((x_2-x_1)*(y_1-y_3) - (y_2-y_1)*(x_1-x_3)) / ((y_4-y_3)*(x_2-x_1) - (x_4-x_3)*(y_2-y_1))
        except ZeroDivisionError:
            if (self.line_on_point(line_2, line_1.position)) and (self.line_on_point(line_2, line_1.position_2)):
                line_1.position[1] += 0.0000005
                line_1.position_2[1] += 0.0000005
                line_2.position[1] -= 0.0000005
                line_2.position_2[1] -= 0.0000005
                # print("parallel")
            return True
        
        if (intersect_distance_1 < 0 or intersect_distance_1 > 1) or (intersect_distance_2 < 0  or intersect_distance_2 > 1): #check for collision
            return False
        
        intersection_position = Vector2(x_1 + (intersect_distance_1 * (x_2 - x_1)), y_1 + (intersect_distance_1 * (y_2 - y_1)))
        gfxdraw.aacircle(line_1.surface, int(intersection_position[0]), int(intersection_position[1]), 5, (255, 0, 0))
        
        line_1.segment_vector = line_1.position_2 - line_1.position #figure out the directions of lines
        line_2.segment_vector = line_2.position_2 - line_2.position
        
        line_1.position = line_1.position + (intersect_distance_1 * .5) * line_1.segment_vector *(not line_1.anchored) #distance along the line * the line direction + the original point
        line_1.position_2 = line_1.position_2 + (intersect_distance_1 * .5) * line_1.segment_vector *(not line_1.anchored)
        line_2.position = line_2.position - (intersect_distance_2 * .5) * line_2.segment_vector *(not line_2.anchored) #same as the other but minus
        line_2.position_2 = line_2.position_2 - (intersect_distance_2 * .5) * line_2.segment_vector *(not line_2.anchored)
        
        return True
        