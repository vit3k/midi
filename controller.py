import mido
from midi_device import MidiDevice

#def test(msg):
#  print(msg)

class Controller(MidiDevice):
  def __init__(self, input_name, device_manager):
    print('controller const')
    self.input = mido.open_input(self.get_port(mido.get_input_names(), input_name))
    self.device_manager = device_manager
    print('before lamba')
    self.input.callback = lambda msg: self.handle(msg)
    print('after lambda')

  def handle(self, msg):
    print(msg)
    for device in self.device_manager.outputs:
      if msg.type == 'program_change':
        self.device_manager.outputs[device].change_patch(msg.program)

  def close(self):
    self.input.close()