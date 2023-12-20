import pygame

class gameobject():

    def __init__(self, pos, vel, w, h, s, image_path, animated_img=False, stat=True):
        
        self.position = pos
        self.velocity = vel 

        self.static = stat

        self.width = w
        self.height = h
        self.scale = s

        self.frame = 0
        self.is_animated_img = animated_img
    
        self.sprite = pygame.image.load(image_path + ".png").convert()
        self.get_current_frame()

    def get_current_frame(self):

        self.rendered_sprite = pygame.Surface((self.width, self.height)).convert_alpha()
        self.rendered_sprite.blit(self.sprite, (0,0), ((self.frame*self.width), 0, self.width, self.height))
        self.rendered_sprite = pygame.transform.scale(self.rendered_sprite, (self.width*self.scale, self.height*self.scale))
        self.rendered_sprite.set_colorkey((0,0,0))

    def update_position(self, maxval):

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.position[1] = max(maxval, self.position[1])