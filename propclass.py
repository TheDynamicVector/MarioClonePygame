from gameobjectclass import*

size_hash = {
    "Hill" : [395,94],
    "HardBlock" : [63,63],
    "Block" : [200, 240],
    "Trees" : [165,197],
    "Castle" : [581,713]
}

class block(gameobject):

    def __init__(self, pos, type, index=0, breakable=False, scale=1, animation_dict={}, collision_offset=[0,0], collision_size=[1,1]):

        super().__init__(
            pos=pos, 
            vel=[0,0], 
            width=size_hash[type][0], 
            height=size_hash[type][1], 
            scale=scale, 
            collision_offset=collision_offset,
            collision_size=collision_size,
            animation_dict=animation_dict,
            image_path="Sprites/" + type,
            frame=index,
            is_animated=breakable, 
            static=True,
            draw_order=-1,
            object_type= "BreakableBlock" if breakable else "",
            one_shot_animation=True,
            transparent=breakable
        )

        self.breakable = breakable

class hard_block(block):

    def __init__(self, pos):

        super().__init__(
            pos=pos, 
            type="HardBlock",
        )

class brick(block):

    def __init__(self, pos):

        super().__init__(
            pos=pos, 
            type="Block",
            scale=0.32,
            index=0,
            breakable=True,
            collision_offset=[0,-12],
            collision_size=[1,0.8],
            animation_dict={ "Idle" : [0], "Shift" : [0,1,1,0], "Break" : [1,2] },
        )

    def break_block(self, block_broke=False):
        if block_broke:
            self.change_anim("Break")
            self.collidable = False
            self.register_collisions = False
            self.unqueue_after_anim = True

        else:
            self.change_anim("Shift")


class question_block(block):

    def __init__(self, pos, object_inside="Coin"):

        super().__init__(
            pos=pos, 
            type="Block",
            scale=0.32,
            index=5,
            breakable=True,
            collision_offset=[0,-12],
            collision_size=[1,0.8],
            animation_dict={ "Idle" : [5], "Shift" : [3,4,4,3], "Break" : [5,6,7,3] },
        )

        self.empty = False

        if object_inside == "Coin":
            self.object_inside = coin(pos=[self.position[0]+11, self.position[1] - 50])

        elif object_inside == "Mushroom":
            self.object_inside = mushroom(pos=[self.position[0]+11, self.position[1] - 50])

    def break_block(self, powered_up=False):
        
        if self.empty:
            self.change_anim("Shift")

        else:
            self.change_anim("Break")
            self.animation_dict["Idle"] = [3]
            self.empty=True
            self.add_obj = True


class prop(gameobject):

    def __init__(self, pos, type, scale):

        super().__init__(
            pos=pos, 
            vel=[0,0], 
            width=size_hash[type][0], 
            height=size_hash[type][1], 
            scale=scale, 
            image_path="Sprites/" + type, 
            is_animated=False, 
            static=True,
            draw_order=-2,
            transparent=True,
            collidable=False,
            register_collisions=False
        )
        

class coin(gameobject):

    def __init__(self, pos):

        super().__init__(
            pos=pos, 
            width=40, 
            height=56, 
            scale=1, 
            image_path="Sprites/Coin", 
            is_animated=False, 
            static=True,
            transparent=True,
            collidable=False,
            object_type="Coin"
        )

class mushroom(gameobject):

    def __init__(self, pos):

        super().__init__(
            pos=pos, 
            vel=[0,0], 
            width=225, 
            height=225, 
            scale=0.3, 
            image_path="Sprites/Mushroom", 
            is_animated=False, 
            static=False,
            transparent=True,
            collidable=True,
            register_collisions=True,
            self_moving=True,
            object_type="Mushroom"
        )