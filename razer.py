import requests, time, threading
import urllib3
razer_uri = None
device_types = [
            "keyboard",
            "mouse",
            "headset",
            "mousepad",
            "keypad",
            "chromalink"
            ]


def heartbeat():
    requests.put("{}/heartbeat".format(razer_uri), verify=False)

def heartbeat_thread():
    while True: 
        heartbeat()
        print('heartbeat')
        time.sleep(5)

def init_razer():
    urllib3.disable_warnings()
    requests.get("https://chromasdk.io:54236/razer/chromasdk", verify=False)
    ans = requests.post("https://chromasdk.io:54236/razer/chromasdk", verify=False, json={
        "title": "Homekitty",
        "description": "Adding it to homekit",
        "author": {
            "name": "arthur costa",
            "contact": "https://github.com/RazerOfficial/HTML5ChromaSDK"
        },
        "device_supported": device_types,
        "category": "application"
    })
    global razer_uri
    razer_uri = ans.json()['uri']
    heartbeat()
    time.sleep(1)
    x = threading.Thread(target=heartbeat_thread, args=(), daemon=True)
    x.start()

def set_color_razer_device(device, r, g, b):
    requests.put("{}/{}".format(razer_uri, device), verify=False, json={
        "effect": "CHROMA_STATIC",
        "param": {
            "color": b * 0x10000 + g * 0x100 + r
        }
    }).json()

def set_color_razer(r, g, b):
    for device in device_types:
        set_color_razer_device(device, r, g, b)