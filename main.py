"""main file"""

from direct.stdpy import thread
from ursina import *
from ursina.prefabs.memory_counter import MemoryCounter
from ursina.shaders.noise_fog_shader import noise_fog_shader

import Player
import mobs
import world

app = Ursina(vsync=False)
app.step()

window.position = (50, -1)
window.color = color.black
app.step()

target = Entity()

player: Entity
world_entity: Entity

loaded = False


def load():
    global world_entity, player, loaded
    world_entity = world.init()
    # world_entity = world.world_entity

    player = Player.init()
    # player = Player.player
    time.sleep(7)

    loaded = True


thread.start_new_thread(load, args='')

if not loaded:
    camera.overlay.color = color.white
    camera.overlay.scale = 2.7
    camera.overlay.texture = 'perlin_noise'

    camera.overlay.shader = noise_fog_shader

    camera.overlay.t = 0

    camera.overlay.set_shader_input('time', 0)
    camera.overlay.set_shader_input('dark_color', color.red)
    camera.overlay.set_shader_input('light_color', color.green)

while not loaded:
    print('loading...')

    camera.overlay.t += time.dt
    camera.overlay.set_shader_input('time', camera.overlay.t)

    camera.overlay.set_shader_input('dark_color', lerp(color.red, color.black, camera.overlay.t / 4))
    camera.overlay.set_shader_input('light_color', lerp(color.green, color.cyan, camera.overlay.t / 2))
    app.step()

camera.overlay.color = color.clear
camera.overlay.enabled = False

world_entity.enabled = True

player.enabled = True
player.y = terraincast(player.world_position, world_entity) + 3
player.air_time = -0.05

app.step()


target.can_summon = True
target.t2 = target.t3 = target.t4 = target.t5 = 0.1
target.t1 = 0.5

def get_circ_coordinates(center: Vec3, radius=76):

    theta = 2 * math.pi * random.random()

    x = math.cos(theta) * radius + center.x
    y = math.sin(theta) * radius + center.z

    return x, 0, y

def update():
    if int(window.fps_counter.text) > 40:
        window.fps_counter.color = color.green
        window.fps_counter.scale = 2

    elif int(window.fps_counter.text) > 30:
        window.fps_counter.color = color.yellow
        window.fps_counter.scale = 2.5

    elif int(window.fps_counter.text) > 15:
        window.fps_counter.color = color.orange
        window.fps_counter.scale = 2.7
    else:
        window.fps_counter.color = color.red
        window.fps_counter.scale = 3



    if target.can_summon:
        target.can_summon = False
        invoke(setattr, target, 'can_summon', True, delay=5)  # ************ Increase it to 5

        if target.t1 < 0.8:
            target.t1 += 0.01
        elif target.t2 < 0.8:
            target.t2 += 0.01
        elif target.t3 < 0.8:
            target.t3 += 0.01
        elif target.t4 < 0.8:
            target.t4 += 0.01
        elif target.t5 < 0.8:
            target.t5 += 0.01


        print('probablity: ', target.t1, target.t2, target.t3, target.t4, target.t5)


        if random.random() < target.t4:
            mobs.Graster(player=player, parent=target, position=get_circ_coordinates(center=player.position))

        elif random.random() < target.t3:
            mobs.Karate(player=player, parent=target, position=get_circ_coordinates(center=player.position))

        elif random.random() < target.t2:
            mobs.Frank(player=player, parent=target, position=get_circ_coordinates(center=player.position))

        elif random.random() < target.t1:
            mobs.Graper(player=player, parent=target, position=get_circ_coordinates(center=player.position))
            print('su')




'''
for i in range(2, 3):
    for o in range(2, 3):
        mob = mobs.Graper(player=player, parent=target, x=i * random.uniform(10, 5), z=o * random.uniform(10, 15))
        mobs.Frank(player=player, parent=target, x=i * random.uniform(10, 5), z=o * random.uniform(10, 15))
        mobs.Karate(player=player, parent=target, x=i * random.uniform(10, 5), z=o * random.uniform(10, 15))
        mobs.Graster(player=player, parent=target, x=i * random.uniform(10, 5), z=o * random.uniform(10, 15))
'''
tp_lis = []
for i in range(-3, 3):
    for o in range(-3, 3):
        a = world.Teleport(x=i * 85, z=o * 85)
        tp_lis.append(a)

random.shuffle(tp_lis)

for i in range(len(tp_lis)):
    try:
        tp_lis[i].set(tp_lis[i - 1])
    except:
        pass

MemoryCounter()


# mouse.traverse_target = target


def input(key):
    if key == 'f2':
        app.screenshot(namePrefix='.\\screenshots\\screenshot')

    elif key == Keys.left_alt:
        application.quit()


app.run()
