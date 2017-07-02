import mido
from controller import Controller

class ZoomG3Controller(Controller):
  def __init__(self):
    super(ZoomG3Controller, self).__init__('ZOOM G Series')
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

  def handle(self, output_devices):
    for msg in self.input.iter_pending():
      if msg.type == 'program_change':
        self.pass_to_listeners(msg, output_devices)
      elif msg.type == 'sysex':
        #some  cool zoom stuff could be added
        pass