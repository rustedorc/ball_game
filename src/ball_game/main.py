import pygame as pg
import sys
from .settings import FPS, WIDTH, HEIGHT, CAPTION, COLOURS
from .loader import load_music
from .ball import Ball, BallContainer

class Game:
    def __init__(self) -> None:
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(CAPTION)
        self.clock = pg.time.Clock()

        self.music = load_music(pg.mixer)

        self.ball_container = BallContainer()
    
    def run(self) -> None:
        running = True
        while running:
            self.clock.tick(FPS)
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False
                
                elif event.type == pg.MOUSEBUTTONUP:
                    x, y = pg.mouse.get_pos()
                    self.ball_container.add_ball(Ball(x, y, 10, self.screen, COLOURS['yellow']))
                
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.ball_container.reset_container()
            
            hits = self.ball_container.update()
            if hits:
                self.music['pew'].play()
            
            self.screen.fill(COLOURS['black'])

            self.ball_container.draw_balls()

            pg.display.flip()
        
        pg.quit()
        sys.exit()