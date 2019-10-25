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
from pymunk.vec2d import Vec2d
import pymunk.pygame_util

myBody = pymunk.Body
myShape = pymunk.Circle

executed = False

x1 = 700
x2 = 1200

class BouncyBalls(object):
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """

    myBody

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

        # Balls that exist in the world
        self._balls = []
        self._bodies = []
        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks_to_next_ball = 10

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

            self._process_events()
            self._update_balls()
            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()
            # Delay fixed time between frames
            self._clock.tick(50)
            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

            global x1, x2
            global myBody
            #print(myBody.position)



            if executed == True:
                x = myBody.position.x
                if x > x1 and x < x2:
                    #myBody.gravity = (0.0, 900.0)
                    self._space.gravity = (0, 900)
                    #print("yes")

                else:
                    #myBody.gravity = (0.0, -900.0)
                    self._space.gravity = (0, -900.0)
                    #print("no")

            #print(myBody.position.x)

            #print(myBody.x)

    def _create_ball(self):
        """
        Create a ball.
        :return:
        """
        ##mass = 10
        ##radius = 25
        ##inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        ##body = pymunk.Body(mass, inertia)
        ##x = random.randint(115, 450)
        ##body.position = x, 850
        ##shape = pymunk.Circle(body, radius, (0, 0))
        ##shape.elasticity = 0.95
        ## shape.friction = 0.9
        ##self._space.add(body, shape)
        ##self._balls.append(shape)

        mass = 10
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        global myBody
        myBody = pymunk.Body(mass, inertia)
        x = random.randint(115, 450)
        myBody.position = x, 850
        myBody = myBody
        global myShape
        myShape = pymunk.Circle(myBody, radius, (0, 0))
        myShape.elasticity = 0.95
        myShape.friction = 0.9
        self._space.add(myBody, myShape)
        self._bodies.append(myBody)
        self._balls.append(myShape)

        #print(myBody.position.x)

        global executed
        executed = True







    def _add_static_scenery(self):
        """
        Create the static bodies.
        :return: None
        """

        global x1
        global x2

        static_body = self._space.static_body
        static_lines = [pymunk.Segment(static_body, (100.0, 700.0), (500.0, 400.0), 3.0),
                        pymunk.Segment(static_body, (x1, 100), (x2, 100), 5.0)]
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self._space.add(static_lines)

        #### CREATE AND ADD FAN CUBE



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
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self._space.gravity = (0, 900)

    def _update_balls(self):
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        self._ticks_to_next_ball -= 1
        if self._ticks_to_next_ball <= 0:
            if executed == False:
                self._create_ball()
            self._ticks_to_next_ball = 100
        # Remove balls that fall below 100 vertically
        balls_to_remove = [ball for ball in self._balls if ball.body.position.y < 100]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)



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