# Mini-project #7 - Spaceship

# code to use local simplegui simulator
try:
    import simplegui
    import codeskulptor

    SIMPLEGUICS2PYGAME = False
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    import SimpleGUICS2Pygame.codeskulptor as codeskulptor

    SIMPLEGUICS2PYGAME = True
    import SimpleGUICS2Pygame.codeskulptor_lib as codeskulptor_lib
    import SimpleGUICS2Pygame.simplegui_lib as simplegui_lib

import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
# soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self, canvas):
        # TODO: Modify the draw method for the Ship class to draw
        """
        the ship image (without thrust flames) instead of a circle. This method should
        incorporate the ship's position and angle. Note that the angle should
        be in radians, not degrees. Since a call to the ship's draw method
        already exists in the draw handler, you should now see the ship image.
        Experiment with different positions and angles for the ship.
        """

        # use object parameters to draw image
        canvas.draw_image(self.image, self.image_center,
                          self.image_size, self.pos, self.image_size,
                          self.angle)

        # TODO: Modify the ship's draw method to draw the thrust image
        """
        when it is on. (The ship image is tiled and contains both
        images of the ship.)
        """

    def update(self):
        # TODO: Implement an initial version of the update method for the ship.
        """
        This version should update the position of the ship based on its
        velocity. Since a call to the update method also already exists in
        the draw handler, the ship should move in response to different
        initial velocities.
        """

        # iterate through the
        self.pos = [p + v for p, v in zip(self.pos, self.vel)]

        # TODO: Modify the update method for the ship to increment its angle by
        """ its angular velocity."""

        # TODO: Add code to the ship's update method to use the given helper
        """
        function angle_to_vector to compute the forward vector pointing in
        the direction the ship is facing based on the ship's angle.
        """

        # TODO: Next, add code to the ship's update method to accelerate
        """
        the ship in the direction of this forward vector when the ship is
        thrusting. You will need to update the velocity vector by a small
        fraction of the forward acceleration vector so that the ship does not
        accelerate too fast.
        """

        # TODO: Then, modify the ship's update method such that the ship's
        """
        position wraps around the screen when it goes off the edge (use
        modular arithmetic!).
        """

        # TODO: Up to this point, your ship will never slow down.
        """
        Finally, add friction to the ship's update method as shown in the
        "Acceleration and Friction" video by multiplying each component of
        the velocity by a number slightly less than 1 during each update.
        """
        pass

    # TODO: Add methods to the Ship class to increment and decrement
    """
    the angular velocity by a fixed amount.
    (There is some flexibility in how you structure these methods.)
    """

    # TODO: Add a method to the Ship class to turn the thrusters on/off
    """
    (you can make it take a Boolean argument which is True or False to
    decide if they should be on or off).
    """

    # TODO: Modify the ship's thrust method to play the thrust sound when the
    """thrust is on. Rewind the sound when the thrust turns off."""


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")

    def update(self):
        pass


def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size,
                      (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size,
                      (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()


# timer handler that spawns a rock
def rock_spawner():
    pass


# TODO: Call these methods in the keyboard handlers appropriately
"""and verify that you can turn your ship as you expect."""

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [1, 1], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image,
                asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1], 0, 0,
                   missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)

# TODO: Make your ship turn in response to the left/right arrow keys.
"""Add keydown and keyup handlers that check the left and right arrow keys."""

# TODO: Modify the keyboard handlers to turn the ship's thrusters on/off.

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

# 1 pt - The program draws the ship as an image.
# 1 pt - The ship flies in a straight line when not under thrust.
# 1 pt - The ship rotates at a constant angular velocity in a counter
# clockwise direction when the left arrow key is held down.
# 1 pt - The ship rotates at a constant angular velocity in the clockwise
# direction when the right arrow key is held down.
# 1 pt - The ship's orientation is independent of its velocity.
# 1 pt - The program draws the ship with thrusters on when the up arrow is
# held down.
# 1 pt - The program plays the thrust sound only when the up arrow key is
# held down.
# 1 pt - The ship accelerates in its forward direction when the thrust key is
#  held down.
# 1 pt - The ship's position wraps to the other side of the screen when it
# crosses the edge of the screen.
# 1 pt - The ship's velocity slows to zero while the thrust is not being
# applied.
# 1 pt - The program draws a rock as an image.
# 1 pt - The rock travels in a straight line at a constant velocity.
# 1 pt - The rock is respawned once every second by a timer.
# 1 pt - The rock has a random spawn position, spin direction and velocity.
# 1 pt - The program spawns a missile when the space bar is pressed.
# 1 pt - The missile spawns at the tip of the ship's cannon.
# 1 pt - The missile's velocity is the sum of the ship's velocity and a
# multiple of its forward vector.
# 1 pt - The program plays the missile firing sound when the missile is
# spawned.
# 1 pt - The program draws appropriate text for lives on the upper left
# portion of the canvas.
# 1 pt - The program draws appropriate text for score on the upper right
# portion of the canvas.
