import pygame

from playerclass import*
from gameobjectclass import*
from goomba import*
from time import*

pygame.init()
screen = pygame.display.set_mode((900,900))

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 300)

death_level = 500

def main():

    game_running = True
    game_paused = False

    gameobjects = []

    mario = player(speed= 1.8, accel = 0.02, jump = 4)
    gameobjects.append(mario)

    for i in range(-1,50):
        gameobjects.append(gameobject(pos=[i*63,450], width=63, height=63, scale=1, image_path="Sprites/HardBlock", static=True, transparent=False))

    gameobjects.append(gameobject(pos=[0,450-63], width=63, height=63, scale=1, image_path="Sprites/HardBlock", static=True, transparent=False))
    gameobjects.append(gameobject(pos=[0,450-(2*63)], width=63, height=63, scale=1, image_path="Sprites/HardBlock", static=True, transparent=False))
    gameobjects.append(gameobject(pos=[0,450-(8*63)], width=63, height=63, scale=1, image_path="Sprites/HardBlock", static=True, transparent=False))
    gameobjects.append(gameobject(pos=[63*13,450-63], width=63, height=63, scale=1, image_path="Sprites/HardBlock", static=True, transparent=False))
    
    gameobjects.append(goomba(pos=[200,200]))
    gameobjects.append(goomba(pos=[300,200]))
    gameobjects.append(goomba(pos=[400,200]))

    camera_x = 0
    camera_y = 0

    camera_x_offset = 400
    camera_y_offset = 350

    gravity = 0.024

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

        if keys[pygame.K_r]:
            main()

        if game_paused:
            restart_text = my_font.render('Press r to restart', False, (255, 255, 255))
            screen.blit(restart_text, dest=(500,500))

        #Set camera
        camera_x = camera_x_offset - mario.position[0]
        camera_y = -camera_y_offset + mario.position[1]

        #Background
        screen.fill((0,138,197))

        for obj in gameobjects:

            relative_x = obj.position[0]+camera_x
            relative_y = obj.position[1]-camera_y
            obj.rect = pygame.Rect(relative_x, relative_y, obj.width*obj.scale, obj.height*obj.scale)
            
            # pygame.draw.rect(screen, (255, 0, 0), obj.rect, 5)

            obj.get_current_frame()
            obj.check_collisions(gameobjects) 

            if game_paused == False:
                obj.update_position(gravity)

            screen.blit(obj.rendered_sprite, obj.rect)

            if obj.unqueue_self or (obj != mario and obj.position[1] >= death_level):
                gameobjects.remove(obj)
        
        if mario.alive == False:
            game_paused = True

        pygame.display.flip()

    pygame.quit()

main()