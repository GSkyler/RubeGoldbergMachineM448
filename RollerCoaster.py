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
from pymunk.vec2d import Vec2d

executed = False

x1 = 750
x2 = 925
myBody = pymunk.Body
myShape = pymunk.Shape


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
        self._add_roller_coaster()

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

            global x1, x2
            global myBody
            # print(myBody.position)

            if executed:
                x = myBody.position.x
                if x1 < x < x2:
                    # myBody.gravity = (0.0, 900.0)
                    self._space.gravity = (0, 600)
                    # print("yes")

                else:
                    # myBody.gravity = (0.0, -900.0)
                    self._space.gravity = (0, -900.0)

    def _add_roller_coaster(self):
        points = [(-94.37*2, 129.96*2.5), (-93.92*2, 118.38*2.5), (-91.89*2, 106.11*2.5), (-88.23*2, 93.35*2.5), (-82.88*2, 80.32*2.5),
                  (-75.81*2, 67.25*2.5), (-67.05*2, 54.36*2.5), (-56.62*2, 41.87*2.5), (-44.6*2, 29.99*2.5), (-31.07*2, 18.93*2.5), (-16.15*2, 8.88*2.5), (-8.2*2,4.4*2.5),
                  (11.7*2, 2*2.5), (28.3*2, 7.49*2.5), (43.72*2, 17.1*2.5), (57.81*2, 27.78*2.5)] #, (70.44*2, 39.36*2.5)
        points2 = [(98.68*1.5, 77.42), (104.7*1.5, 90.49), (109.03*1.5, 103.3), (111.69*1.5, 115.87), (112.75*1.5, 127.75),
                   (112.31*1.5, 138.81), (110.49*1.5, 148.86), (107.43*1.5, 157.74), (103.29*1.5, 165.28), (98.25*1.5, 171.37),
                   (92.53*1.5, 175.89), (86.31*1.5, 178.77), (79.83*1.5, 179.97), (73.3*1.5, 179.45), (66.96*1.5, 177.23), (61.01*1.5, 173.34),
                   (55.68*1.5, 167.86), (51.17*1.5, 160.88), (47.66*1.5, 152.51), (45.33*1.5, 142.9), (44.33*1.5, 132.22), (44.78*1.5, 120.64),
                   (46.81*1.5, 108.37), (50.47*1.5, 95.61), (55.82*1.5, 82.58)]
        points3 = [(107.63*2, 21.19*2), (122.55*2, 11.14*2), (138.7*2, 2.26*2), (155.93*2, -5.28*2), (174.05*2, -11.37*2), (192.87*2, -15.89*2),
                   (212.18*2, -18.77*2)]
        for x in range(len(points) - 2):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = 540, 300
            shape = pymunk.Segment(body, points[x], points[x+1], 0.0)
            shape.elasticity = 0
            shape.friction = 0
            self._space.add(body, shape)
        for x in range(len(points2) - 2):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = 520, 300
            shape = pymunk.Segment(body, points2[x], points2[x+1], 0.0)
            shape.elasticity = 0
            shape.friction = 0
            self._space.add(body, shape)
        for x in range(len(points3) - 2):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = 450, 250
            shape = pymunk.Segment(body, points3[x], points3[x+1], 0.0)
            shape.elasticity = 0
            shape.friction = 0
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
        mass = 20
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(115, 350)
        body.position = 400, 900
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.6
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