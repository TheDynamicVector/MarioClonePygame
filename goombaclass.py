from gameobjectclass import*

class goomba(gameobject):

    def __init__(self, pos):

        super().__init__(
            pos=pos, 
            vel=[0,0], 
            width=164, 
            height=161, 
            scale=0.5, 
            image_path="Sprites/Goomba", 
            is_animated=True, 
            static=False,
            animation_dict= {
                "Idle" : [0],
                "Walk" : [0,1],
                "Death" : [2]
            },
            speed=0.2,
            accel=0.5,
            self_moving=True,
            is_enemy=True,
        )
        
        self.alive = True
        self.time_of_death = 0

    def get_current_frame(self):

        if self.is_moving == False and self.grounded == True:
            self.change_anim("Walk")

        if self.grounded == False:
            self.change_anim("Idle")

        if self.alive == False:
            self.change_anim("Death")

        super().get_current_frame()

    def kill_self(self):
        if self.alive == True:
            self.alive = False
            self.time_of_death = time()
            self.change_anim("Death")
            self.collidable = False

    def update_position(self, gravity):
        
        if self.alive == False and time()-self.time_of_death >= 1:
            self.unqueue_self = True

        super().update_position(gravity)
        
