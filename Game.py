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
tailSize = 2 # the size of the tail
spawnFood = False # weather or not there is a food on screen
tailsX = [] # the x pos of the tail pieces
tailsY = [] # the y pos of the tail pieces

# Other Variables
tailNum = int()

# Initalize Pygame
pygame.init()
pygame.font.init()

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Create a screen that is WIDTH wide and HEIGHT tall
pygame.display.set_caption("PySnake") # Name the window 'PySnake'

# Clock Setup For FPS
clock = pygame.time.Clock()

#~~~~~~~~~~ Classes ~~~~~~~~~#
class Head(pygame.sprite.Sprite):
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
        tailPiece = Tail(tailsX[1], tailsY[1]) # create new tail piece
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
        self.rect.centery = y # update the y based off given
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

    def ate(self):
        global spawnFood
        spawnFood = False # There is no longer a food spawned
        self.kill() # Kill the current food

#~~~~~~~ Sprites Init ~~~~~~~#
# Sprite Groups
tailPieces = pygame.sprite.Group()
allSprites = pygame.sprite.Group()

# Sprites
head = Head() # The head of the sanke
allSprites.add(head)

for i in range(tailSize): # Make the tail
    tailsX.append(head.rect.centerx + ((i + 1) * 20))
    tailsY.append(head.rect.centery)
    tailPiece = Tail(tailsX[i], tailsY[i])
    tailPieces.add(tailPiece)

#~~~~~~ Main Game Loop ~~~~~~#
running = True
while (running):
    clock.tick(FPS) # Set the Frames Per Second

    # Check to see if the snake has collided with itself, or the wall
    if (pygame.sprite.spritecollide(head, tailPieces, False) or head.rect.x > WIDTH or head.rect.x < 0 or head.rect.y > HEIGHT or head.rect.y < 0):
        running = False

    # Check events whenever some input is given
    for event in pygame.event.get():
        if (event.type == pygame.QUIT): # If the 'X' in the corner is clicked exit
            running = False
        if (event.type == pygame.KEYDOWN): # If the key is pressed
            key = pygame.key.get_pressed() # Get the key pressed
            if (key[pygame.K_UP]): # If up move up
                head.move("UP")
            if (key[pygame.K_DOWN]): # If down move down
                head.move("DOWN")
            if (key[pygame.K_LEFT]): # If left move left
                head.move("LEFT")
            if (key[pygame.K_RIGHT]): # If right move right
                head.move("RIGHT")

    # Edit Tail Positions
    for i in range(tailSize): # Repeats based off how many tail pieces there are
        if (i < tailSize - 1): # while i is 1 less than the number of tail pieces
            tailsX[(tailSize - 1) - i] = tailsX[(tailSize - 1) - (i + 1)] # Take one elenemt and move it to the right
            tailsY[(tailSize - 1) - i] = tailsY[(tailSize - 1) - (i + 1)] # Take one elenemt and move it to the right
        else:
            tailsX[0] = head.rect.centerx # Set the first element to the new x
            tailsY[0] = head.rect.centery # Set the first element to the new y

    # Update Tail Posiiton
    tailNum = 0 # Set the tail it is updating to 0 (a.k.a 1)
    for i in tailPieces: # for however many tail pieces there are
        i.update(tailsX[tailNum], tailsY[tailNum], tailNum) # Update the Tail
        tailNum += 1 # Go on to the next tail piece

    # Updates the head
    allSprites.update()

    # Spawn Food
    if (not spawnFood): # If there is no food on screen
        # Make a food at a random x and y, that is 1 grid away from the wall, and step 20 so that it is always in line with the snake
        food = Food(random.randrange(20, WIDTH - 20, 20), random.randrange(20, HEIGHT - 20, 20))
        allSprites.add(food)
        spawnFood = True

    # Check for food eaten
    if (pygame.sprite.collide_rect(head, food) == 1): # If the head is colliding with a food
        food.ate() # Get rid of food
        head.eat() # Add 1 to tail

    # Draw Frame
    screen.fill(BLACK) # Gets rid of everything on the screen
    allSprites.draw(screen) # Draws the head
    tailPieces.draw(screen) # Draws the blocks

    # Show Frame
    pygame.display.flip() # Flips the display to show new frame

# Quit out of pygame
pygame.quit()
pygame.font.quit()
