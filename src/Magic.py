__all__ = ["Magic"]

from Collider import Collider
import util

from Vector2 import Vector2
import config

# Local settings
MAGIC_SPEED = Vector2(3, 3)
MAGIC_ATTACK_IMAGE = "fireballRight.png"

class Magic(Collider):
        '''
                Magic class for the magic attack
        '''
        loadedImage = 0

        def __init__(self, x, y):
            super(Magic,self).__init__()

            if Magic.loadedImage == 0:
                Magic.loadedImage,tmp = util.loadImage(MAGIC_ATTACK_IMAGE)

            self.setImage(Magic.loadedImage)

            self.setPos(x, y)

            self.setVel(Vector2(MAGIC_SPEED))

        #Use to find coordinates of mouse relative to current pos. Set Vector
        def magicPath(self):
                pass

        def update(self, clock, environment):
            super(Magic,self).update(clock, environment, True)

            #Kill magic object if it reaches the windows bounds.
            if self.rect.top > config.HEIGHT or self.rect.top < 0 or self.rect.right < 64 or self.rect.right > config.WIDTH - 64:
                self.kill()
