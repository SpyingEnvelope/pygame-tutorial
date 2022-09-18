import pygame
from sys import exit
import math
from random import randint, choice

# Sprite classes combine rect and surfaces
## Sprite class for player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize the sprite class so we can access it
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        # for animating the player
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()



        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        
        # import sound
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        # change jump volume between 0 and 1
        self.jump_sound.set_volume(0.2)

    # check for player input
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            # play the sound
            self.jump_sound.play()
    
    # apply the gravity
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    # update function
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        # import different surface images based on whether type is fly or not
        self.type = type
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animation_state(self):
        if self.type == 'fly':
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
        else:
            self.animation_index += 0.05
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    # if a sprite x is lower than 100, then delete the sprite
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# function for displaying score
def display_score():
    current_time = math.floor(pygame.time.get_ticks() / 1000 - start_time)
    score_surface = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rect)
    return current_time

# set obstacle movement
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        
        obstacle_list =[obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

# collisions function
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    # detecte collision between sprites with pygame.sprite.spritecollide(sprite, group, boolean). Set boolean to true to delete the one colliding with yours, false not to do that
    # access sprite with .sprite in a single group
    # pygame.sprite.spritecollide(sprite, group, boolean) returns an empty list in cases of no collision and a list if there are collisions
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        #empty the obstacle group in order to restar the game
        obstacle_group.empty()
        return False
    else:
        return True

# Function to animate the player
def player_animation():
    global player_surface, player_index
    # display the jump surface when player is not on floor
    if player_rect.bottom < 300:
        player_surface = player_jump
    # player walking animation if the player is on the floor
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
    


# start with pygame.init(). It starts and adds all the subparts of pygame.
pygame.init()

#display surface. Takes at least one argument with width and height

# screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((800, 400))
# Set name for the game
pygame.display.set_caption('Runner Speech Game')
# clock object helps with time and framerate control
clock = pygame.time.Clock()

# Create an instance of the player class
## We are creating a single group that contains the player sprite
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacles group
obstacle_group = pygame.sprite.Group()

# Import sound
bg_music = pygame.mixer.Sound('audio/music.wav')
# Play the sound and loop it forever. You can add a number for number of loops. -1 means forever
# bg_music.play(loops = -1)
# bg_music.set_volume(0.1)


# Creating a plain surface. Takes a tuple with width and height (width,height)
# test_surface = pygame.Surface((100, 200))
# fill fills the surface with a color. Check documentation for all colors
# test_surface.fill('Red')

## CREATING TEXT
# 1. creat a fone (text size and style)
# 2. write text on a surface
# 3. blit the text onto a surface
# test_font = pygame.font.Font(font type, font size)
test_font = pygame.font.Font('font/PixelType.ttf', 50)

# Check game state
game_active = False

# Timer
start_time = 0

## unlike the other surface that just creates as block. This is how you import an image. Every import is a new surface. Convert converts images to something pygame can work with
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
# Arguments for render(text, anti-aliasing, color)
# score_surface = test_font.render('My game', False, (64,64,64))
# score_rect = score_surface.get_rect(center = (400, 50))

## OBSTACLES

# import snail image. convert_alpha converts alpha (which are white squares). use this to get rid of white squares
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# change snail position
# snail_x_pos = 800
# The proper way to move is with a rect though
# snail_rect = snail_surface.get_rect(midbottom = (800, 300))

# Import the fly image
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Rectangles position things more precisely and are used for collisions. Surface for image and positioning is usually done with rectangle
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
# for animating the player
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
# Create a rect around the surface. Rectangle lets you grab any point and choose where to place it
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300))
# Sprite class combines surface and rect. 

# Create gravity
player_gravity = 0

# Player image for game over/intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
# Scaling the player stand. See documentation for transform
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

# game over/intro text
title_text = test_font.render('Speech Pixel Runner', False, (64,64,64))
title_rect = title_text.get_rect(center = (400,70))
instruction_text = test_font.render('Press Space to Start the Game', False, (64,64,64))
instruction_rect = instruction_text.get_rect(center = (400,330))

# get the score
score = 0

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# use a while True loop to keep the game running forever, so the game stays on
while True:
    # Draw all your elements in here
    # Update everything in the while True loop

    # Check for player input. pygame.event.get() gets all the possible inputs from players
    for event in pygame.event.get():
        # pygame.QUIT is for when the player presses X on the window
        # Check documentation for all event types (they're called event types)
        if event.type == pygame.QUIT:
            # pygame.quit() is the opposite of pygame.init(). Use exit() after pygame.quit()
            pygame.quit()
            exit()
           
        if game_active:    
            # This is how you press keys in the event loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

        # do something if the mouse moves
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print('collision')

            # do something if the mouse clicks the player
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
        
        # If the game has ended
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    bg_music.play(loops = -1)
                    bg_music.set_volume(0.1)
                    # snail_rect.left = 800
                    start_time = math.floor(pygame.time.get_ticks() / 1000)
        
        # event based on interavles
        if game_active:
            # event type for sending in different enemies
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 210)))
            # event.type for animation enemy movements
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
    
    # if game_active is true, the game runs
    if game_active:
        # put the regular surface in the while true loop
        # screen.blit(surface, (position)). Position origin point is the top left. The last object goes on top of the one before it
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # use pygame.draw to draw a rect for the score. See documentation for different shapes you can draw
        # pygame.draw.rect(screen, '#C0E8EC', score_rect)
        # # copy and add width in order to maintain background color
        # pygame.draw.rect(screen, '#C0E8EC', score_rect, 10)

        # ###### FUNCTION FOR DRAWING A FEW SHAPES ######
        # # a command for drawing a line
        # # pygame.draw.line(screen, 'Purple', (0,0), (800, 400),10)
        # # function for drawing an ellipse
        # # pygame.draw.ellipse(screen,'Brown', pygame.Rect(50, 200, 100, 100))
        # ###### FUNCTION FOR DRAWING A FEW SHAPES ######

        # screen.blit(score_surface, score_rect)
        # move snail
        # snail_rect.left -= 5
        # # if snail is out of screen, respawn it on the screen
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)
        # move the player rectangle
        # player_rect.left +=1

        #get a key that was pressed without event loop
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('jump')


        # player_gravity increases with every loop
        # player_gravity += 1

        # # use player rectangle instead for positioning
        # player_rect.y += player_gravity

        # # keep the player on the ground
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300

        # player_animation()
        # screen.blit(player_surface, player_rect)
        # Call the sprite
        player.draw(screen)
        # Update the sprite
        player.update()

        # Draw the obstacle sprite
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        ## Collisions

        game_active = collision_sprite()
        # collision with snail
        # if snail_rect.colliderect(player_rect):
        #     game_active = False

        # detect coliisions between rectangles. returns 0 or 1. collision means 1 and 0 means no collision. py automatically sees 0 as False
        # if player_rect.colliderect(snail_rect):
        #     print('collision')
        
        # use collidepoint to check if one point connects with a rectangle. Good for mouse clicking and is very important. rect1.collidepoint((x,y))
        # get mouse position with either pygame.mouse or event loop. see documentation for all options for pygame.mouse
        # pygame.mouse.get_pressed() returns which mouse button is pressed
        # mouse_pos = pygame.mouse.get_pos()
        # if player_rect.collidepoint((mouse_pos)):
        #     print(pygame.mouse.get_pressed())

        # game_active = collisions(player_rect, obstacle_rect_list)
    
    # This is if the game is not active
    if game_active == False:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        bg_music.stop()

        # add text to game over or intro screen
        if score == 0:
            screen.blit(title_text, title_rect)
        if score > 0:
            score_text = test_font.render(f'Your score: {score}', False, (64,64,64))
            score_rect = score_text.get_rect(center = (400,70))
            screen.blit(score_text, score_rect)

        screen.blit(instruction_text, instruction_rect)
        # clear enemy list
        obstacle_rect_list.clear()


    # Update the display surface. Call it and don't think about it
    pygame.display.update()
    # call clock object. Put an integer. The integer tells pygame that the game should not run faster than 60 fps.
    clock.tick(60)

    ## Display images on a surface.
    # Display surface is the game window.
    # A regular surface is essentially a single image. Has to be connected to the display surface to be visible
