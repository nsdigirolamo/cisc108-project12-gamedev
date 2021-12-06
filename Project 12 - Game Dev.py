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

ASTEROID_SPEED_LIMITER = 0.01
ASTEROID_SPAWN_RATE = 25

STAR_SPAWN_RATE = 100

Spaceship = {
    'sprite': DesignerObject,
    'x_speed': int,
    'y_speed': int,
    'is_turning_left': bool,
    'is_turning_right': bool,
    'is_accelerating': bool
    }

Asteroid = {
    'sprite': DesignerObject,
    'x_speed': int,
    'y_speed': int,
    }

Star = {
    'sprite': DesignerObject
    }

World = {
    'spaceship': Spaceship,
    'asteroids': [Asteroid],
    'stars': [Star],
    'score': int,
    'score_text': DesignerObject,
    'game_over_text': DesignerObject
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
        'asteroids': [],
        'stars': [],
        'score': 0,
        'score_text': create_score_text(),
        'game_over_text': create_game_over_text()
        }


def create_spaceship() -> Spaceship:
    """
    Creates a spaceship.

    Returns:
        Spaceship: The newly created spaceship.
    """
    sprite = image('spaceship.png', get_width() / 2, get_height() / 2)
    sprite['scale'] = 0.075

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
    Takes user input for turning the spaceship. Sets the state of the
    dictionary's is_turning_left or is_turning_right values to True depending
    on the key input.

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
    Turns the spaceship. Increases or decreases the angle of the spaceship
    depending on the state of the dictionary's is_turning_left and
    is_turning_right values.

    Args:
        world (World): The game world.
    """
    if world['spaceship']['is_turning_left']:
        world['spaceship']['sprite']['angle'] += SPACESHIP_TURN_SPEED
    elif world['spaceship']['is_turning_right']:
        world['spaceship']['sprite']['angle'] -= SPACESHIP_TURN_SPEED


def stop_spaceship_turning(world: World, key: str):
    """
    Takes user input for turning the spaceship. Sets the state of the
    dictionary's is_turning_left or is_turning_right values to False depending
    on the key input.

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
    Takes user input for accelerating the spaceship. Sets the state of the
    dictionary's is_accelerating values to True depending on the key input.

    Args:
        world (World): The game world.
        key (str): The key input.
    """
    if key == 'w':
        world['spaceship']['is_accelerating'] = True


def handle_spaceship_acceleration(world: World):
    """
    Accelerates the spaceship. Acceleration occurs depending on the state of
    the dictionary's is_accelerating value. The rate of acceleration is
    decided by SPACESHIP_ACCELERATION

    Args:
        world (World): The game world.
    """
    # Below adds 90 degrees to the angle to fix the direction of 0 degrees.
    # By default 0 degrees is aligned to north (up) so by adding 90 degrees
    # we make it so that east is 0 degrees, north is 90 degrees, west is 180
    # degrees, south is 270 degrees, etc.
    ship_angle = world['spaceship']['sprite']['angle'] + 90

    # I am bad at Trigonometry so this is like magic to me.
    # By using sin and cos, we can convert the angle of the ship into an
    # x and y direction and then accelerate the ship in those directions.
    if world['spaceship']['is_accelerating']:
        world['spaceship']['x_speed'] += SPACESHIP_ACCELERATION * cos(radians(ship_angle))
        world['spaceship']['y_speed'] -= SPACESHIP_ACCELERATION * sin(radians(ship_angle))


def stop_spaceship_acceleration(world: World, key: str):
    """
    Takes user input for accelerating the spaceship. Sets the state of the
    dictionary's is_accelerating values to False depending on the key input.

    Args:
        world (World): The game world.
        key (str): The key input.
    """
    if key == 'w':
        world['spaceship']['is_accelerating'] = False


def move_spaceship(world: World):
    """
    Moves the spaceship by increasing or decreasing the spaceship's x and y
    positions by the amount of their respective speeds.

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


def create_asteroid(x_position: int, y_position: int, x_speed: int, y_speed: int) -> Asteroid:
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
    sprite['scale'] = 0.2

    return {
        'sprite': sprite,
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

            world['asteroids'].append(create_asteroid(x_position, y_position, x_speed, y_speed))


def move_asteroids(world: World):
    """
    Controls movement for all asteroids in the given world.

    Args:
        world (World): The game world.
    """
    for asteroid in world['asteroids']:
        asteroid['sprite']['x'] += asteroid['x_speed']
        asteroid['sprite']['y'] += asteroid['y_speed']


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
    Updates the score when a star collides with the spaceship.

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
    stop_spaceship_turning
    )

when(
    'updating',
    move_spaceship,
    wrap_spaceship_position,
    spawn_asteroid,
    move_asteroids,
    spawn_star,
    handle_spaceship_star_collide,
    handle_spaceship_acceleration,
    handle_spaceship_turning
    )

when(
    spaceship_asteroid_collide,
    pause
    )

start()
