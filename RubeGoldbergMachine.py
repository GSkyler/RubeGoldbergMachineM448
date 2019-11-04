import tkinter as tk
import random
root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Ask a yes or no question!')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Type in the box below :')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)



def getQ():
    global x1
    x1 = entry1.get() + ""
    print(entry1.get())
    root.destroy()



button1 = tk.Button(text='Get your answer!', command=getQ, bg='brown', fg='white',
                    font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)


root.mainloop()

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

        #adds trampoline
        self._add_trampoline()

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
        static_lines = [pymunk.Segment(static_body, (100.0, 700.0), (675.0, 700.0), 0.0),  # Dominoes
                        pymunk.Segment(static_body, (0.0, 750.0), (100.0, 700.0), 0.0),   # Dominoes
                        pymunk.Segment(static_body, (850.0, 600.0), (1000.0, 500.0), 0.0),  # Funnel Diag Left
                        pymunk.Segment(static_body, (1200.0, 600.0), (1050.0, 500.0), 0.0),  # Funnel Diag Right
                        pymunk.Segment(static_body, (1000.0, 400.0), (1000.0, 500.0), 0.0),  # Funnel Vert Left
                        pymunk.Segment(static_body, (1050.0, 400.0), (1050.0, 500.0), 0.0),  # Funnel Vert Right
                        ]
        #static_lines = [pymunk.Segment(static_body, (50.0, 100.0), (500.0, 100.0), 0.0)] #these are like points to make a line (like a acoordinate grid where 0 is on the bottom)
        for line in static_lines:
            line.elasticity = 0.05
            line.friction = 0.9
        self._space.add(static_lines)

    def _add_domino(self):
        for i in range(5): #5 dominoes
            points = [(-10, -40), (-10, 40), (10, 40), (10, -40)]
            mass = 1
            inertia = pymunk.moment_for_box(3, (30, 60))
            body = pymunk.Body(mass, inertia)
            body.position = (300+(i*55)), 750
            shape = pymunk.Poly(body, points, None, 0)
            shape.elasticity = 0
            shape.friction = 0.5
            self._space.add(body, shape)

        # ball that will be hit by dominoes
        mass = 1
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = 625, 750
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.2
        shape.friction = 0.1
        self._space.add(body, shape)

    def _add_trampoline(self):
        points = [(-70, -10), (-70, 10), (70, 10), (70, -10)]
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = 720, 600
        body.angle = 100
        shape = pymunk.Poly(body, points, None, 0)
        shape.elasticity = 6.0
        shape.friction = 0.5
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
        mass = 1
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
