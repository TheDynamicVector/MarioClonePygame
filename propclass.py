from gameobjectclass import*

size_hash = {
    "Hill" : [395,94]
}

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