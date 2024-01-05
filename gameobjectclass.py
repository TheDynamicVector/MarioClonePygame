import pygame
from time import*

collision_margin = 15
animation_speed = 0.1

friction_force = 2

def lerp(a, b, t):

    if abs(a-b) < 0.005:
        return b 

    return (1 - t) * a + t * b

def clamp(val, min, max):

    if val < min:
        return min
    
    if val > max:
        return max
    
    return val

def sign(val):
    if val < 0:
        return -1
    return 1

class gameobject():

    def __init__(self, pos, width, height, image_path, direction=1, is_animated=False, static=True, vel=[0,0], scale=1, transparent=True, collidable=True, animation_dict={}, self_moving=False, speed=244, accel=23, draw_order=0, register_collisions=True, object_type="", frame=0, one_shot_animation=False, collision_offset=[0,0], collision_size=[1,1]):
        
        self.position = pos
        self.velocity = vel 

        self.unqueue_after_anim = False

        self.one_shot_animation = one_shot_animation

        self.collision_offset = collision_offset
        self.collision_size = collision_size
        
        self.object_type = object_type

        self.static = static
        self.collidable = collidable

        self.width = width
        self.height = height
        self.scale = scale

        self.frame = frame
        self.is_animated = is_animated

        self.direction = direction

        self.transparent = transparent

        self.rect = pygame.Rect(0,0,0,0)

        self.grounded = False
        self.obstructed_left = False
        self.obstructed_right = False
        self.obstructed_top = False

        self.bottom_collision = None
        self.top_collision = None
        self.left_collision = None
        self.right_collision = None

        self.collisions = []

        self.animation_dict = animation_dict

        self.current_anim = "Idle"
        self.frame_time = 0
        self.anim_frame = 0

        self.self_moving = self_moving

        self.speed = speed
        self.accel = accel

        self.is_moving = False
        
        self.register_collisions = register_collisions

        self.unqueue_self = False

        self.sprite = pygame.image.load(image_path + ".png").convert()

        self.draw_order = draw_order

        self.alive = True

        self.add_obj = False

    def set_frame(self):

        self.anim_frame += 1

        if self.one_shot_animation and self.anim_frame >= len(self.animation_dict[self.current_anim]):
            self.change_anim("Idle")
            if self.unqueue_after_anim:
                self.unqueue_self = True
            return
        
        self.anim_frame = self.anim_frame % len(self.animation_dict[self.current_anim])
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

        self.collisions = []
        
        if self.collidable == False:
            return
        
        self.grounded = False
        self.obstructed_left = False
        self.obstructed_right = False
        self.obstructed_top = False

        self.bottom_collision = None
        self.top_collision = None
        self.left_collision = None
        self.right_collision = None

        for o in objects:

            if o != self and o.register_collisions == True and pygame.Rect.colliderect(self.rect, o.rect):
                
                self.collisions.append(o)

                if o.collidable == True:
                    if abs(self.rect.bottom - o.rect.top) <= collision_margin:
                        self.grounded = True
                        self.bottom_collision = o

                    else:

                        if abs(self.rect.right - o.rect.left) <= collision_margin:
                            self.obstructed_right = True
                            self.right_collision = o

                        if abs(self.rect.left - o.rect.right) <= collision_margin:
                            self.obstructed_left = True
                            self.left_collision = o

                        if abs(self.rect.top - o.rect.bottom) <= collision_margin:
                            self.obstructed_top = True
                            self.right_collision = o

    
    def move(self, direction):
        

        if self.is_animated:
            self.change_anim("Walk")
        self.is_moving = True
        self.direction = direction
        self.velocity[0] += self.accel*direction

    def update_position(self, gravity, delta):
        
        self.velocity[0] = clamp(self.velocity[0], -self.speed, self.speed)

        if self.is_moving == False and self.velocity[0] != 0:
            self.velocity[0] = lerp(self.velocity[0], 0, (abs(self.velocity[0])/self.speed)/friction_force)

        velocity_dir = sign(self.velocity[0])

        if self.is_moving and self.obstructed_left and velocity_dir == -1:
            self.velocity[0] = 0

        if self.is_moving and self.obstructed_right and velocity_dir == 1:
            self.velocity[0] = 0

        if self.obstructed_top and self.velocity[1] < 0:
            self.velocity[1] = 0
        
        if self.static == False and self.grounded == False:
            self.velocity[1] += gravity*delta

        elif self.velocity[1] >= 0:
            self.velocity[1] = 0

        if self.self_moving and self.alive:
            self.move(self.direction)
            if (self.obstructed_left and self.direction == -1) or (self.obstructed_right and self.direction == 1):
                self.direction *= -1

        self.position[0] += self.velocity[0]*delta
        self.position[1] += self.velocity[1]*delta

    def change_anim(self, new_anim):
        if new_anim != self.current_anim:
            self.current_anim = new_anim
            self.anim_frame = 0
            self.set_frame()
