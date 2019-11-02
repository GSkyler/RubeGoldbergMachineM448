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



# https://stackoverflow.com/questions/34926901/python-tkinter-clickable-text

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
    global choice
    choice = random.choice([True, False])

    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """
    def __init__(self):
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, -900.0)
        # self.x1 = ""
        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((600, 700))

        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        # Balls that exist in the world
        self._balls = []

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

    def _add_static_scenery(self):
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_lines = [pymunk.Segment(static_body, (250.0, 400.0), (270.0, 300.0), 0.0),  #left bucket line 1
                        pymunk.Segment(static_body, (270.0, 300.0), (330.0, 300.0), 0.0),  #midddle bucket line 1
                        pymunk.Segment(static_body, (330.0, 300.0), (350.0, 400.0), 0.0),  #right bucket line 1
                        pymunk.Segment(static_body, (350.0, 400.0), (370.0, 300.0), 0.0),  #left bucket line 2
                        pymunk.Segment(static_body, (370.0, 300.0), (430.0, 300.0), 0.0),  # middle bucket line 2
                        pymunk.Segment(static_body, (430.0, 300.0), (450.0, 400.0), 0.0),  # right bucket line 2
                        ]
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.95
        self._space.add(static_lines)

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
            self._create_ball()
            self._ticks_to_next_ball = 300

    def _create_ball(self):
        """
        Create a ball.
        :return:
        """
        mass = 12
        radius = 17
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(260, 440)
        body.position = x, 650
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.80
        shape.friction = 0.9
        self._space.add(body, shape)
        self._balls.append(shape)

    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """

        self._screen.fill(THECOLORS["white"])

        font = pygame.font.Font('freesansbold.ttf', 32)

        black = (0, 0, 0)

        # create a text suface object,
        # on which text is drawn on it.
        text = font.render(x1, True, black)
        text2 = font.render("Yes", True, black)
        text3 = font.render("No", True, black)





        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()
        textRect2 = text2.get_rect()
        textRect3 = text3.get_rect()

        # set the center of the rectangular object.
        textRect.center = (300, 200)
        textRect2.center = (300, 450)#text under bucket 1
        textRect3.center = (400, 450)#text under bucket 2

        # infinite loop
        # while True:

        if choice == True :
            self._screen.blit(text2, textRect2)#this randomizes which bucket will be yes or no
            self._screen.blit(text3, textRect3)
            print("yeh")
        if choice == False :
            self._screen.blit(text2, textRect3)
            self._screen.blit(text3, textRect2)
            print("nah")

        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        self._screen.blit(text, textRect)


    def _draw_objects(self):
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)



if __name__ == '__main__':
    game = BouncyBalls()
    game.run()