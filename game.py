from ast import walk
import pygame
from pygame.locals import *
from data import world_data

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1200
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mushroomer')

# Define game virables
tile_size = 50

# Load components
background = pygame.image.load('components/world/background.png')
deep_dirt = pygame.image.load('components/world/deepdirt.png')
grass_dirt = pygame.image.load('components/world/grassdirt.png')
grass_dirt_left = pygame.image.load('components/world/grassdirtleft.png')
grass_dirt_right = pygame.image.load('components/world/grassdirtright.png')
grass_dirt_topleft = pygame.image.load('components/world/grassdirttopleft.png')
grass_dirt_topright = pygame.image.load('components/world/grassdirttopright.png')


blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f'components/player/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 40))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5

        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]



        # Handle animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]


        #add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check for collision
        for tile in world.tile_list:
            # Check in X Dir
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0


            # Check n Y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Below the ground
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # Up the ground
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        #draw player onto screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255,10,30), self.rect, 2)



class World():
    def __init__(self, data):
        self.tile_list = []

        def create_component(component_name):
            img = pygame.transform.scale(component_name, (tile_size, tile_size))
            img_rect = img.get_rect()
            img_rect.x = col_count * tile_size
            img_rect.y = row_count * tile_size
            tile = (img, img_rect)
            self.tile_list.append(tile)

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    create_component(deep_dirt)
                if tile == 2:
                    create_component(grass_dirt)
                if tile == 3:
                    create_component(grass_dirt_left)
                if tile == 4:
                    create_component(grass_dirt_right)
                if tile == 5:
                    create_component(grass_dirt_topleft)
                if tile == 6:
                    create_component(grass_dirt_topright)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (0,255,0), tile[1], 1)


world = World(world_data)
player = Player(100, screen_height - 130)

run = True
while run:

    clock.tick(fps)
    screen.blit(background, (0, 0))
    world.draw()
    player.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()