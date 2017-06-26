import time
import mido

class MidiDevice:
  def get_port(self, ports, name):
    return next(iter([x for x in ports if x.startswith(name)] or []), None)

class OutputDevice(MidiDevice):
  def get_mapping(self, program):
    if program in self.mapping:
      return self.mapping[program]
    return program % self.max_patches

  def __init__(self, output_name, mapping, max_patches):
    self.output = mido.open_output(self.get_port(mido.get_output_names(), output_name))
    self.mapping = mapping
    self.max_patches = max_patches

  def change_patch(self, number):
    program = self.get_mapping(number)
    print('Changing program to {}'.format(program))
    program_change = mido.Message('program_change', program=program)
    self.output.send(program_change)    

class Controller(MidiDevice):
  def __init__(self, input_name, output_devices):
    self.input = mido.open_input(self.get_port(mido.get_input_names(), input_name))
    self.output_devices = output_devices

  def handle(self):
    for msg in self.input.iter_pending():
      if msg.type == 'program_change':
        pass

  def pass_to_listeners(self, msg):
    for device in self.output_devices:
      if msg.type == 'program_change':
        device.change_patch(msg.program)
    
class ZoomG3Controller(Controller):
  def __init__(self, output_devices):
    super(ZoomG3Controller, self).__init__('ZOOM G Series', output_devices)
    self.output = mido.open_output(self.get_port(mido.get_output_names(), 'ZOOM G Series'))
    self.output.send(mido.Message('sysex', data=[0x7E, 0x00, 0x06, 0x01]))
    id_message = self.input.receive()
    self.device_id = id_message.data[1]
    self.manufacturer_id = id_message.data[4]
    self.model_number = id_message.data[5]
    self.send_command(0x50)
    self.send_command(0x33)

  def send_command(self, command):
    self.output.send(mido.Message('sysex', data=[self.manufacturer_id, self.device_id, self.model_number, command]))

  def handle(self):
    for msg in self.input.iter_pending():
      if msg.type == 'program_change':
        self.pass_to_listeners(msg)
      elif msg.type == 'sysex':
        #some cool stuff
        pass

katana_map = {
  0: 0,
  1: 0,
  2: 3,
  3: 4,
  4: 2
}

katana = OutputDevice('KATANA', katana_map, 5)
zoom = ZoomG3Controller([katana])

print('Listening...')
while True:
  zoom.handle()
  time.sleep(0.01)