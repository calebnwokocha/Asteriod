"""
File: asteroids.py
Original Author: Br. Burton
Co-author: Caleb Nwokocha
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import math
import random
from abc import ABC, abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

class Point():
    def __init__(self):
        '''Intialize x and y coordinates of an object.'''
        self._x = 0.0
        self._y = 0.0
        
    def set_x(self, value):
        '''Set x coordinate of an object.'''
        self._x = value
    
    def set_y(self, value):
        '''Set y coordinate of an object.'''
        self._y = value
    
    def get_x(self):
        '''Return x coordinate of an object.'''
        return self._x
    
    def get_y(self):
        '''Return y coordinate of an object.'''
        return self._y
    
class Velocity():
    def __init__(self):
        '''Intialize rate of change of x and y coordinates.'''
        self._dx = 0.0
        self._dy = 0.0
        
    def set_dx(self, value):
        '''Set rate of change of the x coordinate of an object.'''
        self._dx += value
    
    def set_dy(self, value):
        '''Set rate of change of the y coordinate of an object.'''
        self._dy += value
        
    def get_dx(self):
        '''Return rate of change of the x coordinate of an object.'''
        return self._dx
    
    def get_dy(self):
        '''Return rate of change of the y coordinate of an object.'''
        return self._dy
   
class FlyingObject():
    def __init__(self):
        self._angle = 90
        self.center = Point()
        self.velocity = Velocity()
        self._radius = 0
        self.alive = True
        self._alpha = 255 # For transparency, 1 means not transperent
        
    def set_vector(self, x_value, y_value):
        '''Set vector of a flying object.'''
        self.center.set_x(x_value)
        self.center.set_y(y_value)
        
    def set_velocity(self, dx_value, dy_value):
        '''Set velocity of a flying object.'''
        self.velocity.set_dx(dx_value)
        self.velocity.set_dy(dy_value)
    
    def set_angle(self, value):
        '''Set angle of a flying object.'''
        if self._angle > 360:
            self._angle = 0
        
        if self._angle < -360:
            self._angle = 0
            
        self._angle += value
    
    def get_angle(self):
        '''Return angle of a flying object.'''
        return self._angle
        
    def advance(self):
        '''Change position of flying object.'''
        self.set_vector(self.center.get_x() + self.velocity.get_dx(), self.center.get_y() + self.velocity.get_dy())
        
    def is_off_screen(self, screen_width, screen_height):
        '''Check whether flying object is off screen.'''
        if self.center.get_x() > screen_width or self.center.get_y() > screen_height:
            return True
        elif self.center.get_x() < 0 or self.center.get_y() < 0:
            return True
        else:
            return False

class Ship(FlyingObject):
    def __init__(self):
        '''Intialize ship attributes.'''
        super().__init__()
        self.radius = SHIP_RADIUS
        self.turn_amount = SHIP_TURN_AMOUNT
        self.thrust_amount = SHIP_THRUST_AMOUNT
        self.alive = True
        self._img = "images/playerShip1_orange.png"
        self._texture = arcade.load_texture(self._img)
        self._width = self._texture.width
        self._height = self._texture.height
        
        # Set ship initial position
        self.set_vector(SCREEN_WIDTH / 2, SCREEN_WIDTH - SCREEN_HEIGHT)
        
    def draw(self):
        '''Display ship on screen.'''
        if self.alive:
            arcade.draw_texture_rectangle(self.center.get_x(), self.center.get_y(), self._width, self._height, self._texture, self._angle, self._alpha)
        
    def accelerate(self, ddx, ddy):
        '''Cause change to the ship velocity.'''
        self.set_velocity(ddx, ddy)
        
class Bullet(FlyingObject):
    def __init__(self):
        '''Intialize bullet attributes.'''
        super().__init__()
        self._speed = BULLET_SPEED
        self.radius = BULLET_RADIUS
        self._life = 0
        self._img = "images/laserBlue01.png"
        self._texture = arcade.load_texture(self._img)
        self._width = self._texture.width
        self._height = self._texture.height
        self._alpha = 0
        self.is_fired = False
        self._angle = 0
        
        # Set bullet initial position.
        self.set_vector(SCREEN_WIDTH / 2, SCREEN_WIDTH - SCREEN_HEIGHT)
    
    def draw(self):
        '''Display bullet on screen.'''
        arcade.draw_texture_rectangle(self.center.get_x(), self.center.get_y(), self._width, self._height, self._texture, self._angle, self._alpha)
    
    def advance(self):
        '''Chang position of bullet.'''
        self.set_vector(self.center.get_x() + self.velocity.get_dx(), self.center.get_y() + self.velocity.get_dy())
        
        # In bullet life to 60. Bullet is dead after 60 frames.
        self._life += 1
        if self._life == BULLET_LIFE:
            self.alive = False
    
    def fire(self, angle):
        '''Fire bullet from ship.'''
        self._alpha = 255
        self.set_velocity(math.cos(math.radians(angle)) * self._speed, math.sin(math.radians(angle)) * self._speed)
        self.is_fired = True        
        
class Asteriods(ABC):
    def __init__(self):
        '''Intialize asteriod attributes'''
        self.center = Point()
        self.velocity = Velocity()
        self._rock_count = 0
        self._is_hit = False
        self._angle = 0
        self.radius = 0
        self.alive = True
        self.is_hit = False
        self._is_split = False
        
    @abstractmethod
    def draw(self):
        '''Display asteriod on screen.'''
        pass
    
    @abstractmethod
    def advance(self):
        '''Change position of asteriod.'''
        pass
    
    @abstractmethod
    def split(self):
        '''Split asteriod into smaller parts.'''
        pass
        
    @abstractmethod
    def is_off_screen(self, screen_width, screen_height):
        '''Check whether asteriod is off screen.'''
        pass
    
class Large_Asteriods(Asteriods):
    def __init__(self):
        '''Intialize large asteriod attributes.'''
        super().__init__()
        self._rock_count = 0
        self._is_hit = False
        self.radius = BIG_ROCK_RADIUS
        self._speed = 0.0
        self._spin = 0
        self._img = "images/meteorGrey_big1.png"
        self._texture = arcade.load_texture(self._img)
        self._width = self._texture.width
        self._height = self._texture.height
        self._alpha = 255
        self.is_large = True
        self.is_medium = False
        self.is_small = False
        
        # Set initial vector and velocity of large asteriod.
        self.set_vector(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.set_velocity(BIG_ROCK_SPEED * random.randint(-1, 1), BIG_ROCK_SPEED * random.randint(-1, 1))
         
    def set_vector(self, x_value, y_value):
        '''Set vector of large asteriod.'''
        self.center.set_x(x_value)
        self.center.set_y(y_value)
     
    def set_velocity(self, dx_value, dy_value):
        '''Set velocity of small asteriod.'''
        self.velocity.set_dx(dx_value)
        self.velocity.set_dy(dy_value)
        
    def draw(self):
        '''Display large asteriod on screen.'''
        arcade.draw_texture_rectangle(self.center.get_x(), self.center.get_y(), self._width, self._height, self._texture, self._angle, self._alpha)
        
    def advance(self):
        '''Change position of large asteriod.'''
        self._angle += BIG_ROCK_SPIN
        self.set_vector(self.center.get_x() + self.velocity.get_dx(), self.center.get_y() + self.velocity.get_dy())
     
    def split(self):
        '''Split large asteriod into two medium asteriods and one small asteriod.'''
        self._is_split = True
        self.alive = False
        
    def is_off_screen(self, screen_width, screen_height):
        '''Check whether large asteriod is off screen.'''
        if self.center.get_x() > screen_width or self.center.get_y() > screen_height:
            return True
        elif self.center.get_x() < 0 or self.center.get_y() < 0:
            return True
        else:
            return False

class Medium_Asteriods(Asteriods):
    def __init__(self):
        '''Intialize medium asteriod attributes'''
        super().__init__()
        self._rock_count = 0
        self._is_hit = False
        self._radius = 0
        self._spin = 0
        self._img = "images/meteorGrey_med1.png"
        self._texture = arcade.load_texture(self._img)
        self._width = self._texture.width
        self._height = self._texture.height
        self._alpha = 255
        self.is_large = False
        self.is_medium = True
        self.is_small = False
        
        self.small_asteriod_1 = Small_Asteriods()
        self.small_asteriod_2 = Small_Asteriods()
        
    def set_vector(self, x_value, y_value):
        '''Set vector of medium asteriod.'''
        self.center.set_x(x_value)
        self.center.set_y(y_value)
     
    def set_velocity(self, dx_value, dy_value):
        '''Set velocity of medium asteriod.'''
        self.velocity.set_dx(dx_value)
        self.velocity.set_dy(dy_value)
        
    def draw(self):
        '''Display medium asteriod on screen.'''
        arcade.draw_texture_rectangle(self.center.get_x(), self.center.get_y(), self._width, self._height, self._texture, self._angle, self._alpha)
 
    def advance(self):
        '''Change position of medium asteriod.'''
        self._angle += MEDIUM_ROCK_SPIN
        self.set_vector(self.center.get_x() + self.velocity.get_dx(), self.center.get_y() + self.velocity.get_dy())
    
    def split(self):
        '''Split medium asteriod into two small asteriods.'''
        self._is_split = True
        self.alive = False
        
    def is_off_screen(self, screen_width, screen_height):
        '''Check whether medium asteriod is off screen.'''
        if self.center.get_x() > screen_width or self.center.get_y() > screen_height:
            return True
        elif self.center.get_x() < 0 or self.center.get_y() < 0:
            return True
        else:
            return False
    
class Small_Asteriods(Asteriods):
    def __init__(self):
        '''Intialize small asteriod attributes'''
        super().__init__()
        self._rock_count = 0
        self._is_hit = False
        self._radius = 0
        self._spin = 0
        self._img = "images/meteorGrey_small1.png"
        self._texture = arcade.load_texture(self._img)
        self._width = self._texture.width
        self._height = self._texture.height
        self._alpha = 255
        self.is_large = False
        self.is_medium = False
        self.is_small = True
        
    def set_vector(self, x_value, y_value):
        '''Set vector of small asteriod.'''
        self.center.set_x(x_value)
        self.center.set_y(y_value)
     
    def set_velocity(self, dx_value, dy_value):
        '''Set velocity of small asteriod.'''
        self.velocity.set_dx(dx_value)
        self.velocity.set_dy(dy_value)
        
    def draw(self):
        '''Display small asteriod on screen.'''
        arcade.draw_texture_rectangle(self.center.get_x(), self.center.get_y(), self._width, self._height, self._texture, self._angle, self._alpha)
    
    def advance(self):
        '''Change position of medium asteriod.'''
        self._angle += SMALL_ROCK_SPIN
        self.set_vector(self.center.get_x() + self.velocity.get_dx(), self.center.get_y() + self.velocity.get_dy())
        
    def split(self):
        '''Delete small asteriod'''
        self.alive = False
        
    def is_off_screen(self, screen_width, screen_height):
        '''Check whether small asteriod is off screen.'''
        if self.center.get_x() > screen_width or self.center.get_y() > screen_height:
            return True
        elif self.center.get_x() < 0 or self.center.get_y() < 0:
            return True
        else:
            return False

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.ship = Ship()
        self.bullet = Bullet()
        self.bullets = []
        self.new_angle = 0
        self.asteriods = []
        
        self.load_asteriods()
               
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        self.ship.draw()

        for bullet in self.bullets:
            bullet.draw()
            
        for asteriod in self.asteriods:
            asteriod.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        # TODO: Tell everything to advance or move forward one step in time
        self.ship.advance()
        
        for bullet in self.bullets:
            bullet.advance()
        
        for asteriod in self.asteriods:
            asteriod.advance()
                
        # TODO: Check for keys, off-screen objects, zombies, and collisions
        self.check_keys() 
        self.check_off_screen()
        self.cleanup_zombies()
        self.check_collisions()

    # Display 5 large asteriods when game start. 
    def load_asteriods(self):
        for asteriod in range(INITIAL_ROCK_COUNT):
            large_asteriods = Large_Asteriods()
            self.asteriods.append(large_asteriods)
    
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            # Reset ship angle then increment angle by 3
            if self.new_angle >= 0:
                self.new_angle = 0
            self.new_angle += self.ship.turn_amount
            
            # Increment ship angle in anti-clockwise direction
            self.ship.set_angle(self.new_angle)
            
        if arcade.key.RIGHT in self.held_keys:
            # Reset ship angle then decrement angle by 3
            if self.new_angle <= 0:
                self.new_angle = 0
            self.new_angle -= self.ship.turn_amount                           
            
            # Increment ship angle in clockwise direction
            self.ship.set_angle(self.new_angle)
               
        if arcade.key.UP in self.held_keys:
            # Accelerate ship.
            self.ship.accelerate(self.ship.thrust_amount / math.tan(abs(math.radians(self.ship.get_angle()))), self.ship.thrust_amount)

        if arcade.key.DOWN in self.held_keys:
            # Deaccelerate ship.
            self.ship.accelerate(self.ship.thrust_amount / math.tan(abs(math.radians(self.ship.get_angle()))), (self.ship.thrust_amount) * -1)

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
            #for bullet in self.bullets:
                #bullet.fire(self.ship.get_angle())
        
    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet()
                self.bullets.append(bullet)
                
                # Set bullet angle and vector corresponding to that of the ship.
                if not self.bullets[0].is_fired:
                    self.bullets[0].set_angle(self.ship.get_angle())
                    self.bullets[0].set_vector(self.ship.center.get_x(), self.ship.center.get_y())
                
                # Fire!
                self.bullets[0].fire(self.ship.get_angle())

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
            
    def check_off_screen(self):
        """
        Checks to see if ship or bullets or asteriods have left the screen
        and if so, display ship or asteriod on opposite side of the screen 
        corresponding to where they left. For bullet, reset its position .
        :return:
        """
        if self.ship.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
            if self.ship.center.get_y() >= SCREEN_HEIGHT:
                self.ship.center.set_y(0)
            elif self.ship.center.get_y() <= 0:
                self.ship.center.set_y(SCREEN_HEIGHT)
                
        if self.ship.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
            if self.ship.center.get_x() >= SCREEN_WIDTH:
                self.ship.center.set_x(0)
            elif self.ship.center.get_x() <= 0:
                self.ship.center.set_x(SCREEN_WIDTH)
                
        for asteriod in self.asteriods:
            if asteriod.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                if asteriod.center.get_y() >= SCREEN_HEIGHT:
                    asteriod.center.set_y(0)
                elif asteriod.center.get_y() <= 0:
                    asteriod.center.set_y(SCREEN_HEIGHT)
           
        for asteriod in self.asteriods:
            if asteriod.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                if asteriod.center.get_x() >= SCREEN_WIDTH:
                    asteriod.center.set_x(0)
            elif asteriod.center.get_x() <= 0:
                asteriod.center.set_x(SCREEN_WIDTH)
        
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                if bullet.center.get_x() >= SCREEN_WIDTH:
                    bullet.center.set_x(0)
                elif bullet.center.get_x() <= 0:
                    bullet.center.set_x(SCREEN_WIDTH)
                    
                if bullet.center.get_y() >= SCREEN_HEIGHT:
                    bullet.center.set_y(0)
                elif bullet.center.get_y() <= 0:
                    bullet.center.set_y(SCREEN_HEIGHT)

    def cleanup_zombies(self):
        """
        Removes any dead bullets or asteriods from the list.
        :return:
        """
        # Check for dead bullets and remove them.
        for bullet in self.bullets: 
            if not bullet.alive:
                self.bullets.remove(bullet)
                
        # Instantiate group 1 asteriods that would replace a large asteriod when it's dead/split.        
        medium_asteriod_1 = Medium_Asteriods()
        medium_asteriod_2 = Medium_Asteriods()
        small_asteriod = Small_Asteriods()
        
        # Instantiate group 2 asteriods that would replace a medium asteriod when it's dead/split.
        small_asteriod_1 = Small_Asteriods()
        small_asteriod_2 = Small_Asteriods()
        
        # For all asteriod in the game:
        for asteriod in self.asteriods:
            # Check whether asteriod is not dead and whether it is a large asteriod.
            # If asteriod is dead and is a large one: 
            if not asteriod.alive and asteriod.is_large:
                # Set vectors of the intantiated group 1 asteriods.
                medium_asteriod_1.set_vector(asteriod.center.get_x() + 20, asteriod.center.get_y() + 20)
                medium_asteriod_2.set_vector(asteriod.center.get_x() - 20, asteriod.center.get_y() - 20)
                small_asteriod.set_vector(asteriod.center.get_x() + 20, asteriod.center.get_y() - 20)
                
                # Set velocity of the intantiated group 1 asteriods.
                medium_asteriod_1.set_velocity(asteriod.velocity.get_dx() + 2, asteriod.velocity.get_dy() + 2)
                medium_asteriod_2.set_velocity((asteriod.velocity.get_dx() + 2) * -1, (asteriod.velocity.get_dy() + 2) * -1)
                small_asteriod.set_velocity(asteriod.velocity.get_dx() + 2, 0)
                
                # Remove dead large asteriod from the game.
                self.asteriods.remove(asteriod)
                
                # Put group 1 asteriods in the game.
                self.asteriods.append(medium_asteriod_1)
                self.asteriods.append(medium_asteriod_2)
                self.asteriods.append(small_asteriod)
                
            # Otherwise, if asteriod is dead and is a medium one: 
            elif not asteriod.alive and asteriod.is_medium:
                # Set vectors of the intantiated group 2 asteriods.
                small_asteriod_1.set_vector(asteriod.center.get_x() + 20, asteriod.center.get_y() + 20)
                small_asteriod_2.set_vector(asteriod.center.get_x() - 20, asteriod.center.get_y() - 20)
                
                # Set velocity of the intantiated group 2 asteriods.
                small_asteriod_1.set_velocity(asteriod.velocity.get_dx() + 1.5, asteriod.velocity.get_dy() + 1.5)
                small_asteriod_2.set_velocity((asteriod.velocity.get_dx() + 1.5) * -1, (asteriod.velocity.get_dy() + 1.5) * -1)
                
                # Remove dead medium asteriod from the game.
                self.asteriods.remove(asteriod)
                
                # Put group 2 asteriods in the game.
                self.asteriods.append(small_asteriod_1)
                self.asteriods.append(small_asteriod_2)
                
            # If asteriod is dead and is a small one: 
            elif not asteriod.alive and asteriod.is_small:
                self.asteriods.remove(asteriod)
            
    def check_collisions(self):
        """
        Checks to see if bullets have hit asteriods.
        If true, break asteriod into medium or smaller parts.
        Also check if asteriods have hit the ship. If true break
        asteriod into medium and smaller parts.
        :return:
        """
        for bullet in self.bullets:
            for asteriod in self.asteriods:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and asteriod.alive:
                    too_close = bullet.radius + asteriod.radius

                    if (abs(bullet.center.get_x() - asteriod.center.get_x()) < too_close and
                                abs(bullet.center.get_y() - asteriod.center.get_y()) < too_close):
                        # its a hit!
                        bullet.alive = False
                        asteriod.is_hit = True
                        asteriod.split()

        for asteriod in self.asteriods:
            # Make sure they are both alive before checking for a collision
            if self.ship.alive and asteriod.alive:
                too_close = self.ship.radius + asteriod.radius

                if (abs(self.ship.center.get_x() - asteriod.center.get_x()) < too_close and
                            abs(self.ship.center.get_y() - asteriod.center.get_y()) < too_close):
                    
                    # Ship would destroy if hit by a large asteriod.
                    """
                    if asteriod.is_large:
                        self.ship.alive = False
                    """
                    # its a hit!
                    asteriod.is_hit = True
                    asteriod.split()
                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()
        
# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()