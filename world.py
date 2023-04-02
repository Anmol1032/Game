from perlin_noise import PerlinNoise
from ursina import *

world_entity: Entity | None = None


class Tp(Entity):
    def __init__(self, **kwargs):
        super(Tp, self).__init__(model='sphere', color=color.rgba(10, 255, 255), **kwargs)
        self.collider = 'sphere'
        self.tp = Tp


class TpTer(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        # self.parent = camera.ui
        self.point1 = Entity(parent=self, model=Circle(32, mode='point', thickness=.01), color=color.white, y=0,
                             scale=10, texture='circle')
        self.point2 = Entity(parent=self.point1, model=Circle(16, mode='point', thickness=.03), color=color.white,
                             scale=.75, texture='circle')
        self.point3 = Entity(parent=self.point2, model=Circle(8, mode='point', thickness=.02), color=color.white,
                             scale=.6, texture='circle')

        self.cube = Entity(parent=self.point3, model=Cube(subdivisions=(1, 1, 1), mode='line', thickness=2),
                           color=color.cyan, scale=3.2)

        self.center = Entity(parent=self.cube, model=Cube(), color=color.rgba(10, 255, 255, 37), scale=0.1)
        self.tp = Tp(parent=self.center, scale=0.75)

        self.scale = 1
        self.y = -.25

        # camera.orthographic = True

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.point3.rotation_x += 40 * time.dt

        self.point2.rotation_x += 20 * time.dt
        self.point2.rotation_y += 28 * time.dt

        self.point1.rotation_x += 8 * time.dt
        self.point1.rotation_y += 12 * time.dt
        self.point1.rotation_z += 20 * time.dt


class Teleport(Entity):
    def __init__(self, **kwargs):
        super(Teleport, self).__init__(**kwargs)
        self.start = TpTer(**kwargs)
        self.start.y = terraincast(self.start.world_position, world_entity) + 10
        self.world_position = self.start.world_position

    def set(self, gate):
        if hasattr(gate, 'start'):
            self.start.tp.gate = gate.start.world_position + Vec3(0, -6, 0)
        elif hasattr(gate, 'world_position'):
            self.start.tp.gate = gate.world_position
        else:
            self.start.tp.gate = gate


def init():
    global world_entity

    grass = load_texture('grass')

    # the land
    noise = PerlinNoise(octaves=10)

    hv = [[noise([x / 75, z / 75]) * 7.5 for x in range(75)] for z in range(75)]

    world_entity = Entity(model=Terrain(height_values=hv), scale=512, texture=grass, collider='mesh',
                          texture_scale=[32, 32], color=color.rgba(13, 69, 100), enabled=False)

    def w_update():
        world_entity.texture_offset += Vec2(0.1, 0.1) * Vec2(random.uniform(-1, 1), random.uniform(-1, 1)) * time.dt

    world_entity.update = w_update

    # the sky
    sky = Sky(scale=74, color=color.rgba(3, 37, 37))

    # and black fog also
    camera.clip_plane_far = 75
    scene.fog_density = (37, 73)
    scene.fog_color = color.clear



    return world_entity



if __name__ == '__main__':
    from ursina.prefabs.first_person_controller import FirstPersonController
    from ursina import curve

    app = Ursina()
    player = FirstPersonController(y=100, speed=50)
    # EditorCamera()

    init()

    # fps checker
    center = Entity(model='sphere', color=color.white, position=[20, 10, 20])
    for i in range(500):
        FPS_red = Entity(parent=center, model='sphere', color=color.random_color(), scale=random.uniform(.001, .5),
                         position=[random.uniform(-20, 20), random.uniform(-20, 20), random.uniform(-20, 20)])
    center.animate_rotation(Vec3(137, 500, 1255), 20, delay=3, curve=curve.linear)
    app.run()
