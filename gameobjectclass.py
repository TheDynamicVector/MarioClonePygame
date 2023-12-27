import pygame

class gameobject():

    def __init__(self, pos, width, height, image_path, is_animated=False, static=True, vel=[0,0], scale=1, transparent=True, collidable=True):
        
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

        self.collisions = []


        self.sprite = pygame.image.load(image_path + ".png").convert()
        self.get_current_frame()

    def get_current_frame(self):

        self.rendered_sprite = pygame.Surface((self.width, self.height)).convert_alpha()
        self.rendered_sprite.blit(self.sprite, (0,0), ((self.frame*self.width), 0, self.width, self.height))
        self.rendered_sprite = pygame.transform.scale(self.rendered_sprite, (self.width*self.scale, self.height*self.scale))
        
        if self.direction == -1:
            self.rendered_sprite = pygame.transform.flip(self.rendered_sprite, True, False)

        if self.transparent:
            self.rendered_sprite.set_colorkey((0,0,0))

    def check_collisions(self, objects):

        coll_list = []

        for o in objects:

            if o != self and o.collidable == True and pygame.Rect.colliderect(self.rect, o.rect):
                
                coll_list.append(o)

                if abs(self.rect.bottom - o.rect.top) <= 56:
                    self.grounded = True

        self.collisions = coll_list
    
    def update_position(self, gravity):
        
        if self.static == False and self.grounded == False:
            self.velocity[1] += gravity

        elif self.velocity[1] >= 0:
            self.velocity[1] = 0

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
