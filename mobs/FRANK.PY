import random

from mobs.main_class import *

model = Mesh(
    vertices=[(.5, .5, 0), (0, .5, -.5), (-.5, .5, 0), (0, .5, .5), (0, -.5, 0), (0, 1, 0)],
    triangles=[4, 0, 1, 4, 1, 2, 4, 2, 3, 4, 3, 0, 5, 1, 0, 5, 2, 1, 5, 3, 2, 5, 0, 3],
    uvs=((0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
)

class Frank(Enemy):
    def __init__(self, **kwargs):
        self.its_type = 'graper'
        self.tag = '#terraincast'

        self.max_hp = 25
        self.hp = self.max_hp

        self.xp_to_give = 5
        super(Frank, self).__init__(model=model, collider='mesh', **kwargs)

        self.can_damage = True



    def sound(self):
        sound = Audio('hurt_2', pitch=0.7492, volume=1)
        sound.position = self.position

    def update(self):

        if distance(self.player, self) < 2:
            if self.can_damage:
                self.can_damage = False
                invoke(setattr, self, 'can_damage', True, delay=1)
                self.player.hp -= 1
        else:
            self.position += self.forward * time.dt \
                             * (curve.in_cubic(1.3 - self.hp / self.max_hp) + 0.4) * 7

        self.look_at_2d(self.player, 'y')

        self.y = terraincast(self.world_position, self.world_entity) + 1

        super(Frank, self).update()