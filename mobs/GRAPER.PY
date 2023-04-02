from mobs.main_class import *

class Graper(Enemy):
    def __init__(self, **kwargs):
        self.its_type = 'graper'
        self.tag = '#terraincast'

        self.max_hp = 10
        self.hp = self.max_hp

        self.xp_to_give = 2
        super(Graper, self).__init__(model='cube', collider='box', **kwargs)



        self.can_damage = True

    def sound(self):
        from ursina.prefabs.ursfx import ursfx
        sound = ursfx([(0.0, 1.0), (0.01, 0.8), (0.06, 1.0), (0.99, 1.0), (1.0, 0.6)], volume=30, wave='coin_1',
                      pitch=8,
                      speed=2.5)
        sound.position = self.position

    def update(self):

        if distance(self.player, self) < 2:
            if self.can_damage:
                self.can_damage = False
                invoke(setattr, self, 'can_damage', True, delay=1)
                self.player.hp -= random.randint(0, 1)
        else:
            # self.position = lerp(self.position, self.player.position, time.dt / 6)
            self.position += self.forward * time.dt \
                             * (curve.in_cubic(1.3 - self.hp / self.max_hp) + 0.4) * 7

        self.look_at_2d(self.player, 'y')

        self.y = terraincast(self.world_position, self.world_entity) + 1

        super(Graper, self).update()
