import pygame
import random
import time
import threading
# import RPi.GPIO as GPIO
# this is necessary to start up all the pygame modules:
pygame.init()

# setting up the display window:
global xmax, ymax
global screen
xmax = 800
ymax = 600
left_boundary = 50
right_boundary = 700
screen = pygame.display.set_mode((xmax, ymax))
# set_mode() takes a tuple as an argument that tells it the width and height
# of the window (A.K.A. the resolution)

# Sets the title of the window
pygame.display.set_caption('Falling Meteors')

# attrubuting icon:
# Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a>
# from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

# icon for game window
icon = pygame.image.load("Images/meteorite.png")
pygame.display.set_icon(icon)

# Player image
player_image = pygame.image.load("Images/astronaut.png").convert_alpha()
# Background Image
background = pygame.image.load("Images/galaxy.jpg")
# Asteroid Images
asteroid1_image = pygame.image.load("Images/asteroid4.png").convert_alpha()
asteroid2_image = pygame.image.load("Images/asteroid5.png").convert_alpha()
asteroid3_image = pygame.image.load("Images/space-station.png")
asteroid4_image = pygame.image.load("Images/asteroid-3.png").convert_alpha()

asteroids = [asteroid1_image, asteroid2_image, asteroid3_image, asteroid4_image]

# Coordinates for player image (x, y). Base off screen width and height

playerX = 370
playerY = 480


class Player:
    global player_image, playerX, playerY

    def __init__(self):
        self.xpos = playerX
        self.ypos = playerY
        self.set_pos()

    # player function that takes x and y coordinates

    def set_pos(self):
        # blit means "Drawing"
        # blit method takes an image and coordinates as arguments
        screen.blit(player_image, (self.xpos, self.ypos))

    def change_xpos(self, x_change):
        self.xpos += x_change


class Asteroid:
    global xmax, ymax
    global screen
    global asteroids

    def __init__(self, image):
        self.image = image
        self.ypos = random.randint(-100, -10)
        self.xpos = random.randint(left_boundary, right_boundary)
        self.set_pos()
        self.fall_speed = 50

    def fall(self, y_change):
        self.ypos += y_change

    def set_pos(self):
        screen.blit(self.image, (self.xpos, self.ypos))

    def reset(self, y_start):
        self.ypos = y_start


# pins
left_button = 13
right_button = 15


# """ class GPIO_Handler:
#     def GPIO_Setup(self):
#         GPIO.setwarnings(False)
#         GPIO.setmode(GPIO.BOARD)
#         GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#         GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#     def left_callback(channel):
#         global playerX
#         print("Left button pressed")
#         playerX -= 50

#     def right_callback(channel):
#         global playerX
#         print("Right button pressed")
#         playerX += 50 """


# GPIO_Handler.GPIO_Setup()

# GPIO.add_event_detect(left_button, GPIO.RISING, callback=GPIO_Handler.left_callback, bouncetime=50)
# GPIO.add_event_detect(right_button, GPIO.RISING, callback=GPIO_Handler.right_callback, bouncetime=50)


# The game loop. Where all the logic of the game is. Start with a 'crashed' boolean that determines when the game loop ends.
running = True

startTime = time.time()

theAsteroids = []
for i in range(len(asteroids)):
    theAsteroids.append(Asteroid(asteroids[i]))
# asteroid1 = Asteroid(asteroid1_image)
# asteroid2 = Asteroid(asteroid2_image)
# asteroid3 = Asteroid(asteroid3_image)
# asteroid4 = Asteroid(asteroid4_image)

asteroid_fall_speed = 1.5
player = Player()


def game_loop():
    global running
    while running:

        # # RGB control for bacground. Takes tuple as argument
        # screen.fill((0, 0, 0))
        # Set background image
        screen.blit(background, (0, 0))

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

            #         playerX_change = 0

        # player function must come after the screen fill to avoid covering up image

        player.set_pos()

        # asteroid1.fall(asteroid_fall_speed)
        # asteroid2.fall(asteroid_fall_speed)
        # asteroid3.fall(asteroid_fall_speed)
        # asteroid4.fall(asteroid_fall_speed)
        for asteroid in theAsteroids:
            asteroid.fall(asteroid_fall_speed)

        if theAsteroids[0].ypos > ymax + 100:
            theAsteroids[0].reset(-100)
            theAsteroids[0].xpos = random.randint(left_boundary, right_boundary)

        if theAsteroids[1].ypos > ymax + 100:
            theAsteroids[1].reset(-1000)
            theAsteroids[1].xpos = random.randint(left_boundary, right_boundary)

        if theAsteroids[2].ypos > ymax + 100:
            theAsteroids[2].reset(-50)
            theAsteroids[2].xpos = random.randint(left_boundary, right_boundary)

        if theAsteroids[3].ypos > ymax + 100:
            theAsteroids[3].reset(-40)
            theAsteroids[3].xpos = random.randint(left_boundary, right_boundary)

        for asteroid in theAsteroids:
            asteroid.set_pos()

        player_rect = player_image.get_rect(topleft=(playerX, playerY))
        for i in range(len(asteroids)):
            asteroidRect = asteroids[i].get_rect(
                topleft=(theAsteroids[i].xpos, theAsteroids[i].ypos))
            if player_rect.colliderect(asteroidRect):
                print("collision detected")

        # increase the number after the modulo operator to decrease the asteroid spawn speed

        # displaying program is taxing so work on background stuff firs
        # Updating the display. You can either use update or use flip method. Update only changes whatever you put in the parameter. If no argument is given update changes everything. pygame flip always changes everything (Not really necessary)
        pygame.display.update()


game_loop()

pygame.quit()


# Notes
# Asteroids need to stay within Borders and speed adjustment
# Should we make the movement of the Astro smoother or...
