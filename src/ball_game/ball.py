from __future__ import annotations

import pygame as pg
from pygame.math import Vector2 as Vector
from typing import Optional, NamedTuple
from itertools import combinations
import random

from .settings import FPS, GRAVITY, HEIGHT, WIDTH, SPEED_MULTIPLIER, COLOURS, BALL_COLOURS

class Coordinates(NamedTuple):
    x: int
    y: int

class Ball:
    def __init__(self, x: int, y: int, radius: int, screen: pg.surface.Surface, colour: tuple[int, int, int]) -> None:
        self.x = x
        self.y = y
        self.start = Coordinates(self.x, self.y)
        self.radius = radius
        self.screen = screen
        self.colour = colour

        self.down = Vector(0, 1) * SPEED_MULTIPLIER
        self.up = Vector(0, -1) * SPEED_MULTIPLIER
        self.left = Vector(-1, 0) * SPEED_MULTIPLIER
        self.right = Vector(1, 0) * SPEED_MULTIPLIER
        self.null_position = Vector(0, 0)

        self.current_direction: Vector = self.down

        self.kinematics = {letter:float('inf') for letter in 'SUVAT'}
        
    def __repr__(self) -> str:
        return f'Ball(x={self.x}, y={self.y}, radius={self.radius}, colour={self.colour})'
    
    def draw_circle(self) -> None:
        pg.draw.circle(self.screen, self.colour, (self.x, self.y), self.radius)
    
    def update(self):
        #s = ut + 0.5at^2 NO
        #v^2 = u^2 + 2as
        if self.y >= (HEIGHT - self.radius):
            self.current_direction = self.up + random.choice((self.left, self.right, self.null_position))
            self.colour = random.choice(list(BALL_COLOURS.values()))
        elif self.y <= self.radius:
            self.current_direction = self.down + random.choice((self.left, self.right, self.null_position))
            self.colour = random.choice(list(BALL_COLOURS.values()))
        
        if self.x <= self.radius:
            self.current_direction = self.right + random.choice((self.up, self.down, self.null_position))
            self.colour = random.choice(list(BALL_COLOURS.values()))
        elif self.x >= (WIDTH - self.radius):
            self.current_direction = self.left + random.choice((self.up, self.down, self.null_position))
            self.colour = random.choice(list(BALL_COLOURS.values()))

        
        self.x, self.y = (self.x + self.current_direction.x) , (self.y + self.current_direction.y)

    
    def collision(self, ball: Ball) -> bool:
        """Checks if two balls have collided
        uses a^2 + b^2 = c^2 and checks if the distance between
        the two centres is less than the sum of the two radiuses"""
        return ((((self.x - ball.x) ** 2) + (self.y - ball.y) ** 2) ** (1/2)) < (self.radius + ball.radius)


class BallContainer:
    def __init__(self, *balls: Ball, container:Optional[list[Ball]] = None) -> None:
        self.container = container if container is not None else []
        self.container.extend(balls)
    
    def __repr__(self) -> str:
        return f'BallContainer({self.container})'
    
    def draw_balls(self) -> None:
        for ball in self.container:
            ball.draw_circle()
    
    def add_ball(self, ball: Ball) -> None:
        self.container.append(ball)
    
    def remove_ball(self, *balls: Ball) -> None:
        for ball in balls:
            self.container.remove(ball)
    
    def update(self) -> None:
        self.detect_collisions()
        for ball in self.container:
            ball.update()
    
    def reset_container(self) -> None:
        self.container = []
    
    def detect_collisions(self) -> None:
        for b1, b2 in combinations(self.container, 2):
            if b1 is b2:
                continue
            
            if b1.collision(b2):
                args: tuple[int, int, int, pg.surface.Surface, tuple[int, int, int]] = ((b1.x + b2.x) // 2, (b1.y + b2.y) // 2, b1.radius + b2.radius, b1.screen, COLOURS['yellow'])
                self.add_ball(Ball(*args))
                try:
                    self.remove_ball(b1, b2)
                except ValueError:
                    pass

                    