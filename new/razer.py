from razer_connect import RazerConnect
from razer_mouse import RazerMouse
from razer_mousepad import RazerMousepad
import requests
import time
import threading
import urllib3
from light import Color
from razer_keyboard import RazerKeyboard

razer_device_types = [
    "keyboard",
    "mouse",
    "headset",
    "mousepad",
    "keypad",
    "chromalink"
]

razer_init_request = {
    "title": "CuRazor",
    "description": "Unifying light",
    "author": {
        "name": "arthur costa",
                "contact": "arthurlpgcosta@gmail.com"
    },
    "device_supported": razer_device_types,
    "category": "application"
}


class RazerController:
    chromasdk_uri = None

    def heartbeat(self):
        if self.chromasdk_uri != None:
            requests.put(
                "{}/heartbeat".format(self.chromasdk_uri), verify=False)

    def run_thread(self):
        while True:
            self.heartbeat()
            time.sleep(3)

    def init(self, config, add_device):
        self.config = config
        urllib3.disable_warnings()
        requests.get(
            "https://chromasdk.io:54236/razer/chromasdk", verify=False)
        ans = requests.post("https://chromasdk.io:54236/razer/chromasdk",
                            verify=False, json=razer_init_request)
        self.chromasdk_uri = ans.json()['uri']
        self.heartbeat()
        time.sleep(1)
        heartbeat_thread = threading.Thread(
            target=self.run_thread, args=(), daemon=True)
        heartbeat_thread.start()
        for device in config['devices']:
            dev = None
            if device['id'] == 'keyboard':
                dev = RazerKeyboard(self.chromasdk_uri)
            if device['id'] == 'connect':
                dev = RazerConnect(self.chromasdk_uri)
            if device['id'] == 'mouse':
                dev = RazerMouse(self.chromasdk_uri)
            if device['id'] == 'mousepad':
                dev = RazerMousepad(self.chromasdk_uri)
            if dev == None:
                raise 'Unimplemented device type: {}'.format(device['id'])
            else:
                dev.name = device['name']
                add_device(dev)


