import pygame
from playerclass import*
from gameobjectclass import*

pygame.init()
screen = pygame.display.set_mode((900,900))

camera_x = 0
camera_y = 0

gravity = -9.81
y_max = 370

gameobjects = []

mario = player(1, 25)
gameobjects.append(mario)

game_running = True

while game_running:

    #Key Inputs
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False

        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        mario.position[0] += mario.speed
    if keys[pygame.K_d]:
        mario.position[0] -= mario.speed
    if keys[pygame.K_SPACE]:
        mario.jump()

    #Set camera
    camera_x = mario.position[0]
    camera_y = mario.position[1]

    #Background
    screen.fill((0,138,197))

    for obj in gameobjects:

        if(obj.position[1] < y_max):
            obj.velocity[1] += gravity
        print(obj.velocity)
        obj.get_current_frame()
        obj.update_position(y_max)

        screen.blit(obj.rendered_sprite, pygame.Rect(obj.position[0]+camera_x, obj.position[1]+camera_y, obj.width, obj.height))

    pygame.display.flip()

pygame.quit()