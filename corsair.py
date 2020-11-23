from cuesdk import CueSdk
import threading
import queue
import time


def read_keys(inputQueue):
    while (True):
        input_str = input()
        inputQueue.put(input_str)


def get_available_leds():
    leds = list()
    device_count = corsair_sdk.get_device_count()
    for device_index in range(device_count):
        led_positions = corsair_sdk.get_led_positions_by_device_index(device_index)
        # for x in led_positions:
        #     zz = (list(map(lambda x: x.id, corsair_sdk.get_devices())))
        #     print(corsair_sdk.get_led_colors_by_device_index(device_index, range(600,612)))
        leds.append(led_positions)
    return leds


def set_color_corsair(r, g, b):
    cnt = len(corsair_all_leds)
    for di in range(cnt):
        device_leds = corsair_all_leds[di]
        for led in device_leds:
            device_leds[led] = (r, g, b)  
        corsair_sdk.set_led_colors_buffer_by_device_index(di, device_leds)
        corsair_sdk.set_led_colors_flush_buffer()

def init():
    global corsair_sdk
    corsair_sdk = CueSdk()
    connected = corsair_sdk.connect()
    corsair_sdk.request_control()
    if not connected:
        err = corsair_sdk.get_last_error()
        print("Handshake failed: %s" % err)
        return

    global corsair_all_leds
    corsair_all_leds = get_available_leds()
