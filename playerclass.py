from gameobjectclass import*

death_level = 800

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
            static=False,
            animation_dict= {
                "Idle" : [0],
                "Walk" : [1,2,3],
                "Jump" : [5],
                "Death" : [6]
            },
            speed=speed,
            accel=accel,
            is_player=True
        )
        
        self.jump_velocity = jump

        self.powered_up = False

        self.alive = True

        self.coins = 15

    def jump(self, half_jump=False):

        if self.grounded == True:

            self.velocity[1] = -self.jump_velocity
            if half_jump:
                self.velocity[1] = -self.jump_velocity*0.75
            
            self.grounded = False

    def update_position(self, gravity):

        super().update_position(gravity)

        if self.bottom_collision != None and self.bottom_collision.is_enemy and self.bottom_collision.alive:
            self.bottom_collision.kill_self()
            self.jump(half_jump=True)

        if self.alive == True:
            if self.position[1] >= death_level or (self.left_collision != None and self.left_collision.is_enemy) or (self.right_collision != None and self.right_collision.is_enemy) or (self.top_collision != None and self.top_collision.is_enemy):
                self.die()

    def die(self):
        self.alive = False
        self.change_anim("Death")

    def get_current_frame(self):

        if self.is_moving == False and self.grounded == True:
            self.change_anim("Idle")

        if self.grounded == False:
            self.change_anim("Jump")

        if self.alive == False:
            self.change_anim("Death")

        super().get_current_frame()
        
