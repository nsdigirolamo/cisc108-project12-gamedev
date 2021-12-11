# Project 12 - Game Development
# Date: Fall 2021
# Course: CISC108
# School: University of Delaware
# Author: Nicholas DiGirolamo

from designer import *
from math import sin, cos, radians
from random import randint, random

SPACESHIP_ACCELERATION = 0.5
SPACESHIP_TURN_SPEED = 10
SPACESHIP_SCALE = 0.075

LASER_SPEED = 10
LASER_SCALE = 0.025

ASTEROID_SPEED_LIMITER = 0.01
ASTEROID_SPAWN_RATE = 30
LARGE_ASTEROID_SCALE = 0.2
MEDIUM_ASTEROID_SCALE = 0.1
SMALL_ASTEROID_SCALE = 0.05

STAR_SPAWN_RATE = 200

Spaceship = {
    'sprite': DesignerObject,
    'x_speed': int,
    'y_speed': int,
    'is_turning_left': bool,
    'is_turning_right': bool,
    'is_accelerating': bool
    }

Laser = {
    'sprite': DesignerObject,
    'x_speed': int,
    'y_speed': int
    }

Asteroid = {
    'sprite': DesignerObject,
    'x_speed': int,
    'y_speed': int,
    'size': str,
    }

Star = {
    'sprite': DesignerObject
    }

World = {
    'spaceship': Spaceship,
    'lasers': [Laser],
    'asteroids': [Asteroid],
    'stars': [Star],
    'score': int,
    'score_text': DesignerObject,
    'game_over_text': DesignerObject,
    }


def create_world() -> World:
    """
    Creates a game world.

    Returns:
        World: The newly created game world.
    """
    set_window_color('black')

    return {
        'spaceship': create_spaceship(),
        'lasers': [],
        'asteroids': [],
        'stars': [],
        'score': 0,
        'score_text': create_score_text(),
        'game_over_text': create_game_over_text(),
        }


def create_spaceship() -> Spaceship:
    """
    Creates a spaceship.

    Returns:
        Spaceship: The newly created spaceship.
    """
    sprite = image('spaceship.png', get_width() / 2, get_height() / 2)
    sprite['scale'] = SPACESHIP_SCALE

    return {
        'sprite': sprite,
        'x_speed': 0,
        'y_speed': 0,
        'is_turning_left': False,
        'is_turning_right': False,
        'is_accelerating': False
        }


def start_spaceship_turning(world: World, key: str):
    """
    Starts turning the spaceship depending on user input.

    Args:
        world (World): The game world.
        key (str): The key input.
    """
    if key == 'a':
        world['spaceship']['is_turning_left'] = True

    if key == 'd':
        world['spaceship']['is_turning_right'] = True


def handle_spaceship_turning(world: World):
    """
    Turns the spaceship by increasing or decreasing its angle.

    Args:
        world (World): The game world.
    """
    if world['spaceship']['is_turning_left']:
        world['spaceship']['sprite']['angle'] += SPACESHIP_TURN_SPEED
    elif world['spaceship']['is_turning_right']:
        world['spaceship']['sprite']['angle'] -= SPACESHIP_TURN_SPEED


def stop_spaceship_turning(world: World, key: str):
    """
    Stops turning the spaceship depending on user input.

    Args:
        world (World): The game world.
        key (str): The key input.
    """
    if key == 'a':
        world['spaceship']['is_turning_left'] = False

    if key == 'd':
        world['spaceship']['is_turning_right'] = False


def start_spaceship_acceleration(world: World, key: str):
    """
    Starts accelerating the spaceship depending on user input.

    Args:
        world (World): The game world.
        key (str): The key input.
    """
    if key == 'w':
        world['spaceship']['is_accelerating'] = True


def handle_spaceship_acceleration(world: World):
    """
    Accelerates the spaceship in a direction determined by its angle.

    Args:
        world (World): The game world.
    """
    # Below adds 90 degrees to the angle to adjust the direction of 0 degrees.
    # By default 0 degrees is aligned up, so by adding 90 degrees we make it 
    # so that right is 0 degrees, up is 90 degrees, left is 180 degrees and 
    # down is 270 degrees.
    ship_angle = world['spaceship']['sprite']['angle'] + 90

    # I am bad at Trigonometry so this is like magic to me.
    # By using sin and cos, we can convert the angle of the ship into an
    # x and y direction and then accelerate the ship in those directions.
    if world['spaceship']['is_accelerating']:
        world['spaceship']['x_speed'] += SPACESHIP_ACCELERATION * cos(radians(ship_angle))
        world['spaceship']['y_speed'] -= SPACESHIP_ACCELERATION * sin(radians(ship_angle))


def stop_spaceship_acceleration(world: World, key: str):
    """
    Stops accelerating the spaceship depending on user input.

    Args:
        world (World): The game world.
        key (str): The key input.
    """
    if key == 'w':
        world['spaceship']['is_accelerating'] = False


def move_spaceship(world: World):
    """
    Moves the spaceship.

    Args:
        world (World): The game world.
    """
    world['spaceship']['sprite']['x'] += world['spaceship']['x_speed']
    world['spaceship']['sprite']['y'] += world['spaceship']['y_speed']


def wrap_spaceship_position(world: World):
    """
    Wraps the spaceship around to the other side of the screen if it collides
    with the border.

    Args:
        world (World): The game world.
    """
    x_position = world['spaceship']['sprite']['x']
    y_position = world['spaceship']['sprite']['y']

    if x_position > get_width():
        x_position = x_position % get_width()
    elif x_position < 0:
        x_position = get_width()

    if y_position > get_height():
        y_position = y_position % get_height()
    elif y_position < 0:
        y_position = get_height()

    world['spaceship']['sprite']['x'] = x_position
    world['spaceship']['sprite']['y'] = y_position
    

def spaceship_asteroid_collide(world: World) -> bool:
    """
    Checks to see if any asteroids have collided with the spaceship.

    Args:
        world (World): The game world.
    Returns:
        bool: Whether or not any collisions were found.
    """
    spaceship_x = world['spaceship']['sprite']['x']
    spaceship_y = world['spaceship']['sprite']['y']

    for asteroid in world['asteroids']:
        # A collision with the spaceship is only detected if the asteroid
        # collides with the center of the spaceship. This allows the players
        # to get a bit closer to asteroids without losing the game.
        if colliding(asteroid['sprite'], spaceship_x, spaceship_y):
            show_game_over_text(world)
            return True


def create_laser(x_position: int, y_position: int, angle: float) -> Laser:
    """
    Creates a new laser projectile.

    Args:
        x_position (int): The initial x position of the laser.
        y_position (int): The initial y position of the laser.
    Returns:
        Laser: The newly created laser.
    """
    sprite = image('laser.png', x_position, y_position)
    sprite['scale'] = LASER_SCALE

    x_speed = LASER_SPEED * cos(radians(angle + 90))
    y_speed = LASER_SPEED * sin(radians(angle + 90))

    return {
        'sprite': sprite,
        'x_speed': x_speed,
        'y_speed': y_speed,
        }


def spawn_laser(world: World, key: str):
    """
    Creates a new laser depending on user input.

    Args:
        world (World): The game world.
        key (str): The input key.
    """
    x_position = world['spaceship']['sprite']['x']
    y_position = world['spaceship']['sprite']['y']
    angle = world['spaceship']['sprite']['angle']

    if key == 'space':
        world['lasers'].append(create_laser(x_position, y_position, angle))


def move_lasers(world: World):
    """
    Controls movement for all lasers in the given world.

    Args:
        world (World): The game world.
    """
    for laser in world['lasers']:
        laser['sprite']['x'] += laser['x_speed']
        laser['sprite']['y'] -= laser['y_speed']


def handle_laser_asteroid_collide(world: World):
    """
    Deletes a laser and an asteroid once they collide, and spawns 4 new
    smaller asteroids if the asteroid wasn't small.

    Args:
        world (World): The game world.
    """
    new_lasers = []
    new_asteroids = []

    lasers_for_deletion = []
    asteroids_for_deletion = []

    laser_count = 0
    asteroid_count = 0

    collision = False

    # Looks at every laser and asteroid and checks for collisisons.
    # Collided objects are recorded in lasers_for_deletion and asteroids_for_deletion.
    for laser in world['lasers']:
        for asteroid in world['asteroids']:
            if colliding(laser['sprite'], asteroid['sprite']):
                lasers_for_deletion.append(laser_count)
                asteroids_for_deletion.append(asteroid_count)
            asteroid_count += 1
        asteroid_count = 0
        laser_count += 1

    laser_count = 0
    asteroid_count = 0

    # This loop creates a new list of lasers without the ones marked for deletion
    for laser in world['lasers']:
        if laser_count not in lasers_for_deletion:
            new_lasers.append(laser)
        laser_count += 1

    # This looop creates a new list of asteroids. Any asteroids marked for deletion
    # are replaces by 4 smaller asteroids.
    for asteroid in world['asteroids']:
        if asteroid_count not in asteroids_for_deletion:
            new_asteroids.append(asteroid)
        else:
            new_asteroids = new_asteroids + divide_asteroid(asteroid) 
        asteroid_count += 1

    world['asteroids'] = new_asteroids
    world['lasers'] = new_lasers


def create_asteroid(x_position: int, y_position: int, x_speed: int, y_speed: int, size: str) -> Asteroid:
    """
    Creates a new asteroid.

    Args:
        x_position (int): The intial x position of the asteroid.
        y_position (int): The intial y position of the asteroid.
        x_speed (int): The intial x speed of the asteroid.
        y_speed (int): The intial y speed of the asteroid.
    Returns:
        Asteroid: The newly created asteroid.
    """
    sprite = image('asteroid.png', x_position, y_position)

    if size == 'big':
        sprite['scale'] = LARGE_ASTEROID_SCALE
    elif size == 'medium':
        sprite['scale'] = MEDIUM_ASTEROID_SCALE
    elif size == 'small':
        sprite['scale'] = SMALL_ASTEROID_SCALE

    return {
        'sprite': sprite,
        'size': size,
        'x_speed': x_speed,
        'y_speed': y_speed
        }


def spawn_asteroid(world: World):
    """
    Randomly determines when to create a new asteroid.

    Args:
        world (World): The game world.
    """
    if randint(0, ASTEROID_SPAWN_RATE) == 0:
        # Looks for points in an area 100 pixels larger than the game screen
        # in every direction.
        x_position = randint(-50, get_width() + 100)
        y_position = randint(-50, get_height() + 100)

        # Checks if the points are outside the game screen.
        x_is_outside = x_position < 0 or x_position > get_width()
        y_is_outside = y_position < 0 or y_position > get_height()

        if x_is_outside or y_is_outside:
            # Set the asteroid's speeds so it moves towards the middle of the
            # screen and randomizes the speeds so they don't congregate in the
            # dead center.
            x_speed = random() * (get_width()/2 - x_position)
            y_speed = random() * (get_height()/2 - y_position)

            # Slow the asteroids down
            x_speed = x_speed * ASTEROID_SPEED_LIMITER
            y_speed = y_speed * ASTEROID_SPEED_LIMITER

            world['asteroids'].append(create_asteroid(x_position, y_position, x_speed, y_speed, 'big'))


def divide_asteroid(asteroid: Asteroid) -> Asteroid:
    """
    Divides an asteroid into 4 smaller asteroids.

    Args:
        asteroid (Asteroid): The asteroid to be divided.
    Returns:
        Asteroid: A list of 4 smaller asteroids.
    """

    new_asteroids = []
    x_position = asteroid['sprite']['x']
    y_position = asteroid['sprite']['y']

    if asteroid['size'] == 'big':
        new_asteroids.append(create_asteroid(x_position, y_position, 5, 0, 'medium'))
        new_asteroids.append(create_asteroid(x_position, y_position, -5, 0, 'medium'))
        new_asteroids.append(create_asteroid(x_position, y_position, 0, 5, 'medium'))
        new_asteroids.append(create_asteroid(x_position, y_position, 0, -5, 'medium'))
    elif asteroid['size'] == 'medium':
        new_asteroids.append(create_asteroid(x_position, y_position, 5, 0, 'small'))
        new_asteroids.append(create_asteroid(x_position, y_position, -5, 0, 'small'))
        new_asteroids.append(create_asteroid(x_position, y_position, 0, 5, 'small'))
        new_asteroids.append(create_asteroid(x_position, y_position, 0, -5, 'small'))

    return new_asteroids


def move_asteroids(world: World):
    """
    Controls movement for all asteroids in the given world.

    Args:
        world (World): The game world.
    """
    for asteroid in world['asteroids']:
        asteroid['sprite']['x'] += asteroid['x_speed']
        asteroid['sprite']['y'] += asteroid['y_speed']


def create_star(x_position: int, y_position: int) -> Star:
    """
    Creates a new star.

    Args:
        x_position (int): The x position of the star.
        y_position (int): The y position of the star.
    Returns:
        Star: The newly created star.
    """
    sprite = image('star.png', x_position, y_position)
    sprite['scale'] = 0.1

    return {
        'sprite': sprite,
        }


def spawn_star(world: World):
    """
    Randomly determines when to create a new star.

    Args:
        world (World): The game world.
    """
    if randint(0, STAR_SPAWN_RATE) == 0:
        x_position = randint(0, get_width())
        y_position = randint(0, get_height())

        world['stars'].append(create_star(x_position, y_position))


def handle_spaceship_star_collide(world: World):
    """
    Removes a star once the spaceship collides with it, and then updates the
    score.

    Args:
        world (World): The game world.
    """
    spaceship = world['spaceship']
    new_stars = []

    for star in world['stars']:
        if colliding(spaceship['sprite'], star['sprite']):
            world['score'] += 1
            world['score_text']['text'] = "Score: " + str(world['score'])
        else:
            new_stars.append(star)

    world['stars'] = new_stars


def create_score_text() -> DesignerObject:
    """
    Creates the score text.

    Returns:
        DesignerObject: The newly created text.
    """
    score = text('yellow', "Score: 0", 24, get_width() / 2, 50)
    return score


def create_game_over_text() -> DesignerObject:
    """
    Creates the "GAME OVER!" text.

    Returns:
        DesignerObject: The newly created text.
    """
    game_over_text = text('red', 'GAME OVER!', 48, get_width() / 2, get_height() / 2)
    game_over_text['visible'] = False
    return game_over_text


def show_game_over_text(world: World):
    """
    Makes the "GAME OVER!" text visible.

    Args:
        world (World): The game world.
    """
    world['game_over_text']['visible'] = True


when(
    'starting',
    create_world
    )

when(
    'typing',
    start_spaceship_acceleration,
    start_spaceship_turning
    )

when(
    'done typing',
    stop_spaceship_acceleration,
    stop_spaceship_turning,
    spawn_laser
    )

when(
    'updating',
    move_spaceship,
    wrap_spaceship_position,
    move_lasers,
    handle_laser_asteroid_collide,
    spawn_asteroid,
    move_asteroids,
    spawn_star,
    handle_spaceship_star_collide,
    handle_spaceship_acceleration,
    handle_spaceship_turning,
    )

when(
    spaceship_asteroid_collide,
    pause
    )

start()
