import requests
from light import Light, Color

razer_border_works = 0
mx = 22 + 2 * razer_border_works
class RazerMousepad(Light):
    def __init__(self, chromasdk_uri):
        self.chromasdk_uri = chromasdk_uri
        self.num_zones = 15
        self.colors = [0] * 15
        self.name = "Razer Mousepad"

    def update(self):
        request = {
            "effect": "CHROMA_CUSTOM",
            "param": self.colors
        }
        response = requests.put(
            "{}/mousepad".format(self.chromasdk_uri), verify=False, json=request)
        print(response.json())

    def set_color(self, color: Color, zone: int):
        self.colors[zone] = color.toBGRInt()
