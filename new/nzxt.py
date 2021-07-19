

from nzxt_hueplus import NZXTHuePlus
from light import Color

class NZXTController:
    def init(self, config, add_device):
        self.config = config
        
        for device in config['devices']:
            dev = None
            if device['id'] == 'hue_plus':
                dev = NZXTHuePlus(device['leds'])
            if dev == None:
                raise 'Unimplemented device type: {}'.format(device['id'])
            else:
                dev.name = device['name']
                add_device(dev)


