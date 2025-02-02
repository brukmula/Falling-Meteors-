import pygame
import random
import time
import threading
import RPi.GPIO as GPIO
# this is necessary to start up all the pygame modules:
pygame.init()
pygame.font.init()

# setting up the display window:
global xmax, ymax
global screen
xmax = 900
ymax = 600
left_boundary = 50
right_boundary = xmax - 100
screen = pygame.display.set_mode((xmax, ymax))
# set_mode() takes a tuple as an argument that tells it the width and height
# of the window (A.K.A. the resolution)
# myfont = pygame.font.SysFont('Comic Sans MS', 30)

# textsurface = myfont.render('{}'.format(time), False, (0, 0, 0))


# Sets the title of the window
pygame.display.set_caption('Falling Meteors')

# attrubuting icon:
# Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a>
# from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

# icon for game window
icon = pygame.image.load("Images/meteorite.png").convert_alpha()
pygame.display.set_icon(icon)

# Player image
player_image = pygame.image.load("Images/astronaut.png").convert_alpha()
# Background Image
background = pygame.image.load("Images/galaxy.jpg").convert_alpha()
# Asteroid Images
asteroid1_image = pygame.image.load("Images/asteroid4.png").convert_alpha()
asteroid2_image = pygame.image.load("Images/asteroid5.png").convert_alpha()
asteroid3_image = pygame.image.load("Images/space-station.png").convert_alpha()
asteroid4_image = pygame.image.load("Images/asteroid-3.png").convert_alpha()

asteroids = [asteroid1_image, asteroid2_image, asteroid3_image, asteroid4_image]



# Coordinates for player image (x, y). Base off screen width and height

playerX = 450
playerY = 550


class Player:

    def __init__(self, image, x, y):
        self.xpos = x
        self.ypos = y
        self.image = image
        self.rect = self.image.get_rect(center = (self.xpos, self.ypos))
        self.rect.height -= 10
        self.rect.width -= 10
        
        

    # player function that takes x and y coordinates

    def set_pos(self):
        # blit means "Drawing"
        # blit method takes an image and coordinates as arguments
        screen.blit(self.image, self.rect)

    def change_xpos(self, x_change):
        self.xpos += x_change
        self.rect.x = self.xpos 

    def isCollided(self, obj):
        return self.rect.colliderect(obj.rect)





class Asteroid:
    global xmax, ymax
    global screen
    global asteroids
    global clock
    global random_integers 

    def __init__(self, image):
        
        self.image = image
        self.ypos = random.randint(-1000, -100)
        self.xpos = random.randint(*(((200 * i) + 50), ((200 * (i + 1)))))
        self.fall_speed = 6.0
        self.rect = self.image.get_rect(center = (self.xpos, self.ypos))
        self.rect.height -= 10
        self.rect.width -= 10
        
        
        
        

    def fall(self):
        self.ypos += self.fall_speed 
        self.rect.y = self.ypos

    def set_pos(self):
        screen.blit(self.image, self.rect)

    def reset(self, y_start = -100):
        self.ypos = y_start
        self.rect.y = self.ypos
    
    def randomize_xpos(self, increment):
        self.xpos = random.randint(*(((200 * increment) + 50), ((200 * (increment + 1)))))
        self.rect.x = self.xpos
        return self.xpos




# pins
left_button = 13
right_button = 15


class GPIO_Handler:
    def GPIO_Setup():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def left_callback(channel):
        global player
        player.change_xpos(-50)

    def right_callback(channel):
        global player
        player.change_xpos(50) 


GPIO_Handler.GPIO_Setup()

GPIO.add_event_detect(left_button, GPIO.RISING, callback=GPIO_Handler.left_callback, bouncetime=50)
GPIO.add_event_detect(right_button, GPIO.RISING, callback=GPIO_Handler.right_callback, bouncetime=50)


# The game loop. Where all the logic of the game is. Start with a 'crashed' boolean that determines when the game loop ends.








theAsteroids = []
for i in range(len(asteroids)):
    theAsteroids.append(Asteroid(asteroids[i]))

player = Player(player_image, playerX, playerY)

level_speed_increment = 1.0


def game_loop():
    level_1 = False
    level_2= False
    level_3 = False
    level_4 = False
    level_5 = False
    level_6 = False
    level_7 = False
    level_8 = False
    level_9 = False
    level_10 = False
    
        
    level_count = 0
    
    clock = pygame.time.Clock()

    running = True
    startTime = pygame.time.get_ticks()
    while running:
        
        

        # # RGB control for bacground. Takes tuple as argument
        
        # Set background image
    
        # pygame module helps with "event handling." (AKA clicking, mouse placement, keys pressed)
        for event in pygame.event.get():  # gets list of events
            if event.type == pygame.QUIT:  # Pygame.quit is the same as clicking x on the window
                running = False  # Not the best but works to easily quit loop
            # print(event) # printing events so you can keep track

            # if keystroke is pressed check whether its right or left. Will change later when we get to it. (Find some way of configuring buttons)
            if event.type == pygame.KEYDOWN:  # KEYDOWN detects keystoke event
                if event.key == pygame.K_LEFT and player.xpos > left_boundary:
                    player.change_xpos(-50)
                if event.key == pygame.K_RIGHT and player.xpos < right_boundary:
                    player.change_xpos(50)
            # if event.type == pygame.KEYUP:  # Detects when key is released
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #         player.change_xpos(0)
                    
        # player function must come after the screen fill to avoid covering up image

        
        
        
        
        for i in range(len(theAsteroids)):
            theAsteroids[i].fall()
            if theAsteroids[i].ypos > ymax + 100:
                theAsteroids[i].reset(random.randint(-1000, -100))
                theAsteroids[i].image = random.choice(asteroids)
                theAsteroids[i].randomize_xpos(i)
                
                        
                
        

        # if theAsteroids[0].ypos > ymax + 100:
        #     theAsteroids[0].reset(-100)
        #     theAsteroids[0].randomize_xpos()

        # if theAsteroids[1].ypos > ymax + 100:
        #     theAsteroids[1].reset(-200)
        #     theAsteroids[1].randomize_xpos()

        # if theAsteroids[2].ypos > ymax + 100:
        #     theAsteroids[2].reset(-50)
        #     theAsteroids[2].randomize_xpos()

        # if theAsteroids[3].ypos > ymax + 100:
        #     theAsteroids[3].reset(-40)
        #     theAsteroids[3].randomize_xpos()

        # check for collision
        for i in range(len(theAsteroids)):
            if player.isCollided(theAsteroids[i]):
                running = False
        
        # increase the number after the modulo operator to decrease the asteroid spawn speed

        # displaying program is taxing so work on background stuff firs
        # Updating the display. You can either use update or use flip method. Update only changes whatever you put in the parameter. If no argument is given update changes everything. pygame flip always changes everything (Not really necessary)
        screen.blit(background, (0, 0))
        for asteroid in theAsteroids:
            asteroid.set_pos()
        player.set_pos()

        font = pygame.font.SysFont('Consolas', 30)
        time_since_start = pygame.time.get_ticks() - startTime
        screen.blit(font.render("Time: {:.1f}".format(time_since_start / 1000), True, (0, 0, 0)), (32, 48))
        screen.blit(font.render("Level: {}".format(int(level_count)), True, (0, 0, 0)), (32, 70))


        if not level_1:
            if int(time_since_start / 100) == 100:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_1= True
                    level_count += 0.25

        if not level_2:
            if int(time_since_start / 100) == 200:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_2= True
                    level_count += 0.25

        if not level_3:
            if int(time_since_start / 100) == 300:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_3 = True
                    level_count += 0.25

        if not level_4:
            if int(time_since_start / 100) == 400:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_4 = True
                    level_count += 0.25

        if not level_5:
            if int(time_since_start / 100) == 500:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_5 = True
                    level_count += 0.25

        if not level_6:
            if int(time_since_start / 100) == 600:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_6 = True
                    level_count += 0.25

        if not level_7:
            if int(time_since_start / 100) == 700:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_7 = True
                    level_count += 0.25

        if not level_8:
            if int(time_since_start / 100) == 800:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_8 = True
                    level_count += 0.25

        if not level_9:
            if int(time_since_start / 100) == 900:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_9 = True
                    level_count += 0.25

        if not level_10:
            if int(time_since_start / 100) == 1000:
                for asteroid in theAsteroids:
                    asteroid.fall_speed += level_speed_increment
                    level_10 = True
                    level_count += 0.25

        


        #print(int(time_since_start / 100))
        clock.tick_busy_loop(360)
        pygame.display.update()
        

game_loop()

pygame.quit()


# Notes
# Asteroids need to stay within Borders and speed adjustment
# Should we make the movement of the Astro smoother or...
