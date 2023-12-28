from gameobjectclass import*

friction_force = 2

def sign(val):
    if val < 0:
        return -1
    return 1

def lerp(a, b, t):

    if abs(a-b) < 0.001:
        return b 

    return (1 - t) * a + t * b

def clamp(val, min, max):

    if val < min:
        return min
    
    if val > max:
        return max
    
    return val

class player(gameobject):

    def __init__(self, speed, jump, accel):

        super().__init__(
            pos=[0,0], 
            vel=[0,0], 
            width=114, 
            height=95, 
            scale=1, 
            image_path="Sprites/Mario", 
            is_animated=True, 
            static=False
        )
        
        self.speed = speed
        self.accel = accel
        self.jump_velocity = jump

        self.powered_up = False

        self.is_moving = False

    def jump(self):
        
        if self.grounded == True:
            self.velocity[1] = -self.jump_velocity
            self.grounded = False

    def move(self, direction):
        self.is_moving = True
        self.direction = direction
        self.velocity[0] += self.accel*direction

    def update_position(self, gravity):

        self.velocity[0] = clamp(self.velocity[0], -self.speed, self.speed)

        if self.is_moving == False and self.velocity[0] != 0:
            self.velocity[0] = lerp(self.velocity[0], 0, (abs(self.velocity[0])/self.speed)/friction_force)

        if self.is_moving and self.obstructed_left and self.direction == -1:
            self.velocity[0] = 0

        if self.is_moving and self.obstructed_right and self.direction == 1:
            self.velocity[0] = 0

        if self.obstructed_top and self.velocity[1] < 0:
            self.velocity[1] = 0

        super().update_position(gravity)

    def check_collisions(self, objects):
        super().check_collisions(objects)