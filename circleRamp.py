import inspect
import math

import pygame
import pygame.color
from pygame.locals import *

import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util

pymunk.pygame_util.positive_y_is_up = False

pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0.0, 900.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# containers
box_size = 200



def add_bar(space, pos, box_offset):
    body = pymunk.Body()
    body.position = Vec2d(pos) + box_offset
    shape = pymunk.Segment(body, (0, 135), (0, -135), 6)#length of the segmgent
    shape.mass = 20
    shape.friction = 0.7
    space.add(body, shape)
    return body

txts = {}



box_offset = box_size, box_size
b1 = add_bar(space, (50, 100), box_offset)
b2 = add_bar(space, (-10000, 100), box_offset)
# Add some pin joints to hold the circles in place.
space.add(pymunk.PivotJoint(b1, space.static_body, (50, 100) + Vec2d(box_offset)))
c = pymunk.SimpleMotor(b1, b2, math.pi)

txts[0] = inspect.getdoc(c)
space.add(c)


static_body = space.static_body
#static_lines = [pymunk.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0)]
static_lines = [pymunk.Segment(static_body, (0.0, 100.0), (700.0, 100.0), 0.0),
                pymunk.Segment(static_body, (80.0, 250.0), (250.0, 100.0), 0.0),
                pymunk.Segment(static_body, (100.0, 350.0), (100, 250.0), 0.0),
                pymunk.Segment(static_body, (100.0, 400.0), (200, 450.0), 0.0),
                pymunk.Segment(static_body, (100.0, 450.0), (1220, 450.0), 0.0),
                pymunk.Segment(static_body, (100.0, 350.0), (100, 450.0), 0.0),
                pymunk.Segment(static_body, (370.0, 400.0), (700, 400.0), 0.0),
                pymunk.Segment(static_body, (100.0, 150.0), (500, 150.0), 0.0),

                pymunk.Segment(static_body, (900.0, 450.0), (1200, 350.0), 0.0)
               ]
#static_lines = [pymunk.Segment(static_body, (50.0, 100.0), (500.0, 100.0), 0.0)] #these are like points to make a line (like a acoordinate grid where 0 is on the bottom)
for line in static_lines:
    line.elasticity = 0
    line.friction = 0.1
space.add(static_lines)


mass = 1
radius = 25
inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
body = pymunk.Body(mass, inertia)
body.position = 950, 0
shape = pymunk.Circle(body, radius, (0, 0))
shape.elasticity = 0
shape.friction = 0.2
space.add(body, shape)

# TODO add one or two advanced constraints examples, such as a car or rope

mouse_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if mouse_joint != None:
                space.remove(mouse_joint)
                mouse_joint = None

            p = Vec2d(event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit != None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                shape = hit.shape
                # Use the closest point on the surface if the click is outside
                # of the shape.
                if hit.distance > 0:
                    nearest = hit.point
                else:
                    nearest = p
                # mouse_joint = pymunk.PivotJoint(mouse_body, shape.body,
                #                                 (0, 0), shape.body.world_to_local(nearest))
                # mouse_joint.max_force = 50000
                # mouse_joint.error_bias = (1 - 0.15) ** 60
                # space.add(mouse_joint)

        elif event.type == MOUSEBUTTONUP:
            if mouse_joint != None:
                space.remove(mouse_joint)
                mouse_joint = None

    screen.fill(pygame.color.THECOLORS["white"])



    space.step(1/ 60)

    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))