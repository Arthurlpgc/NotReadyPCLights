import os
from light import Light, Color

command_template = ".\\liquidctl.exe --match NZXT set led1 color super-fixed"
razer_border_works = 0
mx = 22 + 2 * razer_border_works
class NZXTHuePlus(Light):
    def __init__(self, num_zones):
        self.num_zones = num_zones
        self.colors = []
        for i in range(num_zones):
            self.colors.append(Color(0,0,0))
        self.name = "NZXT Hue Plus"

    def update(self):
        command = command_template
        for color in self.colors:
            command += f' {color.to_hex(include_hashtag=False)}'
        os.system(command)

    def set_color(self, color: Color, zone: int):
        self.colors[zone] = color
