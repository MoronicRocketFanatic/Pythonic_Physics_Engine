import pygame
from pygame import gfxdraw
import math
from copy import deepcopy

class Box():
    """Class to easily plop a rotatable Box into your pygame scene."""

    def __init__(self, x:int, y:int, width:int, height:int, surface:pygame.Surface, color:tuple = (165, 165, 165), rotation:int = 0, permanent_rotation:int = 0) -> None:
        """Rotation uses degrees, permanent rotation is for a permanent rotation about the object's center."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = surface
        self.color = color
        self.rotation = rotation
        self.permanent_rotation = permanent_rotation

        if self.permanent_rotation > 360:
            self.permanent_rotation -= 360
        
        elif self.permanent_rotation < -360:
            self.permanent_rotation += 360

        # self.left = self.x - self.width/2                      # Removed in favor of a rotatable box that uses points
        # self.top = self.y - self.height/2
        # self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

        self.points = [[self.x - self.width/2, self.y - self.height/2], [self.x + self.width/2, self.y - self.height/2], [self.x + self.width/2, self.y + self.height/2], [self.x - self.width/2, self.y + self.height/2]]

        self.perm_rotated_points = deepcopy(self.points)
        for point in range(len(self.points)):
            temporary_point = self.points[point]
            self.perm_rotated_points[point][0] = math.cos(math.radians(self.permanent_rotation)) * (temporary_point[0] - self.x) - math.sin(math.radians(self.permanent_rotation)) * (temporary_point[1] - self.y) + self.x
            self.perm_rotated_points[point][1] = math.sin(math.radians(self.permanent_rotation)) * (temporary_point[0] - self.x) + math.cos(math.radians(self.permanent_rotation)) * (temporary_point[1] - self.y) + self.y

        self.drawn_points = deepcopy(self.perm_rotated_points)

    
    def draw(self, surface:pygame.Surface = None) -> None:
        """Draws the non-anti-aliased filled box (Surface param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.filled_polygon(surface, self.drawn_points, self.color)


    def draw_wireframe(self, surface:pygame.Surface = None) -> None:
        """Draws the non-anti-aliased wireframe box (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.polygon(surface, self.drawn_points, self.color)

    
    def draw_antialiased(self, surface:pygame.Surface = None) -> None:
        """Draws the anti-aliased filled box (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.aapolygon(surface, self.drawn_points, self.color)
        gfxdraw.filled_polygon(surface, self.drawn_points, self.color) #Requires 2 draw calls, might be a performance issue?


    def draw_antialiased_wireframe(self, surface:pygame.Surface = None) -> None:
        """Draws the anti-aliased wireframe box (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.aapolygon(surface, self.drawn_points, self.color)


    def update(self, x_change:int = 0, y_change:int=0, width_change:int=0, height_change:int=0, rotation_change:int = 0, rotation_center:tuple = None) -> None:
        """Allows manipulation of the box, input the amount of change you want to a variable to have it be properly updated. Rotation center defaults to object center."""

        self.x += x_change
        self.y += y_change
        self.width += width_change
        self.height += height_change
        self.rotation += rotation_change

        # self.left = self.x - self.width/2                     # Removed in favor of a rotatable box that uses points
        # self.top = self.y - self.height/2
        # self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

        self.points = [[self.x - self.width/2, self.y - self.height/2], [self.x + self.width/2, self.y - self.height/2], [self.x + self.width/2, self.y + self.height/2], [self.x - self.width/2, self.y + self.height/2]]


        if self.rotation > 360:
            self.rotation -= 360
        
        elif self.rotation < -360:
            self.rotation += 360

        if rotation_center == None:
            rotation_center = (self.x, self.y)

        for point in range(len(self.points)):
            temporary_point = self.points[point]
            self.perm_rotated_points[point][0] = math.cos(math.radians(self.permanent_rotation)) * (temporary_point[0] - self.x) - math.sin(math.radians(self.permanent_rotation)) * (temporary_point[1] - self.y) + self.x
            self.perm_rotated_points[point][1] = math.sin(math.radians(self.permanent_rotation)) * (temporary_point[0] - self.x) + math.cos(math.radians(self.permanent_rotation)) * (temporary_point[1] - self.y) + self.y

        for point in range(len(self.points)):
            temporary_point = self.perm_rotated_points[point]
            self.drawn_points[point][0] = int(math.cos(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) - math.sin(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[0])
            self.drawn_points[point][1] = int(math.sin(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) + math.cos(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[1])





class Circle():
    """Class to easily plop a circle into your pygame scene."""

    def __init__(self, x:int, y:int, radius:int, surface:pygame.Surface, color:tuple = (165, 165, 165), rotation:int = 0) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.surface = surface
        self.color = color
        self.rotation = rotation

        self.drawn_xy = deepcopy([x, y])
        self.diameter = radius*2

    
    def draw(self, surface:pygame.Surface = None) -> None:
        """Draws the non-anti-aliased filled circle (Surface param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.filled_circle(surface, self.drawn_xy[0], self.drawn_xy[1], self.radius, self.color)


    def draw_wireframe(self, surface:pygame.Surface = None) -> None:
        """Draws the non-anti-aliased wireframe circle (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.aacircle(surface, self.drawn_xy[0], self.drawn_xy[1], self.radius, self.color)

    
    def draw_antialiased(self, surface:pygame.Surface = None) -> None:
        """Draws the anti-aliased filled circle (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.aacircle(surface, self.drawn_xy[0], self.drawn_xy[1], self.radius, self.color)
        gfxdraw.filled_circle(surface, self.drawn_xy[0], self.drawn_xy[1], self.radius, self.color) #Requires 2 draw calls, might be a performance issue?


    def draw_antialiased_wireframe(self, surface:pygame.Surface = None) -> None:
        """Draws the anti-aliased wireframe circle (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.aacircle(surface, self.drawn_xy[0], self.drawn_xy[1], self.radius, self.color)

    
    def update_deprecated(self, x_change:int = 0, y_change:int = 0, radius_change:int = 0, rotation_change:int = 0, rotation_center:tuple = None) -> None:
        """Allows manipulation of the circle, input the amount of change you want to a variable to have it be properly updated. Rotation only makes a difference on a different rotational point."""

        self.x += x_change
        self.y += y_change
        self.radius += radius_change
        self.rotation += rotation_change

        self.diameter = self.radius*2

                

        if self.rotation > 360:
            self.rotation -= 360
        
        elif self.rotation < -360:
            self.rotation += 360

        if rotation_center == None:
            rotation_center = (self.x, self.y)


        temporary_point = [self.x, self.y]
        self.drawn_xy[0] = int(math.cos(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) - math.sin(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[0])
        self.drawn_xy[1] = int(math.sin(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) + math.cos(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[1])


    def update(self, x:int = 0, y:int = 0, radius:int = 0) -> None:
        """Allows manipulation of the circle, input the amount of change you want to a variable to have it be properly updated. Rotation only makes a difference on a different rotational point."""

        self.x = x
        self.y = y
        self.radius = radius
        # self.rotation = rotation (, rotation:int = 0, rotation_center:tuple = None)

        self.diameter = self.radius*2
        
                

        # if self.rotation > 360:
        #     self.rotation -= 360
        
        # elif self.rotation < -360:
        #     self.rotation += 360

        # if rotation_center == None:
        #     rotation_center = (self.x, self.y)


        # temporary_point = [self.x, self.y]
        # self.drawn_xy[0] = int(math.cos(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) - math.sin(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[0])
        # self.drawn_xy[1] = int(math.sin(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) + math.cos(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[1])

        self.drawn_xy = [int(x), int(y)]




class Procedural_Polygon():
    """Class to easily plop a rotatable polygon into your pygame scene."""

    def __init__(self, x:int, y:int, radius:int, point_amount:int, surface:pygame.Surface, color:tuple = (165, 165, 165), rotation:int = 0, permanent_rotation:int = 0) -> None:
        """Points are automatically calculated, rotation is based on degrees, permanent rotation is for a permanent rotation about the object's center."""
        self.x = x
        self.y = y
        self.radius = radius
        self.point_amount = point_amount
        self.surface = surface
        self.color = color
        self.rotation = rotation
        self.permanent_rotation = permanent_rotation

        if self.permanent_rotation > 360:
            self.permanent_rotation -= 360
        
        elif self.permanent_rotation < -360:
            self.permanent_rotation += 360


        self.calculate_points()
        self.drawn_points = deepcopy(self.points)


    def calculate_points(self):
        """Calculates the points based off the radius of the polygon"""
        self.points = []
        radius = self.radius
        point_amount = self.point_amount
        for point in range(point_amount):
            theta = (2*math.pi)/self.point_amount * point + math.radians(self.permanent_rotation)
            coordinates = [self.x + radius * math.cos(theta), self.y + radius *math.sin(theta)]
            # coordinates = [round(self.x + radius * math.cos(theta), 2), round(self.y + radius *math.sin(theta), 1)]
            self.points.append(coordinates)


    def draw(self, surface:pygame.Surface = None) -> None:
        """Draws the non-anti-aliased filled polygon (Surface param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.filled_polygon(surface, self.drawn_points, self.color)


    def draw_wireframe(self, surface:pygame.Surface = None) -> None:
        """Draws the non-anti-aliased wireframe polygon (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.polygon(surface, self.drawn_points, self.color)

    
    def draw_antialiased(self, surface:pygame.Surface = None) -> None:
        """Draws the anti-aliased filled polygon (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.aapolygon(surface, self.drawn_points, self.color)
        gfxdraw.filled_polygon(surface, self.drawn_points, self.color) #Requires 2 draw calls, might be a performance issue?


    def draw_antialiased_wireframe(self, surface:pygame.Surface = None) -> None:
        """Draws the anti-aliased wireframe polygon (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.aapolygon(surface, self.drawn_points, self.color)


    def update(self, x_change:int = 0, y_change:int = 0, radius_change:int = 0, points_amount_change:int = 0, rotation_change:int = 0, rotation_center:tuple = None) -> None:
        """Allows manipulation of the polygon, input the amount of change you want to a variable to have it be properly updated. Rotation center defaults to object center."""
        self.x += x_change
        self.y += y_change
        self.radius += radius_change
        self.point_amount += points_amount_change
        self.rotation += rotation_change

        if self.rotation > 360:
            self.rotation -= 360
        
        elif self.rotation < -360:
            self.rotation += 360

        if rotation_center == None:
            rotation_center = (self.x, self.y)

        self.calculate_points()

        for point in range(len(self.points)):
            temporary_point = self.points[point]
            self.drawn_points[point][0] = int(math.cos(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) - math.sin(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[0])
            self.drawn_points[point][1] = int(math.sin(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) + math.cos(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[1])





class Custom_Polygon():
    """Class to easily plop a rotatable polygon into your pygame scene. REQUIRES MANUAL INPUT OF POINTS"""

    def __init__(self, x:int, y:int, points:list, surface:pygame.Surface, color:tuple = (165, 165, 165), rotation:int = 0, permanent_rotation:int = 0) -> None:
        """Points must be input manually, rotation is based on degrees, permanent rotation is for a permanent rotation about the object's center."""
        self.x = x
        self.y = y
        self.points = points
        self.surface = surface
        self.color = color
        self.rotation = rotation
        self.permanent_rotation = permanent_rotation

        if self.permanent_rotation > 360:
            self.permanent_rotation -= 360
        
        elif self.permanent_rotation < -360:
            self.permanent_rotation += 360

        self.perm_rotated_points = deepcopy(self.points)
        for point in range(len(self.points)):
            temporary_point = self.points[point]
            self.perm_rotated_points[point][0] = math.cos(math.radians(self.permanent_rotation)) * (temporary_point[0] - self.x) - math.sin(math.radians(self.permanent_rotation)) * (temporary_point[1] - self.y) + self.x
            self.perm_rotated_points[point][1] = math.sin(math.radians(self.permanent_rotation)) * (temporary_point[0] - self.x) + math.cos(math.radians(self.permanent_rotation)) * (temporary_point[1] - self.y) + self.y

        self.drawn_points = deepcopy(self.perm_rotated_points)


    def draw(self, surface:pygame.Surface = None) -> None:
        """Draws the non-anti-aliased filled polygon (Surface param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.filled_polygon(surface, self.drawn_points, self.color)


    def draw_wireframe(self, surface:pygame.Surface = None) -> None:
        """Draws the non-anti-aliased wireframe polygon (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.polygon(surface, self.drawn_points, self.color)

    
    def draw_antialiased(self, surface:pygame.Surface = None) -> None:
        """Draws the anti-aliased filled polygon (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.aapolygon(surface, self.drawn_points, self.color)
        gfxdraw.filled_polygon(surface, self.drawn_points, self.color) #Requires 2 draw calls, might be a performance issue?


    def draw_antialiased_wireframe(self, surface:pygame.Surface = None) -> None:
        """Draws the anti-aliased wireframe polygon (Surface Param is optional)."""
        if surface == None:
            surface = self.surface

        gfxdraw.aapolygon(surface, self.drawn_points, self.color)


    def update(self, x_change:int = 0, y_change:int = 0, rotation_change:int = 0, rotation_center:tuple = None) -> None:
        """Allows manipulation of the polygon, input the amount of change you want to a variable to have it be properly updated. Rotation center defaults to object center."""
        self.x += x_change
        self.y += y_change
        self.rotation += rotation_change

        if self.rotation > 360:
            self.rotation -= 360
        
        elif self.rotation < -360:
            self.rotation += 360

        if rotation_center == None:
            rotation_center = (self.x, self.y)

        for point in range(len(self.points)):
            self.points[point][0] += x_change
            self.points[point][1] += y_change
            
            temporary_point = self.points[point]
            self.perm_rotated_points[point][0] = math.cos(math.radians(self.permanent_rotation)) * (temporary_point[0] - self.x) - math.sin(math.radians(self.permanent_rotation)) * (temporary_point[1] - self.y) + self.x
            self.perm_rotated_points[point][1] = math.sin(math.radians(self.permanent_rotation)) * (temporary_point[0] - self.x) + math.cos(math.radians(self.permanent_rotation)) * (temporary_point[1] - self.y) + self.y


        for point in range(len(self.points)):

            temporary_point = self.perm_rotated_points[point]
            self.drawn_points[point][0] = int(math.cos(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) - math.sin(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[0])
            self.drawn_points[point][1] = int(math.sin(math.radians(self.rotation)) * (temporary_point[0] - rotation_center[0]) + math.cos(math.radians(self.rotation)) * (temporary_point[1] - rotation_center[1]) + rotation_center[1])