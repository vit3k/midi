import threading
import time

class MidiLooper(threading.Thread):
  def __init__(self, device_manager):
    threading.Thread.__init__(self)
    self.device_manager = device_manager

  def run(self):
    #config devices as on startup
    self.device_manager.on_device_changed()
    print('Listening for midi...')

    while True:
      #self.device_manager.handle_inputs()
      #time.sleep(0.1)
      pass