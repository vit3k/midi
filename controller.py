import mido
from midi_device import MidiDevice

class Controller(MidiDevice):
  def __init__(self, input_name):
    self.input = mido.open_input(self.get_port(mido.get_input_names(), input_name))

  def handle(self, output_devices):
    for msg in self.input.iter_pending():
      self.pass_to_listeners(msg, output_devices)

  def pass_to_listeners(self, msg, output_devices):
    for device in output_devices:
      if msg.type == 'program_change':
        device.change_patch(msg.program)