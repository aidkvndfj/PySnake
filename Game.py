##############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~Created By: Eric~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
##############################

#~~~~~~~~~~~ Setup ~~~~~~~~~~#
# Needed Imports
import pygame
import random

# Constants
WIDTH = 600 # Width of screen
HEIGHT = 400 # Height of screen
FPS = 7 # frames per second

# Define The Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Global Variables
global tailSize, spawnFood, tailsX, tailsY
tailSize = int(3) # the size of the tail
spawnFood = bool(False) # weather or not there is a food on screen
tailsX = [] # the x pos of the tail pieces
tailsY = [] # the y pos of the tail pieces

# Initalize Pygame
pygame.init()
pygame.font.init()

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Create a screen that is WIDTH wide and HEIGHT tall
pygame.display.set_caption("PySnake") # Name the window 'PySnake'

# Clock Setup For FPS
clock = pygame.time.Clock()

#~~~~~~~~~~ Classes ~~~~~~~~~#
class Head(pygame.sprtie.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Head Setup
        self.image = pygame.Surface((15, 15)) # Create head with 15 width and height
        self.image.fill(BLUE) # Make it blue
        self.rect = self.image.get_rect() # Set the rect to the image rect
        self.rect.center = ((WIDTH / 2, HEIGHT / 2)) #set starting location to middle of the screen
        # Self Variable Setup
        self.vel = 20 # Set the velocity to 20
        self.speedx = -self.vel # Have the head start moving left
        self.speedy = 0 # Have the ehad start without moving up or down
        self.previousDir = None #create previous direction

    def update(self):
        # Moves x and y based off speedx and speedy
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

    def move(self, dir):
        # change the speeds based off what key was pressed, can't turn 180
        if (dir == "UP" and self.previousDir != "DOWN"):
            self.speedx = 0
            self.speedy = -self.vel
            self.previousDir = "UP"
        if (dir == "DOWN" and self.previousDir != "UP"):
            self.speedx = 0
            self.speedy = self.vel
            self.previousDir = "DOWN"
        if (dir == "LEFT" and self.previousDir != "RIGHT"):
            self.speedx = -self.vel
            self.speedy = 0
            self.previousDir = "LEFT"
        if (dir == "RIGHT" and self.previousDir != "LEFT"):
            self.speedx = self.vel
            self.speedy = 0
            self.previousDir = "RIGHT"

        def eat(self):
            global tailSize, tailsX, tailsY
            tailSize += 1 # Add one to tail size
            tailsX.append(self.rect.centerx) # Add a element to tails X
            tailsY.append(self.rect.centery) # Add a element to tails Y
            tailPiece = Tail(blocksX[1], blocksY[1]) # create new tail piece
            tailPieces.add(tailPiece) # Add tail piece to the tail group

class Tail(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Tail piece setup
        self.image = pygame.Surface((15, 15)) # Make it the same size as the head
        self.image.fill(BLUE) # Make it blue
        self.rect = self.image.get_rect() # Set the rect to be the same as the image
        self.rect.centerx = x # Starting x position at given
        self.rect.centery = y # Starting y position at given

    def update(self, x, y, colorScale):
        self.rect.centerx = x # update the x based off given
        self.rect.cetnery = y # update the y based off given
        # Scale the color based on where in tail piece is
        self.image.fill((255.0 / ((colorScale + 2) / 1), 255.0 / ((colorScale + 2) / 1.2), 255.0 / ((colorScale + 2) / 2)))

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Food image Setup
        self.image = pygame.Surface((12, 12)) # Make the food slightly smaller than the head/tail
        self.image.fill(WHITE) # Make the food white
        self.rect = self.image.get_rect() #set the rect to the image rect
        self.rect.centerx = x # Set the x to given x
        self.rect.centery = y # Set the y to given y

#~~~~~~~ Sprites Init ~~~~~~~#
# Sprite Groups
tailPieces = pygame.sprite.Group()

# Sprites
head = Head() # The head of the sanke
for i in range(tailSize): # Make the tail
    tailsX.append(head.rect.centerx + ((i + 1) * 20))
    tailsY.append(head.rect.centerx + ((i + 1) * 20))
    tailPiece = Tail(tailsX[i], tailsY[i])
    tailPieces.add(tailPiece)

#~~~~~~ Main Game Loop ~~~~~~#
running = True
while (running):
    clock.time(FPS) # Set the Frames Per Second

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
