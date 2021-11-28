"""
Project 12 - Game Development
A clone of the famous "Asteroids" arcade game.

Date: Spring 2020
Course: CISC108
School: University of Delaware
Author: Nicholas DiGirolamo
"""

from designer import *
from math import sin, cos, radians
from random import randint, random

SPACESHIP_ACCELERATION = 1
SPACESHIP_TURN_SPEED = 15

ASTEROID_SPEED_LIMITER = 0.01
ASTEROID_SPAWN_RATE = 25

Asteroid = {
    'asteroid': DesignerObject,
    'asteroid_x_speed': int,
    'asteroid_y_speed': int,
    }

World = {
    'spaceship': DesignerObject,
    'spaceship_x_speed': int,
    'spaceship_y_speed': int,
    'asteroids': [Asteroid]
    }

def create_world() -> World:
    """
    Creates the game world.
    
    Returns:
        World: A newly created game world with its components.
    """
    set_window_color('black')
    
    return {
        'spaceship': create_spaceship(),
        'spaceship_x_speed': 0,
        'spaceship_y_speed': 0,
        'asteroids': []
        }

def create_spaceship() -> DesignerObject:
    """
    Creates the spaceship using appropriate adjustments.
    
    Returns:
        DesignerObject: The newly created spaceship.
    """
    spaceship = image('spaceship.png', get_width() / 2, get_height() / 2)
    spaceship['scale'] = 0.075
    return spaceship


def turn_spaceship(world: World, key: str):
    """
    Turns the spaceship. Increases or decreases the angle
    of the spaceship depending on user input.
    
    Args:
        world (World): The game world.
        key (str): The key pressed by the user.
    """
    if key == 'a':
        world['spaceship']['angle'] += SPACESHIP_TURN_SPEED
    elif key == 'd':
        world['spaceship']['angle'] -= SPACESHIP_TURN_SPEED
        
        
def accelerate_spaceship(world: World, key: str):
    """
    Accelerates the spaceship in the direction it's currently pointing. Applies SPACESHIP_ACCELERATION to
    the spaceship_x_speed and spaceship_y_speed.
    
    Args:
        world (World): The game world.
        key (str): The key pressed by the user.
    """
    # Below adds 90 degrees to the angle to fix the direction of 0 degrees.
    # By default 0 degrees is aligned to north (up) so by adding 90 degrees we make it so that
    # east is 0 degrees, north is 90 degrees, west is 180 degrees, south is 270 degrees, etc.
    ship_angle = world['spaceship']['angle'] + 90
    
    # I am bad at Trigonometry so this is like magic to me.
    # By using sin and cos, we can convert the angle of the ship into an x and y direction
    # and then accelerate the ship in those directions.
    if key == 'w':
        world['spaceship_x_speed'] += SPACESHIP_ACCELERATION * cos(radians(ship_angle))
        world['spaceship_y_speed'] -= SPACESHIP_ACCELERATION * sin(radians(ship_angle))


def move_spaceship(world: World):
    """
    Moves the spaceship by increasing or decreasing the spaceship's
    x and y positions by the amount of their respective speeds.
    
    Args:
        world (World): The game world.
    """
    world['spaceship']['x'] += world['spaceship_x_speed']
    world['spaceship']['y'] += world['spaceship_y_speed']
    
    
def wrap_spaceship_position(world: World):
    """
    Wraps the spaceship around to the other side of the screen if it collides with the border.
    
    Args:
        world (World): The game world.
    """
    if world['spaceship']['x'] > get_width():
        world['spaceship']['x'] = world['spaceship']['x'] % get_width()
    elif world['spaceship']['x'] < 0:
        world['spaceship']['x'] = get_width()
        
    if world['spaceship']['y'] > get_height():
        world['spaceship']['y'] = world['spaceship']['y'] % get_height()
    elif world['spaceship']['y'] < 0:
        world['spaceship']['y'] = get_height()
        

def create_asteroid(x_pos: int, y_pos: int, x_speed: int, y_speed: int) -> Asteroid:
    """
    Creates a new asteroid dictionary.
    
    Args:
        x_pos (int): The intial x position of the asteroid.
        y_pos (int): The intial y position of the asteroid.
        x_speed (int): The intial x speed of the asteroid.
        y_speed (int): The intial y speed of the asteroid.
    Returns:
        Asteroid: The newly created asteroid.
    """
    asteroid = image('asteroid.png', x_pos, y_pos)
    asteroid['scale'] = 0.2
    
    return {
        'x_speed': x_speed,
        'y_speed': y_speed,
        'asteroid': asteroid
        }

def spawn_asteroid(world: World):
    """
    Randomly spawns a new asteroid. Most aspects of the asteroid will be randomly determined.
    
    Args:
        world (World): The game world.
    """
    if randint(0, ASTEROID_SPAWN_RATE) == 0:
        # Looks for points in an area 50 pixels larger than the game screen in every direction.
        x_position = randint(-50, get_width() + 50)
        y_position = randint(-50, get_height() + 50)
        
        # Checks if the points are outside the game screen.
        x_is_outside = x_position < 0 or x_position > get_width()
        y_is_outside = y_position < 0 or y_position > get_height()
    
        if x_is_outside or y_is_outside:
            # Set the asteroid's speeds so it moves towards the middle of the screen.
            # Randomizes the speeds so they don't congregate in the dead center.
            x_speed = random() * (get_width()/2 - x_position)
            y_speed = random() * (get_height()/2 - y_position)
        
            # Slow the asteroids down
            x_speed = x_speed * ASTEROID_SPEED_LIMITER
            y_speed = y_speed * ASTEROID_SPEED_LIMITER
        
            world['asteroids'].append(create_asteroid(x_position, y_position, x_speed, y_speed))
        
def move_asteroids(world: World):
    """
    Moves all asteroids in the world. Since the asteroids are their own dictionary, they each have
    a uniqe speed that influences their position.
    
    Args:
        world (World): The game world.
    """
    # asteroid['asteroid']['x'] is confusing syntax. Asteroid (the dictionary) contains a DesignerObject called "asteroid"
    # and that DesignerObject has its own x and y components. I might need to change up the key names in my Asteroid
    # dictionary to make this a bit more clear about what exactly is going on. Alternatively, I could just change the
    # name of the Asteroid dictionary in this for loop!
    for asteroid in world['asteroids']:
        asteroid['asteroid']['x'] += asteroid['x_speed']
        asteroid['asteroid']['y'] += asteroid['y_speed']
        
    
enable_keyboard_repeating()        
when('starting', create_world)
when('updating', move_spaceship, wrap_spaceship_position, spawn_asteroid, move_asteroids)
when('typing', turn_spaceship, accelerate_spaceship)

start()