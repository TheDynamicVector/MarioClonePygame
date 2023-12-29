from gameobjectclass import*

class coin(gameobject):

    def __init__(self, pos, type):

        super().__init__(
            pos=pos, 
            vel=[0,0], 
            width=40, 
            height=56, 
            scale=1, 
            image_path="Sprites/Coin", 
            is_animated=False, 
            static=True,
            draw_order=-1,
            transparent=True,
            collidable=False
        )