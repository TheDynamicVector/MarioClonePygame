import pygame

class gameobject():

    def __init__(self, pos, width, height, image_path, is_animated=False, static=True, vel=[0,0], scale=1, transparent=True):
        
        self.position = pos
        self.velocity = vel 

        self.static = static

        self.width = width
        self.height = height
        self.scale = scale

        self.frame = 0
        self.is_animated = is_animated

        self.direction = 1

        self.transparent = transparent

        self.grounded = False

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

    def update_position(self, gravity):

        if self.position[1] >= 270:
            self.grounded = True

        if self.static == False and self.grounded == False:
            self.velocity[1] += gravity

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]