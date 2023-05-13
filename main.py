from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import time

speed=1
dx=0
alive = True
enemies = []
shrink=2
app=Ursina()

size=12
player=PlatformerController2d(y=0, z=.01, scale=(1,1), color=color.green)
ground=Entity(model='quad', y=-2, scale_x=10, collider="box", color=color.yellow)
wall=Entity(model='quad', x=5.5, scale=(1,5), collider="box", color=color.blue)
platform1=Entity(model='quad', x=1, y=0, scale=(3,1), collider="box", color=color.violet)
platform2=Entity(model='quad', x=4, y=2, scale=(3,1), collider="box", color=color.violet)

camera.add_script(SmoothFollow(target=player, offset=[0, 1, -30], speed=4))

class Enemy(Entity):
    def __init__(self, x, y, model, color):
        super().__init__()
        self.model = model
        self.color=color
        self.collider = "box"
        self.x=x
        self.y=y

block_enemy = Enemy(3,3,'quad', color.black)
enemies.append(block_enemy)
sphere_enemy = Enemy(1,1,'sphere', color.pink)
enemies.append(sphere_enemy)

# enemies.append()
# duplicate(block_enemy, x=1,y=1,model='quad')

class Health_Bar(Entity):
    def __init__(self, y, z, r, g, b):
        super().__init__()
        self.model="quad"
        self.scale=(10, .5)
        self.color=color.rgb(r,g,b)
        self.y=y
        self.z=z
        self.origin=(-.5, -.5)

full_bar=Health_Bar(4, 0, 255, 0, 0)
green_bar=Health_Bar(4, -.01, 0, 255, 0)

def update():
    global speed,dx,alive
    
    full_bar.x=camera.x - size//2
    green_bar.x=full_bar.x
    full_bar.y=camera.y + 5
    green_bar.y=full_bar.y

    dx += speed * time.dt
    if alive :
        if abs(dx) > 2:
            speed *= -1
            dx = 0
        for enemy in enemies:
            enemy.x += speed*time.dt
            # if abs(player.x-enemy.x) < 1 and abs(player.y-enemy.y) < 1:
            #     enemy.color = color.lime
            if player.intersects(enemy).hit:
                player.color = color.red
                #green_bar.scale_x=0
                green_bar.scale_x-=shrink*time.dt
            else:
                player.color=color.green
            if player.y < -3:
                green_bar.scale_x=0
            if green_bar.scale_x<.1:
                    print("player die")
                    alive=False
                    player.disable()

def input(key):
    global alive
    if key == 'r':
        if player.enabled == False:
            player.enable()
            alive = True
            print(alive)
            green_bar.scale_x=10
            player.y=1
            player.x=0

app.run()