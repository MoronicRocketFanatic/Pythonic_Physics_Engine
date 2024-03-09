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
        self.rotation = rotation
        self.rotation_center = rotation_center
        self.permanent_rotation = permanent_rotation

        self.color = color
        self.acceleration = Vector2(0,0)

    def accelerate(self, acceleration:Vector2) -> None:
        """Use to accelerate an object"""
        self.acceleration += acceleration



class Ball(PhysicsObject):
    """And he said, "let there be balls!" and there was balls. The simplest and easiest to compute."""

    def __init__(self, surface: pygame.Surface, x: int = 0, y: int = 0, color: pygame.Color = (200, 200, 200), rotation: int = 0, rotation_center: Vector2 = Vector2(0, 0), permanent_rotation: int = 0) -> None:
        super().__init__(surface, x, y, color, rotation, rotation_center, permanent_rotation)

