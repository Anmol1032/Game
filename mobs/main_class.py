from ursina import *
from ursina import curve
from ursina.shaders.noise_fog_shader import noise_fog_shader

import world


class Enemy(Entity):
    def __init__(self, player: Entity, **kwargs):
        super().__init__(origin_y=-.5, texture='grass', color=color.rgba(10, 205, 255, 215), **kwargs)

        self.kwargs = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)

        try:
            if not self.tag:
                pass
        except:
            self.its_type = 'type'
            self.tag = '#'
            self.max_hp = 10
            self.hp = self.max_hp
            self.xp_to_give = 10
            print('using defaults')

        self.shader = noise_fog_shader
        self.set_shader_input('dark_color', color.black)
        self.set_shader_input('light_color', color.green)
        self.t = 0
        # self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5, .1, .1))

        self.player = player
        self.world_entity = world.world_entity

        self.destroy_in = invoke(setattr, self, 'hp', 0, delay=random.uniform(20, 30))

    def die(self):
        self.s = Sequence(  # The style of destroying.
            Func(setattr, self, 'update', None),
            Func(setattr, self, 'collider', None),
            Func(setattr, self, 'shader', None),
            Wait(1),
            Func(self.animate_color, color.white66, 4, curve=curve.in_out_bounce),
            Func(self.animate_y, self.position.y + 4, 5.9, curve=curve.in_out_quint_boomerang),
            Wait(6),
            Func(self.animate_color, color.clear, 11, curve=curve.in_out_circ),
            Func(self.animate_scale, self.scale * 10, 10, curve=curve.in_circ),
            Wait(11),

            Wait(2),
            Func(destroy, self)
        )

        self.xp_summon()
        for anim in self.animations:
            anim.pause()
            anim.kill()

        self.s.start()



    def xp_summon(self):
        self.xp_giver = Entity()
        self.xp_giver.its_type = 'xp'
        self.xp_giver.position = self.position
        self.xp_giver.parent = self.parent
        self.xp_giver.color = color.cyan
        self.xp_giver.model = 'cube'
        self.xp_giver.collider = 'box'
        self.xp_giver.rotation = self.rotation
        self.xp_giver.texture = 'perlin_noise'

        self.xp_giver.shader = noise_fog_shader
        self.xp_giver.set_shader_input('dark_color', color.green)
        self.xp_giver.set_shader_input('light_color', color.blue)
        self.xp_giver.set_shader_input('time', 0)

        self.xp_giver.t = 0
        def xp_update():
            self.xp_giver.t += time.dt
            self.xp_giver.set_shader_input('time', self.xp_giver.t)

        self.xp_giver.update = xp_update

        setattr(self.xp_giver, 'xp_give', self.xp_to_give)


    def update(self):
        self.t += time.dt
        self.set_shader_input('time', self.t)

        '''
        self.texture_offset += Vec2(0.3, 0.5) * time.dt * random.uniform(-1, 3)
        self.texture_scale += Vec2(random.uniform(-1, 1), random.uniform(-0.5, 0.5)) * time.dt'''

    @staticmethod
    def sound():
        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 1.0), (0.01, 0.8), (0.06, 0.01), (0.99, 1.0), (1.0, 0.0)], volume=0.1, wave='square', pitch=38,
              speed=5)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value < self.max_hp:
            self.sound()
        if value <= 0:
            self.destroy_in.kill()
            self.die()
            return
        # self.health_bar.value = self.hp
