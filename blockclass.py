from gameobjectclass import*

class block(gameobject):

    def __init__(self, pos, type):

        super().__init__(
            pos=pos, 
            vel=[0,0], 
            width=63, 
            height=63, 
            scale=1, 
            image_path="Sprites/" + type, 
            is_animated=False, 
            static=True,
            draw_order=-1,
            transparent=False
        )
        
