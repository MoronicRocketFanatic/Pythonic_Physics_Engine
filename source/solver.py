from time import perf_counter # noqa: F401
import pygame
from pygame import Vector2
from pygame import gfxdraw
import math
from copy import deepcopy


# start = perf_counter()
# print(f"""Function time: (secs): {perf_counter() - start} (millisecs): {(perf_counter() - start)*1000}""")




def perpendicular(vector:Vector2) -> Vector2:
    """Finds the perpendicular of a Vector2, or any point.

    Args:
        vector (Vector2): Vector2 for perpendicular.

    Returns:
        Vector2: Perpendicular of the inputted vector.
    """    
    return Vector2(-vector[1], vector[0])


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



class Polygon(PhysicsObject):
    
    def __init__(self, surface: pygame.Surface, position: Vector2, points:list[Vector2] = [], radius: float = 10, point_amount: int = 3, color: pygame.Color = (200, 200, 200), anchored: bool = False) -> None:
        """A polygon physics object that you can manually build or input a radius and points for a procedural generation.

        Args:
            surface (pygame.Surface): Surface to draw onto.
            position (Vector2): Center of the polygon.
            points (list[Vector2], optional): The positions of the polygon's points; needs at least 3 points. Defaults to autogenerated points based on the center and radius if there is not enough points.
            radius (float, optional): Radius of the procedural polygon. Defaults to 10.
            point_amount (int, optional): Amount of points to build the procedural polygon. Defaults to 3.
            color (pygame.Color, optional): Color of the polygon. Defaults to (200, 200, 200) (light gray).
            anchored (bool, optional): If the polygon is anchored into place or not. Defaults to False.
        """        

        super().__init__(surface, position, color, anchored)
        self.points = points
        self.radius = radius
        self.point_amount = point_amount
        self.rotation = 0
        self.motor = 0
        
        if len(self.points) < 3:
            self.points = []
            theta = 0
            coordinates = Vector2(0,0)
            self.procedural = True
            for point in range(point_amount): #still don't understand this s##t...  maybe one day...
                theta = (2*math.pi)/self.point_amount * point #+ math.radians(360/(self.point_amount*2))
                #theta = 6.28 / point amount * point_number + fixing rotation
                coordinates = Vector2((self.position[0] + self.radius * math.cos(theta)), (self.position[1] + self.radius *math.sin(theta))) #magic?
                # position  =         ( x   +   radius   *   cosine(theta) ), ( y   +   radius   *   sine(theta) ) 
                self.points.append(coordinates) #append vector

        else:
            self.procedural = False
        
        self.point_relatives = []    
        
        for point in self.points:
            self.point_relatives.append(point - self.position)
        
            
    def update_position(self, delta_time: float) -> None:
        super().update_position(delta_time)
        self.rotation += self.motor
        if self.rotation >= 360:
            self.rotation -= 360
        elif self.rotation <= -360:
            self.rotation += 360
            
            
        for point in range(len(self.points)):
            self.points[point] = self.point_relatives[point] + self.position #cheaper than velocity calculation for all points
            temporary_point = self.points[point]
            self.points[point] = Vector2(int(math.cos(math.radians(self.rotation)) * (temporary_point[0] - self.position[0]) - math.sin(math.radians(self.rotation)) * (temporary_point[1] - self.position[1]) + self.position[0]),int(math.sin(math.radians(self.rotation)) * (temporary_point[0] - self.position[0]) + math.cos(math.radians(self.rotation)) * (temporary_point[1] - self.position[1]) + self.position[1]))
        
        # for point in range(len(self.points)):

            # self.points[point][1] = int(math.sin(math.radians(self.rotation)) * (temporary_point[0] - self.position[0]) + math.cos(math.radians(self.rotation)) * (temporary_point[1] - self.position[1]) + self.position[1])

    
    def draw_antialiased_wireframe(self) -> bool:
        """Draws the antialiased wireframe of the object.

        Returns:
            bool: Returns if the object was too far out in the case of an overflow error.
        """        
        try:
            gfxdraw.filled_polygon(self.surface, self.points, self.color)
            gfxdraw.aapolygon(self.surface, self.points, self.color)
            gfxdraw.aacircle(self.surface, int(self.position[0]), int(self.position[1]), 5, (0, 255, 0))

        
        except OverflowError:
            print(f"OBJECT [{self}] OUT OF BOUNDS, MOVING TO 0, 0 AND KILLING VELOCITY.")
            
            new_points = []
            for point in self.points:
                new_points.append(point - self.position)
            
            # self.points = new_points
            self.points = deepcopy(new_points)
            self.position = Vector2(0, 0)
            for point in range(len(self.points)):
                temporary_point = self.points[point]
                self.points[point][0] = int(math.cos(math.radians(self.rotation)) * (temporary_point[0] - self.position[0]) - math.sin(math.radians(self.rotation)) * (temporary_point[1] - self.position[1]) + self.position[0])
                self.points[point][1] = int(math.sin(math.radians(self.rotation)) * (temporary_point[0] - self.position[0]) + math.cos(math.radians(self.rotation)) * (temporary_point[1] - self.position[1]) + self.position[1])


            
            gfxdraw.aapolygon(self.surface, self.points, self.color)
            return True
        
           
    def support_point(self, direction: Vector2) -> Vector2:
        max_point = Vector2()
        max_distance = float(-999999999999999999999999999999999999999)
    
        for point in self.points:
            distance = point.dot(direction)
            
            if distance > max_distance:
                max_distance = distance
                max_point = point
                
        return max_point
    




class Simplex():
    
    def __init__(self) -> None:
        self.points = []
        self.size = 0
    
    def push_front(self, point) -> list:
        self.points.insert(1, point)
        if self.size > 3:
            self.points.pop()
        self.size = min(self.size+1, 3)
        





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

                
                elif (object_1_type == Polygon) and (object_2_type == Polygon):
                    if self.gjk(object_1, object_2):
                        normal = self.EPA(self.simplex, object_1, object_2)
                        try:
                            object_1.position += normal.normalize()
                            object_2.position -= normal.normalize()
                        except ValueError:
                            object_1.position += normal/200000
                            object_2.position -= normal/200000
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
        
        line_1.segment_vector = line_1.position_2 - line_1.position #figure out the directions of lines
        # gfxdraw.aacircle(line_1.surface, int(line_1.segment_vector[0]), int(line_1.segment_vector[1]), 10, (255, 0, 0))
        
        line_1.normals = [Vector2((-1*(line_1.position_2[1] - line_1.position[1]), (line_1.position_2[0] - line_1.position[0]))), Vector2(((line_1.position_2[1] - line_1.position[1]), -1*(line_1.position_2[0] - line_1.position[0])))]
        # gfxdraw.aacircle(line_1.surface, int(line_1.normals[0][0]), int(line_1.normals[0][1]), 5, (0, 255, 0))
        # gfxdraw.aacircle(line_1.surface, int(line_1.normals[1][0]), int(line_1.normals[1][1]), 5, (0, 0, 255))
        
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
        try:
            gfxdraw.aacircle(line_1.surface, int(intersection_position[0]), int(intersection_position[1]), 5, (255, 0, 0))
        except OverflowError:
            pass
        
        line_1.segment_vector = line_1.position_2 - line_1.position #figure out the directions of lines
        
        line_1.normals = [Vector2((-1*(line_1.position_2[1] - line_1.position[1]), (line_1.position_2[0] - line_1.position[0]))), Vector2(((line_1.position_2[1] - line_1.position[1]), -1*(line_1.position_2[0] - line_1.position[0])))]
        line_2.normals = [Vector2((-1*(line_2.position_2[1] - line_2.position[1]), (line_2.position_2[0] - line_2.position[0]))), Vector2(((line_2.position_2[1] - line_2.position[1]), -1*(line_2.position_2[0] - line_2.position[0])))]
        
        #simple as this
        # normal = line_2.normals[1] #figure out what normal to use
        # if line_2.position.angle_to(line_2.position_2) > 0:
        #     normal = line_2.normals[0].normalize()
        # else:
        #     normal = line_2.normals[1].normalize()
        # # normal = normal.normalize()
        # delta = .05 #figure out line overlap... temporary solution
        # #      position += amount of movement * direction * inverse anchored
        # line_1.position += (delta * .5) * normal * (not line_1.anchored)
        # line_1.position_2 += (delta * .5) * normal * (not line_1.anchored)
        # #negative because well... the opposite direction
        # line_2.position -= (delta * .5) * normal * (not line_2.anchored)
        # line_2.position_2 -= (delta * .5) * normal * (not line_2.anchored)









        
        # line_1_referred = Vector2(0,0) - line_1.position
        # line_2_referred = Vector2(0,0) - line_2.position
        
        # normalize1 = line_1.normals[0].normalize()
        # normalize2 = line_2.normals[0].normalize()
        # dot1 = normalize1.dot(line_1_referred)
        # # dot2 = normalize2.dot(line_2_referred)
        
        # if dot1 < 0:
        #     print(f"NORMAL 1 {normalize1}                   DOT = {dot1}")
        #     normal = normalize1
        # else:
        #     print(f"NORMAL 2 {normalize2}                   DOT = {dot1}")
        #     normal = normalize2
        
            
            
        # delta = .5 #figure out line overlap... temporary solution
        # #      position += amount of movement * direction * inverse anchored
        # line_1.position += (delta * .5) * normal * (not line_1.anchored)
        # line_1.position_2 += (delta * .5) * normal * (not line_1.anchored)
        # #negative because well... the opposite direction
        # line_2.position -= (delta * .5) * normal * (not line_2.anchored)
        # line_2.position_2 -= (delta * .5) * normal * (not line_2.anchored)
            
            
            
            
            
            
            
        
        # line_1.normal = line_1.segment_vector.rotate(90)
        # gfxdraw.line(line_1.surface, int(line_1.segment_vector[0]), int(line_1.segment_vector[1]), int(line_1.normal[0]), int(line_1.normal[1]), (0, 255, 0))
        
        
        # line_2.segment_vector = line_2.position_2 - line_2.position
        # gfxdraw.line(line_1.surface, int(line_2.position[0]), int(line_2.position[1]), int(line_2.segment_vector[0]), int(line_2.segment_vector[1]), (255, 0, 0))
        # line_2.normal = line_2.segment_vector.rotate(90)
        # gfxdraw.line(line_1.surface, int(line_2.segment_vector[0]), int(line_2.segment_vector[1]), int(line_2.normal[0]), int(line_2.normal[1]), (0, 255, 0))
        
        # collision_axis = line_2.normal - line_1.normal        
        
        # line_1.position += (0.5 * collision_axis) * (not line_1.anchored)
        # line_1.position_2 += (0.5 * collision_axis) * (not line_1.anchored)
        # line_2.position += (0.5 * collision_axis) * (not line_2.anchored)
        # line_2.position_2 += (0.5 * collision_axis) * (not line_2.anchored)
        
        
        
        # line_1_old_segment_vector = line_1.last_position_2 - line_1.last_position
        # line_1_velocity_vector = line_1_old_segment_vector - line_1.segment_vector
        # line_1_velocity_vector = line_1.last_position - line_1.position
        

        # reflection = line_1_velocity_vector.reflect_ip(line_2.normal)
        # reflection = Vector2(reflection[0], reflection[1])
        # final_reflection = reflection.reflect_ip(line_2.segment_vector)
        # final_reflection = Vector2(final_reflection[0], final_reflection)
        # line_1_velocity_vector = line_1.position - line_1.last_position
        # final_reflection = line_1_velocity_vector
        # final_reflection.reflect_ip(line_2.normals[0])
        # final_reflection.reflect_ip(line_2.segment_vector)
                
        # line_1.accelerate(final_reflection*1000000)
        
        # line_1.position = line_1.position + (intersect_distance_1 * .5) * line_1.segment_vector *(not line_1.anchored) #distance along the line * the line direction + the original point
        # line_1.position_2 = line_1.position_2 + (intersect_distance_1 * .5) * line_1.segment_vector *(not line_1.anchored)
        # line_2.position = line_2.position - (intersect_distance_2 * .5) * line_2.segment_vector *(not line_2.anchored) #same as the other but minus
        # line_2.position_2 = line_2.position_2 - (intersect_distance_2 * .5) * line_2.segment_vector *(not line_2.anchored)
        
        return True      
        
        
    def find_support(self, polygon_1: Polygon, polygon_2: Polygon, direction: Vector2) -> Vector2:
        support_1 = polygon_1.support_point(direction)
        support_2 = polygon_2.support_point(-direction)
        resultant = support_1 - support_2
        # print(f"POINT 1: {support_1}  |  POINT 2: {support_2}  |  RESULTANT: {resultant}")
        return resultant
       
    
    def gjk(self, polygon_1: Polygon, polygon_2: Polygon) -> bool:
        self.direction = polygon_2.position - polygon_1.position # because it will likely give an extreme point
        support_point = self.find_support(polygon_1, polygon_2, self.direction)
        
        points = []
        for i in range(360):
            temp = self.find_support(polygon_1, polygon_2, Vector2(1, 0).rotate(-i))
            if temp not in points:
                points.append(Vector2(temp[0] + 960, temp[1] + 540))
        # print(points)
        gfxdraw.circle(self.all_objects[0].surface, 960, 540, 2, (0,0,255))
        gfxdraw.polygon(self.all_objects[0].surface, points, (255, 0, 0))
        
        self.simplex = Simplex()
        self.simplex.push_front(support_point)
        
        
        self.direction = -support_point
        
        iteration = 0
        looping = True
        # while looping and iteration < 100:
        while looping:
            iteration+=1
            # print(f"SUPPORT: {support_point}")
            support_point = self.find_support(polygon_1, polygon_2, self.direction)
            
            if (support_point.dot(self.direction) <= 0):
                looping = False
                print("false")
                return False
            
            self.simplex.push_front(support_point)
            
            fake_simplex = deepcopy(self.simplex.points)
            for point in range(len(fake_simplex)):
                fake_simplex[point] = Vector2(fake_simplex[point][0] + 960, fake_simplex[point][1] + 540)
                
            try:
                # gfxdraw.polygon(self.all_objects[0].surface, fake_simplex, (0, 255, 0))
                pass
            except ValueError:
                pass
            
            if (self.next_simplex(self.simplex.points, self.direction)):
                print("collide")
                looping = False
                return True
            # elif len(self.points) > 3:
            #     break
            # else:
            #     return False

    
    def next_simplex(self, points: list[Vector2], direction: Vector2) -> bool:
        if self.simplex.size == 2:
            return self.line(points, direction)
        elif self.simplex.size == 3:
            return self.triangle(points, direction)
        return False
    
    def same_direction(self, direction: Vector2, a_negative: Vector2) -> bool:
        return direction.dot(a_negative) > 0
    
    
    def line(self, points: list[Vector2], direction: Vector2) -> bool:
        point_1 = points[0]
        point_2 = points[1]
        # gfxdraw.circle(self.all_objects[0].surface, int(point_1[0] + 960), int(point_1[1] + 540), 3, (255, 0, 0))
        # gfxdraw.circle(self.all_objects[0].surface, int(point_2[0] + 960), int(point_2[1] + 540), 3, (0, 255, 0))        
        point_1_2 = point_2 - point_1
        a_negative = - point_1
        
        if self.same_direction(point_1_2, a_negative):
            self.direction = a_negative
            
        else:
            self.simplex.points = point_1
            self.direction = a_negative
            
        return False
    
    
    def triangle(self, points: list[Vector2], direction: Vector2) -> bool:
        
        point_1 = self.simplex.points[0]
        point_2 = self.simplex.points[1]
        point_3 = self.simplex.points[2]
        # gfxdraw.circle(self.all_objects[0].surface, int(point_1[0] + 960), int(point_1[1] + 540), 3, (255, 0, 0))
        # gfxdraw.circle(self.all_objects[0].surface, int(point_2[0] + 960), int(point_2[1] + 540), 3, (0, 255, 0))
        # gfxdraw.circle(self.all_objects[0].surface, int(point_3[0] + 960), int(point_3[1] + 540), 3, (0, 0, 255))
        
        length_1_2 = point_2 - point_1
        length_1_3 = point_3 - point_1 
        negative_1 = -point_1
        # cross_1_2_3 = Vector2(length_1_2.cross(length_1_3))
        point_1_2_perpendicular = perpendicular(length_1_2)
        point_1_3_perpendicular = perpendicular(length_1_3)
        

        if (self.same_direction(point_1_3_perpendicular, negative_1)):
            if (self.same_direction(length_1_3, negative_1)):
                
            # if (self.same_direction(length_1_3, negative_1)):
                self.simplex.points = [point_1, point_3]
                self.direction = point_1_3_perpendicular
            # return self.line([point_1, point_3], point_1_3_perpendicular)

            else:
                return self.line([point_1, point_2], self.direction)
            
        
    
        else:
            if (self.same_direction(point_1_2_perpendicular, negative_1)):
                return self.line([point_1, point_2], self.direction)
                # if (self.same_direction(length_1_2, negative_1)):
                #     self.simplex.points = [point_1, point_2]
                #     self.direction = point_1_2_perpendicular
                # return self.line([point_1, point_2], point_1_2_perpendicular)


            else:
                return True
                # if (self.same_direction(length_1_2, negative_1)):
                #     self.direction = length_1_2


                # else:
                #     # self.simplex.points = [point_1, point_2, point_3]
                #     # self.direction = -length_1_2
                #     return True
            
        

        return False
    
    
    def EPA(self, polytope:Simplex, polygon_1:Polygon, polygon_2:Polygon):
        minimum_index = 0
        minimum_distance = math.inf
        minimum_normal = Vector2(0,0)
        
        while minimum_distance == math.inf:
            for i in range(polytope.size):
                j = (i + 1) % polytope.size
                
                vertex_i = polytope.points[i]
                vertex_j = polytope.points[j]
                
                vertex_i_j = vertex_j - vertex_i
                try:
                    normal = perpendicular(vertex_i_j).normalize()
                except ValueError:
                    normal = perpendicular(vertex_i_j)
                distance = normal.dot(vertex_i)
                
                if distance < 0:
                    distance *= -1
                    normal *= -1
                    
                if distance < minimum_distance:
                    minimum_distance = distance
                    minimum_normal = normal
                    minimum_index = j
                    
                support = self.find_support(polygon_1, polygon_2, minimum_normal)
                small_distance = minimum_normal.dot(support)
                
                if abs(small_distance - minimum_distance) > 0.001:
                    minimum_distance = math.inf
                    try:
                        polytope.points.remove(support)
                    except ValueError:
                        print("die")
                    polytope.points.insert(minimum_index, support)
                    
        return minimum_normal * (minimum_distance + 0.001)