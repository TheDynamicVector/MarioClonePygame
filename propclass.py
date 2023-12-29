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
            collidable=False
        )
        
