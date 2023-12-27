import pygame

from playerclass import*
from gameobjectclass import*

pygame.init()
screen = pygame.display.set_mode((900,900))

game_running = True

gameobjects = []

mario = player(speed= 0.008, jump= 0.9)
gameobjects.append(mario)

gameobjects.append(gameobject(pos=[0,500], width=63, height=63, scale=1, image_path="Sprites/HardBlock", static=True, transparent=False))
gameobjects.append(gameobject(pos=[0,500], width=63, height=63, scale=1, image_path="Sprites/HardBlock", static=True, transparent=False))

camera_x = 0
camera_y = 0

camera_x_offset = 400
camera_y_offset = 350

gravity = 0.004

while game_running:

    #Key Inputs
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False

        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()

    mario.is_moving = False

    if keys[pygame.K_d]:
        mario.move(1)

    if keys[pygame.K_a]:
        mario.move(-1)
    
    if keys[pygame.K_SPACE]:
        mario.jump()

    #Set camera
    camera_x = camera_x_offset - mario.position[0]
    camera_y = -camera_y_offset + mario.position[1]

    #Background
    screen.fill((0,138,197))

    for obj in gameobjects:

        obj.get_current_frame()
        obj.update_position(gravity)

        relative_x = obj.position[0]+camera_x
        relative_y = obj.position[1]-camera_y

        screen.blit(obj.rendered_sprite, pygame.Rect(relative_x, relative_y, obj.width, obj.height))

    pygame.display.flip()

pygame.quit()