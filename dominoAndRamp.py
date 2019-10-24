"""This example spawns (bouncing) balls randomly on a L-shape constructed of
two segment shapes. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

# Python imports
import random

# Library imports
import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *

# pymunk imports
import pymunk
import pymunk.pygame_util


class BouncyBalls(object):
    numBalls = 0
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """
    def __init__(self):
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, -900.0)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((1500, 900))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        #adds domino
        self._add_domino()

        # Balls that exist in the world
        self._balls = []

        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks_to_next_ball = 10
        self._oneBall = 0


    def run(self):
        """
        The main loop of the game.
        :return: None
        """
        # Main loop

        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)

            self._update_balls()
            self._process_events()

            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()
            # Delay fixed time between frames
            self._clock.tick(50)
            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

    def _add_static_scenery(self):#draws the line
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        #static_lines = [pymunk.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0)]
        static_lines = [pymunk.Segment(static_body, (0.0, 600.0), (1000.0, 600.0), 0.0),  # Dominoes
                        pymunk.Segment(static_body, (0.0, 600.0), (0.0, 750.0), 0.0),     # Dominoes
                        pymunk.Segment(static_body, (0.0, 750.0), (200.0, 600.0), 0.0),   # Dominoes
                        pymunk.Segment(static_body, (1050.0, 500.0), (1250.0, 300.0), 0.0),  # Funnel Diag Left
                        pymunk.Segment(static_body, (1550.0, 500.0), (1350.0, 300.0), 0.0),  # Funnel Diag Right
                        pymunk.Segment(static_body, (1250.0, 100.0), (1250.0, 300.0), 0.0),  # Funnel Vert Left
                        pymunk.Segment(static_body, (1350.0, 100.0), (1350.0, 300.0), 0.0),  # Funnel Vert Right
                        ]
        #static_lines = [pymunk.Segment(static_body, (50.0, 100.0), (500.0, 100.0), 0.0)] #these are like points to make a line (like a acoordinate grid where 0 is on the bottom)
        for line in static_lines:
            line.elasticity = 0.05
            line.friction = 0.9
        self._space.add(static_lines)

    def _add_domino(self):
        for i in range(5):
            points = [(-10, -50), (-10, 50), (10, 50), (10, -50)]
            mass = 10
            inertia = pymunk.moment_for_box(3, (30, 60))
            body = pymunk.Body(mass, inertia)
            body.position = (300+(i*50)), 650
            shape = pymunk.Poly(body, points, None, 0)
            #shape = pymunk.Circle(body, radius, (0, 0))
            shape.elasticity = 0
            shape.friction = 0.9
            self._space.add(body, shape)

        mass = 1
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = 625, 650
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.2
        shape.friction = 0.1
        self._space.add(body, shape)



    def _process_events(self):
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self._running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")

    def _update_balls(self):
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        self._ticks_to_next_ball -= 1
        if self._ticks_to_next_ball <= 0:
            if self._oneBall ==0:
                self._create_ball()
                self._oneBall = 1
            self._ticks_to_next_ball = 100
            # Remove balls that fall below 100 vertically
        balls_to_remove = [ball for ball in self._balls if ball.body.position.y < 100]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)


    def _create_ball(self):
        """
        Create a ball.
        :return:
        """
        mass = 10
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(115, 350)
        body.position = 10, 900
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        self._space.add(body, shape)
        self._balls.append(shape)

    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(THECOLORS["white"])

    def _draw_objects(self):
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)


if __name__ == '__main__':
    game = BouncyBalls()
    game.run()

