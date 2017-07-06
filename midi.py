from device_manager import DeviceManager
from midi_looper import MidiLooper
import time
#from flask import Flask

config = {
  'outputs': [
    {
      'device': 'KATANA MIDI 1',
      'max_patches': 5,
      'map': {
        0: 0,
        1: 0,
        2: 3,
        3: 4,
        4: 2
      }
    }
  ],
  'inputs': [
    {
      'device': 'ZOOM G Series MIDI 1'
    }
  ]
}

device_manager = DeviceManager(config)
midi_looper = MidiLooper(device_manager)

midi_looper.start()

#app = Flask(__name__)
#@app.route('/device_changed') 
#def device_changed(): 
#    device_manager.on_device_changed()

while True:
  with open('/midi') as fifo:
    while True:
      data = fifo.read()
      if len(data) == 0:
        break
      device_manager.on_device_changed()

#app.run(port=8181, host='0.0.0.0', debug=False, use_reloader=False)