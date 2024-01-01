from gameobjectclass import*

death_level = 800

class player(gameobject):

    def __init__(self, speed, jump, accel):

        super().__init__(
            pos=[200,100], 
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
                "Death" : [6],
                "Powered_Idle": [7],
                "Powered_Walk" : [8,9,10],
                "Powered_Jump" : [12]
            },
            speed=speed,
            accel=accel,
            object_type="Player"
        )
        
        self.jump_velocity = jump

        self.powered_up = True

        self.alive = True

        self.coins = 0

        self.power_up()

    def jump(self, half_jump=False):

        if self.grounded == True:

            self.velocity[1] = -self.jump_velocity
            if half_jump:
                self.velocity[1] *= 0.75
            
            self.grounded = False

    def update_position(self, gravity):

        super().update_position(gravity)

        if self.alive == True and self.position[1] >= death_level:
            self.die()

    def check_collisions(self, objects):

        super().check_collisions(objects)

        for col in self.collisions:

            if col.object_type == "Enemy":
                if col.rect.bottom <= self.rect.bottom:
                    self.die()
                elif col.alive == True:
                    col.die()
                    self.jump(half_jump=True)

            if col.object_type == "Coin":
                col.unqueue_self = True
                self.coins += 1

            if col.object_type == "Mushroom":
                col.unqueue_self = True
                self.power_up()

    def power_up(self):
        self.powered_up = True
        self.height *= 2
        self.position[1] -= self.height/2
        self.get_current_frame()
        self.set_frame()

    def power_down(self):
        self.powered_up = False
        self.height /= 2
        self.position[1] += self.height/2
        self.get_current_frame()
        self.set_frame()

    def die(self):
        if self.powered_up:
            self.power_down()
        else:
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
        
    def set_frame(self):
        bef_frame = self.anim_frame
        super().set_frame()
        print(bef_frame==self.anim_frame)

    def change_anim(self, new_anim):
        if new_anim != self.current_anim:
            self.current_anim = new_anim    
            if self.powered_up:
                self.current_anim = "Powered_" + new_anim
            self.anim_frame = 0
            self.set_frame()