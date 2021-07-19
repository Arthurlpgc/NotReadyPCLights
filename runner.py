from corsair import init, set_color_corsair
from nzxt import set_color_nzxt
from razer import init_razer, set_color_razer, heartbeat_thread
import threading, time
from flask import Flask, request
from debounce import debounce


def from_hsv(hsv):
    [h, s, v] = hsv
    c = v * s
    x = c * (1 - abs((h/60) % 2 - 1))
    m = v - c
    rgb = [0, 0, 0]
    if h >= 0 and h < 60:
        rgb = [c, x, 0]
    if h >= 60 and h < 120:
        rgb = [x, c, 0]
    if h >= 120 and h < 180:
        rgb = [0, c, x]
    if h >= 180 and h < 240:
        rgb = [0, x, c]
    if h >= 240 and h < 300:
        rgb = [x, 0, c]
    if h >= 300 and h <360:
        rgb = [c, 0, x]
    rgb = list(map(lambda z: int((z + m) * 255), rgb))
    return rgb
init()
init_razer()
current_hsv = [270, 1, 1]

@debounce(2)
def set_colors_hsv():
    current_colors = from_hsv(current_hsv)
    set_color_corsair(current_colors[0], current_colors[1], current_colors[2])
    set_color_razer(current_colors[0], current_colors[1], current_colors[2])
    set_color_nzxt(current_colors[0], current_colors[1], current_colors[2])
    set_color_corsair(current_colors[0], current_colors[1], current_colors[2])
    set_color_razer(current_colors[0], current_colors[1], current_colors[2])
    set_color_nzxt(current_colors[0], current_colors[1], current_colors[2])

set_colors_hsv()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/set', methods=['POST'])
def set_colors_route():
    print(request.json)
    r = request.json['r']
    g = request.json['g']
    b = request.json['b']
    set_color_corsair(r, g, b)
    set_color_razer(r, g, b)
    return "ok"


@app.route('/hb/on', methods=['GET'])
def hb_on_route():
    if current_hsv[2] == 0:
        current_hsv[2] = 1
        set_colors_hsv()
    return "ok"

@app.route('/hb/off', methods=['GET'])
def hb_off_route():    
    current_hsv[2] = 0    
    set_colors_hsv()
    return "ok"

@app.route('/hb/status', methods=['GET'])
def hb_status_route():
    if current_hsv[2] > 0:
        return "1"
    else: 
        return "0"

@app.route('/hb/saturation/set/<saturation>', methods=['GET'])
def hb_saturation_set_route(saturation):
    current_hsv[1] = float(saturation) / 100
    set_colors_hsv()
    return "ok"

@app.route('/hb/saturation/status', methods=['GET'])
def hb_saturation_status_route():
    return str(current_hsv[1] * 100)

@app.route('/hb/brightness/set/<brightness>', methods=['GET'])
def hb_brightness_set_route(brightness):
    current_hsv[2] = float(brightness) / 100
    set_colors_hsv()
    return "ok"

@app.route('/hb/brightness/status', methods=['GET'])
def hb_brightness_status_route():
    return str(current_hsv[2] * 100)

@app.route('/hb/hue/set/<hue>', methods=['GET'])
def hb_hue_set_route(hue):
    current_hsv[0] = float(hue)
    set_colors_hsv()
    return "ok"

@app.route('/hb/hue/status', methods=['GET'])
def hb_hue_status_route():
    return str(current_hsv[0])

app.run(host='0.0.0.0', port=80)