import pygame
import random
import time
import threading
# import RPi.GPIO as GPIO

# this is necessary to start up all the pygame modules:
pygame.init()

# setting up the display window:
global xmax, ymax
xmax = 800
ymax = 600
screen = pygame.display.set_mode((xmax, ymax))
# set_mode() takes a tuple as an argument that tells it the width and height
# of the window (A.K.A. the resolution)

# Sets the title of the window
pygame.display.set_caption('Our Game Title')

# attrubuting icon:
# Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a>
# from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

# icon for game window
icon = pygame.image.load("Images/meteorite.png")
pygame.display.set_icon(icon)

# Player image
player_image = pygame.image.load("Images/astronaut.png")
# Background Image
background = pygame.image.load("Images/galaxy.jpg")
# Asteroid Images
asteroid1 = pygame.image.load("Images/asteroid.png")
asteroid2 = pygame.image.load("Images/asteroid2.png")
asteroid3 = pygame.image.load("Images/asteroid3.png")
asteroids = [asteroid1, asteroid2, asteroid3]

# Coordinates for player image (x, y). Base off screen width and height
global playerX, playerY
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
        print("new asteroid created")
        self.fall_speed = 100
        self.ypos = ymax
        self.xval = random.randint(0, xmax)
        self.yval = ymax
        self.num_asteroid = random.randint(0, 2)
        screen.blit(asteroids[self.num_asteroid], (self.xval, self.yval))

    def start_falling(self):
        global screen
        global asteroids
        print("start_falling begun")
        for i in range(ymax // self.fall_speed):
            print(self.ypos)
            self.ypos = self.ypos - self.fall_speed
            screen.blit(asteroids[self.num_asteroid], (self.xval, self.yval))
            time.sleep(1)

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

    # RGB control for bacground. Takes tuple as argument
    screen.fill((0, 0, 0))
    # Set background image
    screen.blit(background, (0, 0))

    # pygame module helps with "event handling." (AKA clicking, mouse placement, keys pressed)
    for event in pygame.event.get():  # gets list of events
        if event.type == pygame.QUIT:  # Pygame.quit is the same as clicking x on the window
            running = False  # Not the best but works to easily quit loop
        # print(event) # printing events so you can keep track

        # if keystroke is pressed check whether its right or left. Will change later when we get to it. (Find some way of configuring buttons)
        if event.type == pygame.KEYDOWN:  # KEYDOWN detects keystoke event
            if event.key == pygame.K_LEFT and playerX > 50:
                playerX -= 50
            if event.key == pygame.K_RIGHT and playerX < 700:
                playerX += 50
    #     if event.type == pygame.KEYUP:  # Detects when key is released
    #         if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

    #             playerX_change = 0

    # player function must come after the screen fill to avoid covering up image
    player(playerX, playerY)
    pygame.display.update()

    curTime = time.time()
    print(curTime - startTime)
    if not curTime - startTime % 5:
        theAsteroids.append(Asteroid())
        theAsteroids[numAsteroid].fall()
        numAsteroid += 1

    # displaying program is taxing so work on background stuff first

    # Updating the display. You can either use update or use flip method. Update only changes whatever you put in the parameter. If no argument is given update changes everything. pygame flip always changes everything (Not really necessary)
    pygame.display.update()
    count += 1


pygame.quit()
