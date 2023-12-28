import pygame
from time import*

collision_margin = 15
animation_speed = 0.1
class gameobject():

    def __init__(self, pos, width, height, image_path, is_animated=False, static=True, vel=[0,0], scale=1, transparent=True, collidable=True, animation_dict={}):
        
        self.position = pos
        self.velocity = vel 

        self.static = static
        self.collidable = collidable

        self.width = width
        self.height = height
        self.scale = scale

        self.frame = 0
        self.is_animated = is_animated

        self.direction = 1

        self.transparent = transparent

        self.rect = pygame.Rect(0,0,0,0)

        self.grounded = False
        self.obstructed_left = False
        self.obstructed_right = False
        self.obstructed_top = False

        self.collisions = []

        self.animation_dict = animation_dict

        self.current_anim = "Idle"
        self.frame_time = 0
        self.anim_frame = 0

        self.sprite = pygame.image.load(image_path + ".png").convert()

    def set_frame(self):
        self.anim_frame = (self.anim_frame+1) % len(self.animation_dict[self.current_anim])
        self.frame = self.animation_dict[self.current_anim][self.anim_frame]
        self.frame_time = time()

    def get_current_frame(self):

        if self.is_animated:
            delta = time() - self.frame_time
            if delta >= animation_speed:
                self.set_frame()

        self.rendered_sprite = pygame.Surface((self.width, self.height)).convert_alpha()
        self.rendered_sprite.blit(self.sprite, (0,0), ((self.frame*self.width), 0, self.width, self.height))
        self.rendered_sprite = pygame.transform.scale(self.rendered_sprite, (self.width*self.scale, self.height*self.scale))
        
        if self.direction == -1:
            self.rendered_sprite = pygame.transform.flip(self.rendered_sprite, True, False)

        if self.transparent:
            self.rendered_sprite.set_colorkey((0,0,0))

    def check_collisions(self, objects):

        coll_list = []
        
        self.grounded = False
        self.obstructed_left = False
        self.obstructed_right = False
        self.obstructed_top = False

        for o in objects:

            if o != self and o.collidable == True and pygame.Rect.colliderect(self.rect, o.rect):
                
                coll_list.append(o)

                if abs(self.rect.bottom - o.rect.top) <= collision_margin:
                    self.grounded = True

                else:

                    if abs(self.rect.right - o.rect.left) <= collision_margin:
                        self.obstructed_right = True

                    if abs(self.rect.left - o.rect.right) <= collision_margin:
                        self.obstructed_left = True

                    if abs(self.rect.top - o.rect.bottom) <= collision_margin:
                        self.obstructed_top = True

        self.collisions = coll_list
    
    def update_position(self, gravity):
        
        if self.static == False and self.grounded == False:
            self.velocity[1] += gravity

        elif self.velocity[1] >= 0:
            self.velocity[1] = 0

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def change_anim(self, new_anim):

        if new_anim != self.current_anim:
            self.current_anim = new_anim
            self.anim_frame = 0
            self.set_frame()
