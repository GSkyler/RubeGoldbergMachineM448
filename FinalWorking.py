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

x1 = 1170
x2 = 1345
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
        self._screen = pygame.display.set_mode((1800, 900))
        self._width = 1800
        self._height = 900
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        #adds domino
        self._add_domino()

        #adds trampoline
        self._add_trampoline()
        self._add_trampoline2()

        #add fan
        self._add_fan()

        #add seesaw
        self._add_seesaw()

        #add newton's cradle
        self._add_cradle()

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

            if executed:
                x = myBody.position.x
                if x1 < x < x2:
                    myBody.velocity = myBody.velocity.x, 10 * random.randint(10, 40)

                else:
                    myBody.velocity = myBody.velocity.x, myBody.velocity.y


    def _add_static_scenery(self):#draws the line
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        zigzag_lines = [pymunk.Segment(static_body, (275, 775), (400, 875), 0),  # first
                        pymunk.Segment(static_body, (100, 745), (300, 670), 0),  # second
                        pymunk.Segment(static_body, (475, 620), (200, 520), 0)]  # third
        for line in zigzag_lines:
            line.elasticity = 0.7
            line.friction = 0.5

        static_lines = [pymunk.Segment(static_body, (0.0, 300.0), (0.0, 600.0), 0.0),  # Left border
                        pymunk.Segment(static_body, (100.0, 345.0), (500.0, 345.0), 0.0),  # Dominoes
                        pymunk.Segment(static_body, (0.0, 395.0), (100.0, 345.0), 0.0),  # Dominoes

                        pymunk.Segment(static_body, (1150.0, 800.0), (1500.0, 900.0), 0.0),   # roof
                        pymunk.Segment(static_body, (1800.0, 900.0), (1500.0, 900.0), 0.0),  # roof
                        pymunk.Segment(static_body, (1800.0, 900.0), (1745.0, 600.0), 0.0),  # roof

                        pymunk.Segment(static_body, (1365.0, 145.0), (1385.0, 70.0), 0.0),  # bucket1 left
                        pymunk.Segment(static_body, (1555.0, 145.0), (1535.0, 70.0), 0.0),  # bucket1 right
                        pymunk.Segment(static_body, (1385.0, 70.0), (1535.0, 70.0), 0.0),   # bucket1 bottom

                        pymunk.Segment(static_body, (1555.0, 145.0), (1575.0, 70.0), 0.0),  # bucket2 left
                        pymunk.Segment(static_body, (1745.0, 145.0), (1725.0, 70.0), 0.0),  # bucket2 right
                        pymunk.Segment(static_body, (1575.0, 70.0), (1725.0, 70.0), 0.0),  # bucket2 bottom

                        pymunk.Segment(static_body, (700.0, 300.0), (900.0, 300.0), 0.0),   #see saw stand
                        pymunk.Segment(static_body, (760.0, 600.0), (1100.0, 600.0), 0.0)    #cradle stand
                        ]

        for line in static_lines:
            line.elasticity = 0.25
            line.friction = 0.6

        static_body = self._space.static_body
        plinko_walls = [pymunk.Segment(static_body, (1365.0, 145.0), (1365.0, 600.0), 0.0),
                        pymunk.Segment(static_body, (1745.0, 145.0), (1745.0, 600.0), 0.0)
                        ]
        for line in plinko_walls:
            line.elasticity = 0.05
            line.friction = 0.9
        self._space.add(plinko_walls)

        #plinko dots
        for y in range(7):
            for x in range(7):
                if (y % 2 == 0):
                    b = pymunk.Body(body_type=pymunk.Body.STATIC)
                    b.position = (1375 + (x * 90), 150 + (y * 70))
                    s = pymunk.Circle(b, 2)
                    s.elasticity = 0.3
                    self._space.add(s)
                else:
                    if (x < 4):
                        b = pymunk.Body(body_type=pymunk.Body.STATIC)
                        b.position = (1375 + (x * 90) + 40, 150 + (y * 70))
                        s = pymunk.Circle(b, 2)
                        s.elasticity = 0.3
                        self._space.add(s)

        self._space.add(zigzag_lines)
        self._space.add(static_lines)

    def _add_domino(self):
        for i in range(5):  #5 dominoes
            points = [(-10, -40), (-10, 40), (5, 40), (5, -40)]
            mass = 30
            inertia = pymunk.moment_for_box(3, (30, 60))
            body = pymunk.Body(mass, inertia)
            body.position = (150+(i*55)), 350
            shape = pymunk.Poly(body, points, None, 0)
            shape.elasticity = 0.3
            shape.friction = 0.5
            self._space.add(body, shape)

        # ball that will be hit by dominoes
        mass = 18
        radius = 15
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = 420, 550
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.2
        shape.friction = 0.2
        self._space.add(body, shape)

    def _add_trampoline(self):
        points = [(-70, -10), (-70, 10), (70, 10), (70, -10)]
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = 540, 290
        body.angle = 2.9
        shape = pymunk.Poly(body, points, None, 0)
        shape.elasticity = 9.0
        shape.friction = 0.5
        self._space.add(body, shape)

    def _add_trampoline2(self):
        points = [(-70, -10), (-70, 10), (70, 10), (70, -10)]
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = 560, 500
        body.angle = 5.35
        shape = pymunk.Poly(body, points, None, 0)
        shape.elasticity = 5.0
        shape.friction = 0.5
        self._space.add(body, shape)

    def _add_fan(self):
        points = [(-100, -10), (-100, 10), (75, 10), (75, -10)]
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = 1270, 300
        shape = pymunk.Poly(body, points, None, 0)
        shape.elasticity = 0
        shape.friction = 0
        self._space.add(body, shape)

    def _add_seesaw(self):
        #triangle base
        points = [(-30, 0), (-5, 30), (5, 30), (30, 0)]
        mass = 10
        inertia = pymunk.moment_for_box(3, (30, 60))
        body = pymunk.Body(mass, inertia)
        body.position = 795, 300
        shape = pymunk.Poly(body, points, None, 0)
        shape.elasticity = 0
        shape.friction = 0.9
        self._space.add(body, shape)

        #long rectangle thing
        points = [(-100, -10), (-100, 10), (100, 10), (100, -10)]
        mass = 20
        inertia = pymunk.moment_for_box(3, (30, 60))
        body = pymunk.Body(mass, inertia)
        body.position = 790, 360
        shape = pymunk.Poly(body, points, None, 0)
        shape.elasticity = 0
        shape.friction = 0.9
        self._space.add(body, shape)

        #mini square
        points = [(-10, -10), (-10, 10), (10, 10), (10, -10)]
        mass = 1
        inertia = pymunk.moment_for_box(3, (30, 60))
        body = pymunk.Body(mass, inertia)
        body.position = 870, 380
        shape = pymunk.Poly(body, points, None, 0)
        shape.elasticity = 0.4
        shape.friction = 0.5
        self._space.add(body, shape)

    def _add_cradle(self):
        bodies = []
        for x in range(-100, 150, 50):
            x += self._width / 2
            offset_y = 700
            mass = 1
            radius = 25
            moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, moment)
            body.position = (x, -75 + offset_y)
            shape = pymunk.Circle(body, radius)
            shape.elasticity = 0.9999999
            self._space.add(body, shape)
            bodies.append(body)
            pj = pymunk.PinJoint(self._space.static_body, body, (x, 75 + offset_y), (0, 0))
            self._space.add(pj)

        #ball that cradle hits
        mass = .5
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        global myBody, myShape, executed
        myBody = pymunk.Body(mass, inertia)
        myBody.position = 1055, 605
        myShape = pymunk.Circle(myBody, radius, (0, 0))
        myShape.elasticity = 0.2
        myShape.friction = 0.2
        self._space.add(myBody, myShape)
        executed = True

        self._reset_bodies(self._space)

    def _reset_bodies(self,space):
        for body in space.bodies:
            body.force = 0, 0
            body.torque = 0
            body.velocity = 0, 0
            body.angular_velocity = 0
        color = random.choice(list(THECOLORS.values()))
        for shape in space.shapes:
            shape.color = color

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
        body.position = 350, 900
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