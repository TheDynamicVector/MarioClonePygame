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
            speed=233,
            accel=11,
            self_moving=True,
            object_type="Enemy",
            direction=-1
        )
        
        self.time_of_death = 0

    def get_current_frame(self):

        if self.is_moving == False and self.grounded == True:
            self.change_anim("Walk")

        if self.grounded == False:
            self.change_anim("Idle")

        if self.alive == False:
            self.change_anim("Death")

        super().get_current_frame()

    def die(self, player):
        if self.alive == True:
            self.alive = False
            self.time_of_death = time()
            self.change_anim("Death")
            self.collidable = False

    def update_position(self, gravity, delta):
        
        if self.alive == False and time()-self.time_of_death >= 1:
            self.unqueue_self = True

        super().update_position(gravity, delta)
        
class koopa(gameobject):

    def __init__(self, pos):

        super().__init__(
            pos=pos, 
            vel=[0,0], 
            width=180, 
            height=223, 
            scale=0.45, 
            image_path="Sprites/Koopa", 
            is_animated=True, 
            static=False,
            animation_dict= {
                "Idle" : [3],
                "Walk" : [3,2],
                "Shelled" : [3,0,1,0],
                "Death" : [0]
            },
            speed=233,
            accel=25,
            self_moving=True,
            object_type="Enemy",
            collision_size=[1,0.8],
            collision_offset=[0,-23],
            direction=-1
        )
        self.shelled = False
        self.time_of_death = 0

    def get_current_frame(self):

        if self.grounded == True:
            self.change_anim("Walk")

        else:
            self.change_anim("Idle")

        if self.shelled == True:
            self.change_anim("Death")

        super().get_current_frame()

    def die(self, player):

        if self.shelled:
            if time() - self.time_of_death > 0.1:
                if abs(player.position[0] - self.position[0]) < 23:
                    self.alive = False
                    self.collidable = False
                    self.velocity = [0.1,0]
                    self.grounded = False
                    self.register_collisions = False

                else:
                    self.speed = 755
                    self.time_of_death = time()
                    self.self_moving = True

                    if player.position[0] < self.position[0]:
                        self.velocity[0] = self.speed
                    else:
                        self.velocity[0] = -self.speed

        else:
            self.change_anim("Death")
            self.shelled = True
            self.velocity[0] = 0
            self.self_moving = False
            self.collidable = True
            self.register_collisions = True
            self.time_of_death = time()