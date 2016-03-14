# implementation of Spaceship - program template for RiceRocks
import math
import random

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

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False


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
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
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


# TODO DONE Create a helper function process_sprite_group.
"""
This function should take a set and a canvas and call the update and draw
methods for each sprite in the group.
"""
def process_sprite_group(sprite_group, canvas):
    # TODO: DONE Modify process_sprite_group to check the return value of update for
    """
    sprites. If it returns True, remove the sprite from the group. Again, you
    will want to iterate over a copy of the sprite group in process_sprite_group
    to avoid deleting from the same set over which you are iterating.
    """

    iter_group = sprite_group.copy()
    for i in iter_group:
        i.draw(canvas)
        expired = i.update()
        if expired:
            sprite_group.discard(i)


def group_collide(set_group, other_object):
    """
    Takes a set of objects and determines collision with other_object.
    If any collision in set occurs, the item is removed and true returned.
    :rtype: bool
    :type other_object: object
    :type set_group: set
    :param set_group: set of sprites, e.g., rocks or missiles
    :param other_object: object to check for collision
    """
    return_boolean = False  # default return
    iterate_group = set_group.copy()
    for s in iterate_group:
        if s.collide(other_object):
            return_boolean = return_boolean or True  # return
            set_group.remove(s)

    return return_boolean


# TODO 4.1: Implement a final helper function group_group_collide that takes
"""
two groups of objects as input. group_group_collide should iterate through
the elements of a copy of the first group using a for-loop and then call
group_collide with each of these elements on the second group.
group_group_collide should return the number of elements in the first group
that collide with the second group as well as delete these elements in the
first group. You may find the discard method for sets to be helpful here.
"""


def group_group_collide(group_1, group_2):
    """
    Takes 2 sets of sprite objects, and checks for and keeps track of
    collisions between each element of group_1 with group_2 members. Returns
    the number of collisions
    :rtype: int
    :type group_2: set
    :type group_1: set
    :param group_1: first set of objects to check for collisions
    :param group_2: second set of objects to check for collisions
    """
    tally = 0
    iterate_group_1 = group_1.copy()
    for i in iterate_group_1:
        if group_collide(group_2, i):
            tally += 1
            group_1.discard(i)
    return tally


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

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]],
                              self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
            # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1

        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def increment_angle_vel(self):
        self.angle_vel += .05

    def decrement_angle_vel(self):
        self.angle_vel -= .05

    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))


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

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        """
        Updates sprite and returns boolean concerning lifespan
        :rtype: bool
        :return: boolean, True if >= lifespan
        """
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # TODO: DONE In the update method of the Sprite class, increment the age of the
        """
        sprite every time update is called. If the age is greater than or equal to
        the lifespan of the sprite, then we want to remove it. So, return False
        (meaning we want to keep it) if the age is less than the lifespan and True
        (meaning we want to remove it) otherwise.
        """
        if self.age is not None:
            self.age += 1
            if self.age >= self.lifespan:
                return True
        return False

    # TODO: DONE Add a collide method to the Sprite class. This should take an
    """
    other_object as an argument and return True if there is a collision or False
    otherwise. For now, this other object will always be your ship, but we want
    to be able to use this collide method to detect collisions with missiles
    later, as well. Collisions can be detected using the radius of the two
    objects. This requires you to implement methods get_position and get_radius
    on both the Sprite and Ship classes.
    """

    def collide(self, other_object):
        other_pos = other_object.get_position()
        other_rad = other_object.get_radius()
        if dist(self.pos, other_pos) <= self.radius + other_rad:
            return True
        else:
            return False

# key handlers to control ship
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()


def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)


# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True


def draw(canvas):
    global lives, score, started, time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw/update ship and sprites
    my_ship.draw(canvas)

    # TODO DONE Call the process_sprite_group function on rock_group in the
    """draw handler."""
    process_sprite_group(rock_group, canvas)

    # TODO: DONE In the draw handler, use your helper function process_sprite_group
    """
    to process missile_group. While you can now shoot multiple missiles, you will
    notice that they stick around forever. To fix this, we need to modify the
    Sprite class and the process_sprite_group function.
    """
    process_sprite_group(missile_group, canvas)

    # update ship and sprites
    my_ship.update()

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

    # TODO: In the draw handler, use the group_collide helper to determine if the
    """
    ship hit any of the rocks. If so, decrease the number of lives by one. Note
    that you could have negative lives at this point. Don't worry about that yet.
    """
    ship_collision = group_collide(rock_group, my_ship)
    if ship_collision:
        lives -= 1

    # TODO 4.2: Call group_group_collide in the draw handler to detect
    """
    missile/rock collisions. Increment the score by the number of missile collisions.
    """
    missile_hits = group_group_collide(missile_group, rock_group)
    if missile_hits > 0:
        score += missile_hits


# timer handler that spawns a rock
def rock_spawner():
    global rock_group

    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_avel = random.random() * .2 - .1
    # TODO DONE Remove a_rock and replace it with rock_group.
    """
    Initialize the rock group to an empty set. Modify your rock spawner to
    create a new rock (an instance of a Sprite object) and add it to rock_group.
    """
    if len(rock_group) < 12:
        rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))
    # TODO DONE Modify your rock spawner to limit the total number of rocks in the
    """
    game at any one time. We suggest you limit it to 12. With too many rocks
    the game becomes less fun and the animation slows down significantly.
    """


# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

rock_group = set([])
rock_spawner()

missile_group = set([])

# TODO: DONE Remove a_missile and replace it with missile_group.
"""
Initialize the missile group to an empty set.  Modify your shoot method of
my_ship to create a new missile (an instance of the Sprite class) and add
it to the missile_group. If you use our code, the firing sound should play
automatically each time a missile is spawned.
"""



# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
