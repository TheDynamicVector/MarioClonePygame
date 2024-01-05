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
gravity = 1433

gameobjects = []

grid_size = 63

def main():

    game_running = True
    game_paused = False

    gameobjects = []

    mario = player(speed = 777, accel = 23, jump = 988)
    gameobjects.append(mario)


    #Level Creation
    for i in range(-5,70):
        gameobjects.append(ground_block(pos=[i*grid_size, 450]))

    for i in range(80,110):
        gameobjects.append(ground_block(pos=[i*grid_size, 450]))

    gameobjects.append(question_block(pos=[1071,135], object_inside="Coin"))
    gameobjects.append(question_block(pos=[1512,-54], object_inside="Coin"))

    gameobjects.append(question_block(pos=[1449,135], object_inside="Mushroom"))
    gameobjects.append(question_block(pos=[1575,135], object_inside="Coin"))

    for i in range(0,5):
        gameobjects.append(coin(pos=[1400 + grid_size*i,310]))

    for i in range(0,5):
        gameobjects.append(coin(pos=[2050 + grid_size*i, 180]))

    for i in range(0,10):
        gameobjects.append(coin(pos=[3250 + grid_size*i, 310]))

    for i in range(0,5):
        gameobjects.append(coin(pos=[4650 + grid_size*i, 180]))

    gameobjects.append(brick(pos=[1512,135]))
    gameobjects.append(brick(pos=[1386,135]))
    gameobjects.append(brick(pos=[1638,135]))

    gameobjects.append(goomba(pos=[1386,100]))

    gameobjects.append(pipe(pos=[1890,120], pipe_index=0))
    gameobjects.append(goomba(pos=[2100,200]))

    gameobjects.append(pipe(pos=[2394,120], pipe_index=1))
    gameobjects.append(goomba(pos=[2680,200]))
    gameobjects.append(goomba(pos=[2800,200]))

    gameobjects.append(pipe(pos=[2898,120], pipe_index=2))

    gameobjects.append(question_block(pos=[5985,135], object_inside="Mushroom"))
    gameobjects.append(brick(pos=[5923,135]))
    gameobjects.append(brick(pos=[6048,135]))

    gameobjects.append(pipe(pos=[1890,120], pipe_index=0))
    
    gameobjects.append(pipe(pos=[5040,120], pipe_index=0))
    gameobjects.append(pipe(pos=[6803,120], pipe_index=0))

    gameobjects.append(koopa(pos=[6500,200]))

    camera_x = 0
    camera_y = 0

    camera_x_offset = 400
    camera_y_offset = 350

    last_time = 0

    while game_running:
        curr_time = pygame.time.get_ticks()
        delta = min((curr_time-last_time)/1000, 0.1)
        last_time = curr_time

        #Key Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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

        for obj in sorted_objects:

            relative_x = obj.position[0]+camera_x
            relative_y = obj.position[1]-camera_y

            if relative_x < screen.get_width()+600 and relative_x > -600:
     
                obj.rect = pygame.Rect(relative_x, relative_y, obj.width*obj.scale, obj.height*obj.scale)
                
                obj.get_current_frame()

                if game_paused == False:
                    obj.update_position(gravity, delta)

                screen.blit(obj.rendered_sprite, obj.rect)

                if obj.collidable == True:
                    obj.rect = pygame.Rect(relative_x-obj.collision_offset[0], relative_y-obj.collision_offset[1], obj.width*obj.scale*obj.collision_size[0], obj.height*obj.scale*obj.collision_size[1])
                    obj.check_collisions(gameobjects) 
                    
                #pygame.draw.rect(screen, (255, 0, 0), obj.rect, 5)

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