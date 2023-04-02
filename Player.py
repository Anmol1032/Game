import ursina.prefabs.first_person_controller as fpc
from ursina import curve
from ursina.prefabs.health_bar import HealthBar
from ursina import *


class FPC(fpc.FirstPersonController):
    def __init__(self, **kwargs):
        super(FPC, self).__init__(**kwargs)


        camera.fov = 90

        self.speed = 10

        self.damage = 1

        self.max_xp = 1000
        self.xp = 50
        self.xp_bar = HealthBar(max_value=self.max_xp, origin=(0, 0), position=(0, -0.4),
                                bar_color=color.green.tint(-.4))
        self.xp_bar.bar.origin = (0, 0)
        self.xp_bar.lines.origin = (0, 0)
        self.xp_bar.collider = None
        self.xp_bar.roundness = .1
        self.xp_bar.value = self.xp

        self.max_hp = 200
        self.hp = self.max_hp
        self.prv_hp = self.hp

        self.hp_bar = HealthBar(max_value=self.max_hp, origin=(0, 0), position=(0, -0.45))
        self.hp_bar.bar.origin = (0, 0)
        self.hp_bar.lines.origin = (0, 0)
        self.hp_bar.collider = None
        self.hp_bar.roundness = .5

        self.can_heal = True
        self.can_heal_setter = invoke(setattr, self, 'can_heal', True, delay=5)

        self.enemy_bar = HealthBar(origin=(0, 0), position=(0, 0.35))
        self.enemy_bar.bar.origin = (0, 0)
        self.enemy_bar.lines.origin = (0, 0)
        self.enemy_bar.collider = None
        self.enemy_bar.roundness = .5
        self.enemy_bar.animation_duration = 0
        self.enemy_bar.visible = False

        self.enemy_name = Text(origin=(0, 0), position=(0, 0.4))
        self.enemy_name.color = color.white
        self.enemy_name.visible = False

        self.pos = Text("0, 0, 0", position=(-0.7, 0.45), scale=1.5)


    def update(self):
        super(FPC, self).update()

        if self.can_heal:
            self.hp += 1

        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            self.enemy_bar.visible = True
            self.enemy_bar.max_value = mouse.hovered_entity.max_hp
            self.enemy_bar.value = mouse.hovered_entity.hp

            self.enemy_name.visible = True
            self.enemy_name.text = str(mouse.hovered_entity.name).title()
        else:
            self.enemy_bar.visible = False
            self.enemy_name.visible = False

        self.pos.text = str(round(self.position, 0))[5:-1]

    def input(self, key):
        super(FPC, self).input(key)

        if key == Keys.left_mouse_down:
            if mouse.hovered_entity and distance(mouse.hovered_entity, self) < 10:
                if hasattr(mouse.hovered_entity, 'hp'):
                    mouse.hovered_entity.hp -= self.damage
                    mouse.hovered_entity.blink(color.red, duration=.1)

                elif hasattr(mouse.hovered_entity, 'xp_give'):
                    destroy(mouse.hovered_entity)
                    self.xp += mouse.hovered_entity.xp_give

        if key == Keys.right_mouse_down:
            if mouse.hovered_entity:
                if hasattr(mouse.hovered_entity, 'tp') and distance(mouse.hovered_entity.world_position, self) < 15:
                    mouse.hovered_entity.blink(color.clear, 0.773, curve=curve.in_quint)

                    Audio('teleport_1', pitch=1, volume=0.47)

                    self.animate_position(mouse.hovered_entity.gate, 2, curve=curve.in_out_circ, delay=0.3)
                    invoke(setattr, self, 'air_time', -0.1, delay=2)

    def damage_sound(self):
        sound = Audio('hurt_3', pitch=0.7973, volume=0.45, auto_destroy=True)
        sound.position = self.position

    def heal_sound(self):
        from ursina.prefabs.ursfx import ursfx
        sound = ursfx([(0.0, 0.08), (0.08, 0.72), (0.25, 0.5), (0.59, 1.0), (1.0, 0.0)], volume=0.67, wave='sine',
                      pitch=7, pitch_change=5, speed=2.9)
        sound.position = self.position

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

        if value <= 0:
            destroy(self)
            return

        self.can_heal_setter.kill()
        self.can_heal_setter = invoke(setattr, self, 'can_heal', True, delay=5)
        self.can_heal = False

        if value >= self.max_hp:
            self._hp = self.max_hp
            value = self.max_hp

        if value < self.prv_hp:
            self.damage_sound()

        if value > self.prv_hp:
            self.heal_sound()
            self.hp_bar.bar.blink(color.green, duration=.3)

        self.prv_hp = value
        self.hp_bar.value = value

    def xp_sound(self):
        from ursina.prefabs.ursfx import ursfx
        sound = ursfx([(0.0, 0.74), (0.11, 0.0), (0.58, 0.09), (0.6, 0.75), (1.0, 0.0)], volume=0.75, wave='triangle',
                      pitch=32,
                      pitch_change=7, speed=1.1)
        sound.position = self.position

    @property
    def xp(self):
        return self._xp

    @xp.setter
    def xp(self, value):
        self._xp = value

        if value >= self.max_xp:
            self._xp = self.max_xp
            value = self.max_xp
        else:
            self.xp_sound()

        self.xp_bar.value = value


player: FPC | None = None


def init():
    global player
    player = FPC(y=30, enabled=False)
    return player
