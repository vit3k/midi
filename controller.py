import mido
from midi_device import MidiDevice

class Controller(MidiDevice):
  def __init__(self, input_name, device_manager, callbacks):
    self.input_name = self.get_port(mido.get_input_names(), input_name)
    self.input = mido.open_input(self.input_name)
    self.device_manager = device_manager
    if callbacks:
      print('Setting up callbacks for input receive...')
      self.input.callback = lambda msg: self.handle(msg)
    
  def handle(self, msg):
    print('[{}] Received midi: {}'.format(self.input_name, msg))
    for device in self.device_manager.outputs:
      if msg.type == 'program_change':
        self.device_manager.outputs[device].change_patch(msg.program)

  def close(self):
    self.input.close()

  @staticmethod
  def get_type():
    return 'generic'