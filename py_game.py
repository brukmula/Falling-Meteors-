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
player_image = pygame.image.load("Images/astronaunt2.png")
# Background Image
background = pygame.image.load("Images/galaxy.jpg")
# Asteroid Images
asteroid1 = pygame.image.load("Images/asteroid4.png")
asteroid2 = pygame.image.load("Images/asteroid5.png")
asteroid3 = pygame.image.load("Images/space-station.png")
asteroid4 = pygame.image.load("Images/asteroid-3.png")

asteroids = [asteroid1, asteroid2, asteroid3, asteroid4]

# Coordinates for player image (x, y). Base off screen width and height

playerX = 370
playerY = 480

playerX_change = 0


# player function that takes x and y coordinates
def player(x, y):
    # blit means "Drawing"
    # blit method takes an image and coordinates as arguments
    screen.blit(player_image, (x, y))


class Asteroid:
    global xmax, ymax
    global screen
    global asteroids

    def __init__(self):
        self.fall_speed = 1
        self.falling = True
        self.ypos = 0
        self.xpos = random.randint(0, xmax)
        self.num_asteroid = random.randint(0, 3)
        screen.blit(asteroids[self.num_asteroid], (self.xpos, self.ypos))

    def start_falling(self):
        global screen
        global ymax
        global asteroids
        self.start = time.time()
        self.count = 1
        while self.falling:
            # increase the number after the modulo operator to decrease fall speed
            if not self.count % 6:
                self.ypos += self.fall_speed
            screen.blit(asteroids[self.num_asteroid], (self.xpos, self.ypos))
            if self.ypos >= ymax:
                self.falling = False
            self.count += 1

    def fall(self):
        self.fall_thread = threading.Thread(target=self.start_falling)
        self.fall_thread.daemon = True
        self.fall_thread.start()


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
#         playerX += 500 """


# GPIO_Handler.GPIO_Setup()

# GPIO.add_event_detect(left_button, GPIO.RISING, callback=GPIO_Handler.left_callback, bouncetime=50)
# GPIO.add_event_detect(right_button, GPIO.RISING, callback=GPIO_Handler.right_callback, bouncetime=50)


# The game loop. Where all the logic of the game is. Start with a 'crashed' boolean that determines when the game loop ends.
running = True
count = 0
numAsteroid = 0
theAsteroids = []

startTime = time.time()
asteroid = Asteroid()
asteroid.fall()

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
            if event.key == pygame.K_LEFT and playerX > left_boundary:
                playerX_change = -50
            if event.key == pygame.K_RIGHT and playerX < right_boundary:
                playerX_change = 50
        # if event.type == pygame.KEYUP:  # Detects when key is released
        #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

        #         playerX_change = 0

    #player function must come after the screen fill to avoid covering up image
    playerX += playerX_change
    player(playerX, playerY)
    playerX_change = 0
    

    #increase the number after the modulo operator to decrease the asteroid spawn speed
    if not count % 5:
        theAsteroids.append(Asteroid())
        theAsteroids[numAsteroid].fall()
        numAsteroid += 1

    if len(theAsteroids) > 15:
        theAsteroids = []
        numAsteroid = 0

    if count > 1000:
        count = 0

    # displaying program is taxing so work on background stuff first

    # Updating the display. You can either use update or use flip method. Update only changes whatever you put in the parameter. If no argument is given update changes everything. pygame flip always changes everything (Not really necessary)
    pygame.display.update()
    count += 1
    time.sleep(0.1)


pygame.quit()


##Notes
#Asteroids need to stay within Borders and speed adjustment
#Should we make the movement of the Astro smoother or...
