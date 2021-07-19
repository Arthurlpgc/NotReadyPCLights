from enum import Enum
import colorsys


class Color:
    def __init__(self, r, g, b):
        self.R = int(r)
        self.G = int(g)
        self.B = int(b)

    def from_hsv(h, s, v):
        rgb = colorsys.hsv_to_rgb((h % 360) / 360, s / 100, v / 100)
        return Color(rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

    def to_hex(self, include_hashtag = True):
        def to_hex(c):
            ret = hex(c)
            ret = ret.replace('x', '')
            return ret[-2:]
        ret = to_hex(self.R) + to_hex(self.G) + to_hex(self.B)
        if include_hashtag:
            return f'#{ret}'
        else:
            return ret

    def toBGRInt(self):
        return self.B * 0x10000 + self.G * 0x100 + self.R


class LightType(Enum):
    UNKNOWN = 1
    RAZER = 2


class Light:
    def __init__(light_type: LightType, num_zones: int):
        self.light_type = light_type
        self.num_zones = num_zones
