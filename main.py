import pygame
from time import*

from gameobjectclass import*
from playerclass import*
from enemyclass import*
from propclass import*

pygame.init()
screen = pygame.display.set_mode((900,900))

pygame.font.init()
game_font = pygame.font.SysFont(None, 55)

death_level = 900
gravity = 0.009

def main():

    game_running = True
    game_paused = False

    gameobjects = []

    mario = player(speed= 0.6, accel = 0.02, jump = 2)
    gameobjects.append(mario)

    for i in range(-1,50):
        gameobjects.append(hard_block(pos=[i*63, 450]))

    gameobjects.append(hard_block(pos=[0,450-63]))
    gameobjects.append(hard_block(pos=[0,450-(2*63)]))
    gameobjects.append(hard_block(pos=[0,450-(8*63)]))
    gameobjects.append(hard_block(pos=[63*13,450-63]))

    gameobjects.append(question_block(pos=[340,130], object_inside="Mushroom"))

    gameobjects.append(prop(pos=[1200,-200], type="Castle", scale=1))

    gameobjects.append(koopa(pos=[500,100]))

    gameobjects.append(coin(pos=[200,310]))

    camera_x = 0
    camera_y = 0

    camera_x_offset = 400
    camera_y_offset = 350

    last_time = 0

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

        #Set camera
        camera_x = camera_x_offset - mario.position[0]
        camera_y = -camera_y_offset + mario.position[1]

        #Background
        screen.fill((0,138,197))

        sorted_objects = sorted(gameobjects, key=lambda order: order.draw_order)

        curr_time = pygame.time.get_ticks()
        delta = curr_time-last_time
        last_time = curr_time

        for obj in sorted_objects:

            relative_x = obj.position[0]+camera_x
            relative_y = obj.position[1]-camera_y

            if relative_x < screen.get_width()+100 and relative_x > -100:
     
                obj.rect = pygame.Rect(relative_x, relative_y, obj.width*obj.scale, obj.height*obj.scale)
                
                obj.get_current_frame()

                if obj.collidable:
                    obj.check_collisions(gameobjects) 

                if game_paused == False:
                    obj.update_position(gravity, delta)

                screen.blit(obj.rendered_sprite, obj.rect)

                if obj.collidable == True:
                    obj.rect = pygame.Rect(relative_x-obj.collision_offset[0], relative_y-obj.collision_offset[1], obj.width*obj.scale*obj.collision_size[0], obj.height*obj.scale*obj.collision_size[1])
                
                pygame.draw.rect(screen, (255, 0, 0), obj.rect, 5)

                if obj.unqueue_self or (obj != mario and obj.position[1] >= death_level):
                    gameobjects.remove(obj)

                if obj.add_obj == True:
                    gameobjects.append(obj.object_inside)
                    if obj.object_inside.object_type=="Coin":
                        mario.coins+=1
                        obj.object_inside.unqueue_self = True

                    obj.add_obj = False
        
        if mario.alive == False:
            game_paused = True
            screen.blit(game_font.render('Press r to restart', True, (255, 255, 255), None), dest=(320,233))

        screen.blit(game_font.render("coins: " + str(mario.coins), True, (255, 255, 255), None), dest=(15,15))

        pygame.display.flip()

    pygame.quit()

main()