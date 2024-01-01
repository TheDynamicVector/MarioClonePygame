from gameobjectclass import*

size_hash = {
    "Hill" : [395,94],
    "HardBlock" : [63,63],
    "Block" : [200, 240]
}

class block(gameobject):

    def __init__(self, pos, type, index=0, breakable=False, scale=1, animation_dict={}):

        super().__init__(
            pos=pos, 
            vel=[0,0], 
            width=size_hash[type][0], 
            height=size_hash[type][1], 
            scale=scale, 
            animation_dict=animation_dict,
            image_path="Sprites/" + type,
            frame=index,
            is_animated=breakable, 
            static=True,
            draw_order=-1,
            object_type= "BreakableBlock" if breakable else "",
            one_shot=True,
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
            animation_dict={ "Idle" : [0], "Shift" : [1,1,0] },
        )

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
            collidable=False,
            register_collisions=True,
            self_moving=True,
            object_type="Mushroom"
        )