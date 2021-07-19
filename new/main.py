from nzxt import NZXTController
from razer import RazerController
from light import Color, Light
from time import sleep
import random
import json
config_file = open('config.json')
config = json.loads(config_file.read())
devices = []


def add_device(device: Light):
    global devices
    devices.append(device)


rzctrl = RazerController()
rzctrl.init(config['razer'], add_device)
nzctrl = NZXTController()
nzctrl.init(config['nzxt'], add_device)

for dev_i in range(len(devices)):
    for dev_j in range(devices[dev_i].num_zones):
       devices[dev_i].set_color(Color.from_hsv(random.randrange(0, 360),100,100), dev_j)
    devices[dev_i].update()



print(rzctrl.chromasdk_uri)
sleep(60)
