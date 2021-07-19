import requests
from light import Light, Color

razer_border_works = 0
mx = 22 + 2 * razer_border_works
class RazerMouse(Light):
    def __init__(self, chromasdk_uri):
        self.chromasdk_uri = chromasdk_uri
        self.num_zones = 1
        self.color = Color(0, 0, 0)
        self.name = "Razer Mouse"

    def update(self):
        request = {
            "effect": "CHROMA_STATIC",
            "param": {
                "color": self.color.toBGRInt()
            },
        }
        requests.put(
            "{}/mouse".format(self.chromasdk_uri), verify=False, json=request)

    def set_color(self, color: Color, zone: int):
        assert(zone == 0)
        self.color = color
