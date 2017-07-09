import mido
from controller import Controller

class ZoomG3Controller(Controller):
  def __init__(self, input_name, output_name, device_manager, callbacks):
    super(ZoomG3Controller, self).__init__(input_name, device_manager, callbacks)
    self.output = mido.open_output(self.get_port(mido.get_output_names(),  output_name))
    print('zoom opened output')
    temp_callback = self.input.callback
    self.input.callback = None
    self.output.send(mido.Message('sysex', data=[0x7E, 0x00, 0x06, 0x01]))
    print('message sent')
    id_message = self.input.receive()
    print(id_message)
    self.device_id = id_message.data[1]
    self.manufacturer_id = id_message.data[4]
    self.model_number = id_message.data[5]
    self.input.callback = temp_callback
    self.send_command(0x50)
    self.send_command(0x33)
    self.output.close()
    print('zoom initialized')

  def send_command(self, command):
    self.output.send(mido.Message('sysex', data=[self.manufacturer_id, self.device_id, self.model_number, command]))

  @staticmethod
  def get_type():
    return 'zoomg3'