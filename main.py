# main.py

# load PyGame

# import pygame # Loads all the pygame module in memory
import pygame
import Level as Lvl

#intialize mixer module
#pygame.mixer.pre_init(44100, -16, 2, 512)
#pygame.mixer.init()

pygame.init()

"""
Setup
-where we'll include game settings
"""
worldx = 544  # width
worldy = 544  # height
fps = 20  # frame rate
ani = 4  # animation cycles
clock = pygame.time.Clock()
steps = 15
tile_size = 32
level_map = [Lvl.tile_map_1, Lvl.tile_map_2, Lvl.tile_map_3]
main_menu = True
gameover_screen = False

# imaginary scroll boundary wall
backwardx_wall = 50
forwardx_wall = worldx - 100

#Load sound files
jump_fx = pygame.mixer.Sound("Assets/jump.mp3")
jump_fx.set_volume(0.5)

injury_fx = pygame.mixer.Sound("Assets/injury.mp3")
injury_fx.set_volume(0.7)

treasure_fx = pygame.mixer.Sound("Assets/treasure.mp3")
treasure_fx.set_volume(0.9)

# RGB values 0 - 254
BLUE = (86, 171, 255)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
GREEN = (10, 200, 10)
RED = (250, 0, 0)

# # load image
sky_image = pygame.image.load("Assets/sky.png")

# # Scale the image to your needed size
background = pygame.transform.scale(sky_image, (worldx, worldy))

restart = pygame.image.load("Assets/restart.png")
restart_img = pygame.transform.scale(restart, (125, 50))

start = pygame.image.load("Assets/start.png")
start_img = pygame.transform.scale(start, (175, 75))

exit = pygame.image.load("Assets/exit.png")
exit_img = pygame.transform.scale(exit, (175, 75))

# to take up the whole screen, use worldx and worldy for width and height tuple.

world = pygame.display.set_mode((worldx, worldy))
pygame.display.set_caption("My First Game using PyGame")

player_list = pygame.sprite.Group()
main_group = pygame.sprite.Group()  # all tiles
plat_list = pygame.sprite.Group()  # Good for player to stand
danger_tile_list = pygame.sprite.Group()  # Dangerous tiles for player to go
enemy_list = pygame.sprite.Group()
portal_list = pygame.sprite.Group()
ruby_list = pygame.sprite.Group()


# put run-once code here

"""
Objects
-the code to make characters in our game
"""
# dunder


# class Factory:  # parent class
#     def __init__(self, name, color, material):
#         self.name = name  # attributes -details about things made at factory
#         self.color = color
#         self.material = material


# class Shoes(Factory):  # blueprint for making shoes
#     def __init__(self, name, color, material, size, price):  # constructor
#         super().__init__(name, color, material)  # instantiate parent class
#         # self.name = name      #attributes -details about shoes
#         # self.color = color
#         # self.material = material
#         self.size = size
#         self.price = price


# shoe = Shoes("Crocs", "Blue", "Croslite", 9, 14.99)

# print("**************")
# print(f"{shoe.name} are on sale for {shoe.price} in size {shoe.size}!")
# print("**************")


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def create(self):
        # draw the button
        action = False
        
        # get mouse position
        position = pygame.mouse.get_pos()
        
        # check mouse click collides with button
        if self.rect.collidepoint(position):
            # left mouse click
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print("Left mouse clicked")
                action = True
                self.clicked = True
            # left mouse released
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        world.blit(self.image, self.rect)
        return action

class Game():
    def __init__(self):
        # self.player = player
        # self.enemy_list = enemy_list
        # self.danger_tile_list = danger_tile_list
        # self.portal_list = portal_list
        self.lives = 3
        self.lvl_counter = 0
        self.score = 0
        self.HUD_font = pygame.font.Font(None, 24)
        self.gameover = False
        #create_world(level_map[0])
        self.travel_x = 0
        
    def draw(self):
        lives_text = self.HUD_font.render(f'Lives: {self.lives}', True, WHITE) 
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (10, 10)
        world.blit(lives_text, lives_rect)
        
        score_text = self.HUD_font.render(f'Score: {self.score}/5', True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (worldx - 100,10)
        world.blit(score_text, score_rect)

        
        if self.gameover:
            player.image = player.hurt_image
            player.rect.x = worldx / 2
            player.rect.y = 150
            player.travel_y = 0
            print('Game Over')
            
            gameover_screen = True
            
            if restart_button.create():
                player.kill()
                for enemy in enemy_list:
                    enemy.kill()
                for tile in main_group:
                    tile.kill()
                self.lives = 3
                self.score = 0
                self.gameover = False
                create_world(level_map[0])

    #level advancement
    def level_finish(self):
        portal_collision = pygame.sprite.spritecollide(player, portal_list, False)
        for portal in portal_collision:
            if self.score == 5:
                self.level_progress()

    def level_progress(self):
        player.kill()
        for enemy in enemy_list:
            enemy.kill()
        for tile in main_group:
            tile.kill()
        self.lvl_counter += 1
        print(self.lvl_counter)
        if self.lvl_counter == len(level_map):
            self.lvl_counter = 0
        create_world(level_map[self.lvl_counter])
        player.move(steps,0)
        self.score = 0
            
        
    def check_lives(self):
        enemy_collide = pygame.sprite.spritecollide(player, enemy_list, False)
        for enemy in enemy_collide:
            if player.travel_y <= 0:
                player.is_colliding = False
                self.lives -= 1
            player.rect.bottom = enemy.rect.top - 1
            #player.travel_y = 0
            player.travel_y -= 15
        
        danger_collide = pygame.sprite.spritecollide(player, danger_tile_list, False)
        for danger in danger_collide:
            if player.travel_y <= 0:
                player.is_colliding = False
                self.lives -= 1
                injury_fx.play()
            player.rect.bottom = danger.rect.top - 1
            #player.travel_y = 0
            player.travel_y -= 15
            
    def check_gameover(self):
        if self.lives <= 0:
            self.gameover = True
            self.lives = 0

    #check_ruby_collisions
    def check_collisions(self):
        ruby_collision = pygame.sprite.spritecollide(player, ruby_list, True)
        for ruby in ruby_collision:
            self.score += 1
            treasure_fx.play()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.width = 50
        #self.height = 50
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill(BLUE)
        player_pic = pygame.image.load("Assets/player.png")
        self.image = pygame.transform.scale(player_pic, (tile_size, tile_size))
        hurt_pic = pygame.image.load("Assets/player_hurt.png")
        self.hurt_image = pygame.transform.scale(hurt_pic, (tile_size, tile_size))
        end_pic = pygame.image.load("Assets/player_end.png")
        self.end_image = pygame.transform.scale(end_pic, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x  # go to x
        self.rect.y = y  # go to y
        self.travel_x = 0  # travels along the X axis
        self.travel_y = 0  # travels along the Y axis
        self.is_colliding = False

    def move(self, x, y):
        # self.travel_x = self.travel_x + x
        if self.travel_x == 15 and x == 15:
            pass
        else:
            self.travel_x += x
        # self.travel_y = self.travel_y + y
        self.travel_y += y

    def update(self):
        self.rect.x += self.travel_x
        self.rect.y += self.travel_y
        
        plat_collide = pygame.sprite.spritecollide(self, plat_list, False)
        # Vertical collision
        for plat in plat_collide:
            if self.travel_y > 0:
                self.travel_y = 0
                self.rect.bottom = plat.rect.top
            elif self.travel_y < 0:
                self.travel_y = 0
                self.rect.top = plat.rect.bottom
            self.is_colliding = True
        
        #Detect Horizontal collision
        for plat in plat_list:
            if plat.rect.colliderect(self.rect.x - steps, self.rect.y, 
            self.rect.width, self.rect.height):
                if self.travel_x < 0:
                    self.rect.left = plat.rect.right + steps
            elif plat.rect.colliderect(self.rect.x + steps, self.rect.y, 
            self.rect.width, self.rect.height):
                if self.travel_x > 0:
                    self.rect.right = plat.rect.left - steps
        
        
    def gravity(self):
        if self.rect.y >= worldy: # - tile_size:
            self.travel_y = 0
            self.rect.y = worldy - tile_size
        else:
            self.travel_y += 1
            
    def jump(self):
        if self.is_colliding:
            jump_fx.play()
            self.travel_y -= 15
            self.is_colliding = False
    

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.width = 50
        #self.height = 50
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill(BLUE)
        enemy_pic = pygame.image.load("Assets/monster.png")
        self.image = pygame.transform.scale(enemy_pic, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x  # go to x
        self.rect.y = y  # go to y
        self.travel_x = 0  # travels along the X axis
        self.travel_y = 0  # travels along the Y axis
        self.is_colliding = False
        self.enemySteps = 0
        enemy_list.add(self)
        
        
    def update(self):
        self.rect.x += self.travel_x
        distance = 125
        speed = 4
        if 0 <= self.enemySteps <= distance / 2:
            self.travel_x = speed
        elif distance / 2 <= self.enemySteps < distance:
            self.travel_x = -speed
        else:
            self.enemySteps = 0
        self.enemySteps += 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, main_group, sub_group, image_int):
        super().__init__()

        # load images
        if image_int == 1:
            grass_pic = pygame.image.load("Assets/grass.png")
            self.image = pygame.transform.scale(grass_pic, (tile_size, tile_size))
        elif image_int == 2:
            water_pic = pygame.image.load("Assets/water.png")
            self.image = pygame.transform.scale(water_pic, (tile_size, tile_size))
        elif image_int == 3:
            box_pic = pygame.image.load("Assets/box_coin.png")
            self.image = pygame.transform.scale(box_pic, (tile_size, tile_size))
        # portal
        elif image_int == 6:
            portal_pic = pygame.image.load("Assets/portal.png")
            self.image = pygame.transform.scale(portal_pic, (2*tile_size, 4*tile_size))
        # ruby
        elif image_int == 7:
            ruby_pic = pygame.image.load("Assets/ruby.png")
            self.image = pygame.transform.scale(ruby_pic, (tile_size, tile_size))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        main_group.add(self)
        sub_group.add(self)

 

def create_world(level_map):
    for row in range(len(level_map)):
        for col in range(len(level_map[row])):
            if level_map[row][col] == 1:  # grass
                Platform(col * tile_size, row * tile_size, main_group, plat_list, 1)
            elif level_map[row][col] == 2:  # water
                Platform(
                    col * tile_size, row * tile_size, main_group, danger_tile_list, 2
                )
            elif level_map[row][col] == 3:  # box
                Platform(col * tile_size, row * tile_size, main_group, plat_list, 3)
            elif level_map[row][col] == 6: #portal
                Platform(col*tile_size,row*tile_size,main_group, portal_list, 6)
            elif level_map[row][col] == 7: #ruby
                Platform(col*tile_size,row*tile_size,main_group, ruby_list, 7)
            
            elif level_map[row][col] == 4:
                print(f"Adding player {col*tile_size}, {row*tile_size}")
                global player
                player = Player(col * tile_size, row * tile_size)
                player_list.add(player)
            elif level_map[row][col] == 5:  #enemy
                Enemy(col * tile_size, row * tile_size)
                
    
create_world(level_map[0])
my_game = Game()

restart_button = Button(worldx/2, worldy/2, restart_img)
start_button = Button(worldx/2 - 225, worldy/2, start_img)
exit_button = Button(worldx/2 + 50, worldy/2, exit_img)

# def draw_grid():
#     for line in range(0, 10):
#         pygame.draw.line(
#             world, (WHITE), (0, line * tile_size), (worldx, line * tile_size)
#         )
#         pygame.draw.line(
#             world, (WHITE), (line * tile_size, 0), (line * tile_size, worldy)
#         )


# put Python classes and functions here


"""
Main Loop
-keeps the game running
-updates changes to state of the game, 
-displays those changes on the game screen
"""
play_game = True
while play_game:
    world.fill(BLACK)
    main_group.draw(world)
    
    if main_menu:
        if start_button.create():
            main_menu = False
        if exit_button.create():
            play_game = False
    elif gameover_screen:
        world.fill(RED)
    else:
        # Draw the game
        my_game.check_gameover()
        my_game.check_lives()
        my_game.draw()
        my_game.level_finish()
        my_game.check_collisions()
        
        
        if player.rect.x >= forwardx_wall:
            # scroll all objects to the left
            scroll = player.rect.x - forwardx_wall
            player.rect.x = forwardx_wall
            for sprite in main_group:
                sprite.rect.x -= scroll
            for sprite in enemy_list:
                sprite.rect.x -= scroll
            
        if player.rect.x <= backwardx_wall:
            # scroll all object to the right
            scroll = backwardx_wall - player.rect.x
            player.rect.x = backwardx_wall
            for sprite in main_group:
                sprite.rect.x += scroll
            for sprite in enemy_list:
                sprite.rect.x += scroll
        
        player.gravity()
        player.update()
        player_list.draw(world)
        for enemy in enemy_list:
            enemy.update()
        enemy_list.draw(world)
    # draw_grid()
    pygame.display.flip()
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            play_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == ord("q"):  # ord('a') = 65 ord('A') = 97
                pygame.quit()
                play_game = False
            if event.key == ord("a") or event.key == pygame.K_LEFT:
                print("Left")
                player.move(-steps, 0)
                print(player.travel_x)
            if event.key == ord("d") or event.key == pygame.K_RIGHT:
                print("Right")
                player.move(steps, 0)
                print(player.travel_x)
            if event.key == ord("w") or event.key == pygame.K_UP:
                print("Jump")
                player.jump()
                #print(player.travel_y)
        if event.type == pygame.KEYUP:
            if event.key == ord("q"):  # ord('a') = 65 ord('A') = 97
                pygame.quit()
                play_game = False
            if event.key == ord("a") or event.key == pygame.K_LEFT:
                print("Left Stop")
                player.move(steps, 0)
            if event.key == ord("d") or event.key == pygame.K_RIGHT:
                print("Right Stop")
                player.move(-steps, 0)
            # if event.key == ord('w') or event.key == pygame.K_UP:
            #     print('Jump Stop')
print("Game ends here...")
# time.sleep(2)