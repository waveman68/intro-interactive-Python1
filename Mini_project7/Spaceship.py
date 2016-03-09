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
        """
        Class to store image parameters
        :param center: list of x, y coordinate
        :param size: list of width, height
        :param radius:
        :param lifespan:
        :param animated:
        """
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
missile_info = ImageInfo([10, 10], [20, 20], 3, 50)
missile_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

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
# soundtrack = simplegui.load_sound(
#     "https://dl.dropboxusercontent.com/u/50460508/thrust4.mp3")

missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(0.5)
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
# soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    """
    Returns a unit vector as list from an angle
    :param ang:
    :return: list
    """
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False  # thrusters off
        self.thrust_vec = [0, 0]  # initialize with no thrust
        self.thrust_counter = 0  # initialize counter for sound workaround
        self.acceleration = 0.2  # acceleration when thrusting
        self.angle = angle
        self.angle_vel = 0
        self.angle_vel_delta = 0.1
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.friction = 0.98
        if sound:
            self.sound = sound

    def draw(self, canvas):
        # TODO: DONE Modify the draw method for the Ship class to draw
        """
        the ship image (without thrust flames) instead of a circle. This method should
        incorporate the ship's position and angle. Note that the angle should
        be in radians, not degrees. Since a call to the ship's draw method
        already exists in the draw handler, you should now see the ship image.
        Experiment with different positions and angles for the ship.
        """

        # TODO: DONE Modify the ship's draw method to draw the thrust image
        """
        when it is on. (The ship image is tiled and contains both
        images of the ship.)
        """
        # use object parameters to draw image
        if self.thrust:
            # shift image center to pick image half with flames
            canvas.draw_image(self.image,
                              [self.image_center[0] + 90, self.image_center[1]],
                              self.image_size, self.pos, self.image_size,
                              self.angle)
        elif not self.thrust:  # shift back to image center without flames
            canvas.draw_image(self.image, self.image_center,
                              self.image_size, self.pos, self.image_size,
                              self.angle)

    def update(self):
        # TODO: DONE Implement an initial version of the update method for the ship.
        """
        This version should update the position of the ship based on its
        velocity. Since a call to the update method also already exists in
        the draw handler, the ship should move in response to different
        initial velocities.
        """

        # TODO: DONE Then, modify the ship's update method such that the ship's
        """
        position wraps around the screen when it goes off the edge (use
        modular arithmetic!).
        """

        # iterate through  position and velocity and sum for updated position
        # zip # zip is a handy way to iterate over > 1 lists at the same time
        # the % s wraps the rocket around the screen
        self.pos = [(p + round(v)) % s for p, v, s in
                    zip(self.pos, self.vel, [WIDTH, HEIGHT])]

        # TODO: DONE Modify the update method for the ship to increment its
        """angle by its angular velocity."""
        self.angle += self.angle_vel

        # TODO: DONE Add code to the ship's update method to use the given
        """
        helper function angle_to_vector to compute the forward vector pointing
        in the direction the ship is facing based on the ship's angle.
        """
        if self.thrust:
            # accelerate along forward direction: define thrust vector
            self.thrust_vector = [self.acceleration * round(a_v) for a_v in
                                  angle_to_vector(self.angle)]

            # update the velocity vector change by the thrust vector
            # zip is a handy way to iterate over > 1 lists at the same time
            self.vel = [v + a for v, a in zip(self.vel, self.thrust_vector)]

        # TODO: DONE Next, add code to the ship's update method to accelerate
        """
        the ship in the direction of this forward vector when the ship is
        thrusting. You will need to update the velocity vector by a small
        fraction of the forward acceleration vector so that the ship does not
        accelerate too fast.
        """

        # TODO: Up to this point, your ship will never slow down.
        """
        Finally, add friction to the ship's update method as shown in the
        "Acceleration and Friction" video by multiplying each component of
        the velocity by a number slightly less than 1 during each update.
        """
        self.vel = [self.friction * v for v in self.vel]

        # TODO: DONE Add methods to the Ship class to increment and decrement
        """
        the angular velocity by a fixed amount.
        (There is some flexibility in how you structure these methods.)
        """

    def turn_cw(self):
        # updates angular velocity by a constant delta for clockwise
        self.angle_vel = self.angle_vel_delta

    def turn_ccw(self):
        # updates angular velocity by delta for counter-clockwise
        self.angle_vel = -self.angle_vel_delta

    def thrusting(self, is_thrusting):
        """
        Implements thrusting within Ship class
        :param is_thrusting: boolean, whether thrusters are on
        """

        # TODO: DONE Add a method to the Ship class to turn the thrusters on/off
        """
        (you can make it take a Boolean argument which is True or False to
        decide if they should be on or off).
        """
        if is_thrusting:
            self.thrust = True
            self.thrust_counter += 1  # count how long thrusting
            try:
                self.sound.play()
            except AttributeError:
                pass
        else:
            self.thrust = False
            try:
                self.sound.pause()  # pause playing when not thrusting
            except AttributeError:
                pass
            if self.thrust_counter > 20:
                try:
                    self.sound.rewind()  # rewind only after 20 s (workaround)
                except AttributeError:
                    pass
        # TODO: DONE Modify the ship's thrust method to play the thrust sound when the
        """thrust is on. Rewind the sound when the thrust turns off."""

    # TODO: DONE Add a shoot method to your ship class. This should spawn a new
    """
    # missile (for now just replace the old missile in a_missile). The
    missile's initial position should be the tip of your ship's "cannon".
    Its velocity should be the sum of the ship's velocity and a multiple of
    the ship's forward vector.
    """

    def shoot(self):
        global a_missile
        # 40 pixels from ship middle to tip, rotate by angle
        direction = angle_to_vector(self.angle)
        missile_pos = [round(40 * d) for d in direction]
        missile_start = [c + p for c, p in zip(self.pos, missile_pos)]

        missile_speed = 3  # multiplier to determine velocity vector
        missile_vel = [v + missile_speed * d for v, d in zip(self.vel, direction)]

        # TODO: DONE Make sure that the missile sound is passed to the sprite
        """
        initializer so that the shooting sound is played    whenever you shoot a missile.
        """
        a_missile = Sprite(missile_start, missile_vel, self.angle, 0,
                           missile_image, missile_info, missile_sound)


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

    # TODO: DONE Complete the Sprite class (as shown in the "Sprite class" video)
    """
    # by modifying the draw handler to draw the actual image and the update
    handler to make the sprite move and rotate. Rocks do not accelerate or
    experience friction, so the sprite update method should be simpler than
    the ship update method. Test this by giving a_rock different starting
    parameters and ensuring it behaves as you expect.
    """

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        self.pos = [p + v for p, v in zip(self.pos, self.vel)]
        self.angle += + self.angle_vel


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

    canvas.draw_text('Lives', [30, 40], 24, 'White', 'sans-serif')
    canvas.draw_text(str(lives), [30, 70], 24, 'White', 'sans-serif')

    canvas.draw_text('Score', [WIDTH - 90, 40], 24, 'White', 'sans-serif')
    canvas.draw_text(str(score), [WIDTH - 90, 70], 24, 'White', 'sans-serif')

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()


# key handlers
def keydown(key):
    """
    Handler to react to key-down events
    :param key: key pressed
    """

    # TODO: The up arrow should control the thrusters of your spaceship.
    """
    The thrusters should be on when the up arrow is down and off when it is
    up.
    """

    # TODO: DONE Make your ship turn in response to the left/right arrow keys.
    """Add key-down and key-up handlers that check the left and right arrow keys."""

    # TODO: DONE Modify the keydown handler to call this shoot method when the
    """space-bar is pressed."""

    if key == simplegui.KEY_MAP["up"]:
        # True for update logic to use image with flames
        my_ship.thrusting(True)

    elif key == simplegui.KEY_MAP["left"]:
        # turn the ship counter-clockwise
        my_ship.turn_ccw()

    elif key == simplegui.KEY_MAP["right"]:
        # turn the ship counter-clockwise
        my_ship.turn_cw()

    elif key == simplegui.KEY_MAP['space']:
        # shoot a missile
        my_ship.shoot()


def keyup(key):
    """
    Handler to react to key-up events
    :param key: key pressed
    """

    # improve readability, use in list vice == 'left' or == 'right'
    key_list_lr = [simplegui.KEY_MAP["left"], simplegui.KEY_MAP["right"]]

    if key == simplegui.KEY_MAP["up"]:
        # False for update logic to use image without flames
        my_ship.thrusting(False)

    elif key in key_list_lr:
        # release left/right stops turning
        my_ship.angle_vel = 0


# timer handler that spawns a rock
def rock_spawner():
    """
    Function to generate asteroids (rocks)
    """
    global a_rock
    # TODO: DONE Implement the timer handler rock_spawner.
    """
    # In particular, set a_rock to be a new rock on every tick. (Don't
    forget to declare a_rock as a global in the timer handler.) Choose a
    velocity, position, and angular velocity randomly for the rock. You will
    want to tweak the ranges of these random numbers, as that will affect
    how fun the game is to play. Make sure you generated rocks that spin in
    both directions and, likewise, move in all directions.
    """
    rock_pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
    # work around CodeSkulptor limitation to produce random fractions
    # normally would be random.uniform()...
    rock_vel = [random.randrange(-5, 5), random.randrange(-5, 5)]
    # work around CodeSkulptor limitation to produce -Pi to Pi
    ang = random.randrange(-314, 314) / 100
    ang_vel = random.randrange(-4, 4) / 40
    a_rock = Sprite(rock_pos, rock_vel, ang, ang_vel, asteroid_image,
                    asteroid_info)


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info,
               ship_thrust_sound)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image,
                asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1], 0, 0,
                   missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)

# TODO: DONE Call these methods in the keyboard handlers appropriately
"""and verify that you can turn your ship as you expect."""
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# TODO: Modify the keyboard handlers to turn the ship's thrusters on/off.

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

# 1 pt - The program draws the ship as an image.
# CHECK

# 1 pt - The ship flies in a straight line when not under thrust.
# CHECK

# 1 pt - The ship rotates at a constant angular velocity in a counter
# clockwise direction when the left arrow key is held down.
# CHECK

# 1 pt - The ship rotates at a constant angular velocity in the clockwise
# direction when the right arrow key is held down.
# CHECK

# 1 pt - The ship's orientation is independent of its velocity.
# CHECK

# 1 pt - The program draws the ship with thrusters on when the up arrow is
# held down.
# CHECK

# 1 pt - The program plays the thrust sound only when the up arrow key is
# held down.
# CHECK

# 1 pt - The ship accelerates in its forward direction when the thrust key is
#  held down.
# CHECK

# 1 pt - The ship's position wraps to the other side of the screen when it
# crosses the edge of the screen.
# CHECK

# 1 pt - The ship's velocity slows to zero while the thrust is not being
# applied.
# CHECK

# 1 pt - The program draws a rock as an image.
# CHECK


# 1 pt - The rock travels in a straight line at a constant velocity.
# CHECK

# 1 pt - The rock is respawned once every second by a timer.
# CHECK

# 1 pt - The rock has a random spawn position, spin direction and velocity.
# CHECK

# 1 pt - The program spawns a missile when the space bar is pressed.
# CHECK

# 1 pt - The missile spawns at the tip of the ship's cannon.
# CHECK

# 1 pt - The missile's velocity is the sum of the ship's velocity and a
# multiple of its forward vector.
# CHECK

# 1 pt - The program plays the missile firing sound when the missile is
# spawned.
# CHECK

# 1 pt - The program draws appropriate text for lives on the upper left
# portion of the canvas.
# CHECK

# 1 pt - The program draws appropriate text for score on the upper right
# portion of the canvas.
# CHECK
