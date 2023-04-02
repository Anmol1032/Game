import itertools

from mobs.main_class import *

model = Mesh(
            vertices=[(.5, 0, 0), (0, 0, -.5), (-.5, 0, 0), (0, 0, .5), (0, -.5, 0), (0, .5, 0)],
            triangles=[4, 0, 1, 4, 1, 2, 4, 2, 3, 4, 3, 0, 5, 1, 0, 5, 2, 1, 5, 3, 2, 5, 0, 3],
            uvs=((1, 0), (0, 1), (-1, 0), (0, -1)),
            mode='triangle')

class Graster(Enemy):
    def __init__(self, **kwargs):
        self.its_type = 'graper'
        self.tag = '#fly#shout'

        self.max_hp = 45
        self.hp = self.max_hp

        self.xp_to_give = 9


        super(Graster, self).__init__(model=model, collider='mesh', scale=2, **kwargs)


        self.can_damage = True

        self.rot = self.animate_rotation_y(0)


        self.cu = itertools.cycle([curve.in_circ, curve.out_circ])
        self.va = itertools.cycle([-1, -2, 4, 6])

    def sound(self):
        sound = Audio('coin_1', pitch=0.7492, volume=1)
        sound.position = self.position

    def update(self):

        dist = distance(self.player, self)

        if dist < 3:
            if self.can_damage:
                self.can_damage = False
                invoke(setattr, self, 'can_damage', True, delay=1)
                self.player.hp -= 10

        elif dist < 15:

            t = Vec3(10, 5, 0)

            t.xz = rotate_point_2d(t.xz, Vec3(0, 0, 0), self.rotation_y / 8)

            self.world_position = lerp(
                self.world_position,
                self.player.world_position + t,
                time.dt * 2.7)


            if self.rot.finished:
                self.blink(duration=0.5)
                self.shout()
                self.rot = self.animate_rotation_y(self.rotation_y + 90 * random.uniform(1, 4) * next(self.va), duration=5,
                                            curve=next(self.cu))

        else:
            self.look_at_2d(self.player, 'y')
            self.position += self.forward * 15 * time.dt

        super(Graster, self).update()

    def shout(self):
        e = Entity(model='sphere', color=color.green, collider='sphere', position=self.position)
        invoke(destroy, e, delay=10)

        def update_e():
            e.position += (self.player.position - e.position + Vec3(0, 2, 0)).normalized() * time.dt * 9

            if distance_xz(self.player.position, e.position) < 2:
                destroy(e)
                self.player.hp -= 10

        e.update = update_e

