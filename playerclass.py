from gameobjectclass import*

class player(gameobject):

    def __init__(self, s, j):
        super().__init__([0,0], [0,0], 114, 190, 1, "Sprites/Mario", True, False)
        self.speed = s
        self.powered_up = False
        self.jump_velocity = j

    def jump(self):
        self.velocity[1] -= self.jump_velocity

