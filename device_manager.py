import mido
from output_device import OutputDevice
from controller import Controller
from zoom_g3_controller import ZoomG3Controller

class DeviceManager:
  def __init__(self, config):
    self.inputs = {}
    self.outputs = {}
    self.input_device_list = []
    self.output_device_list = []
    self.config = config

  def get_devconfig(self, device, config):
    return next(iter([x for x in config if x['device'] in device] or []), None)

  def process_outputs(self):
    print('Process outputs')
    new_output_device_list = mido.get_output_names()
    print(new_output_device_list)
    for device in new_output_device_list:
      if device not in self.output_device_list:
        dev_config = self.get_devconfig(device, self.config['outputs'])
        print(device)
        print(dev_config)
        if dev_config is not None and device not in self.outputs:
          self.outputs[device] = OutputDevice(device, dev_config['map'], dev_config['max_patches'])
          print('{} added as output'.format(device))

    for device in self.output_device_list:
      if device not in new_output_device_list and device in self.outputs:
        del self.outputs[device]
        print('{} removed from outputs'.format(device))

    self.output_device_list = new_output_device_list

  def controller_factory(self, device):
    if 'ZOOM G Series MIDI 1' in device:
      print('zoom')
      return ZoomG3Controller(self)
    else:
      return Controller(device, self)

  def process_inputs(self):
    print('Process inputs')
    new_input_device_list = mido.get_input_names()
    print(new_input_device_list)
    for device in new_input_device_list:
      if device not in self.input_device_list:
        dev_config = self.get_devconfig(device, self.config['inputs'])
        print(device)
        print(dev_config)
        if dev_config is not None and device not in self.inputs:
          self.inputs[device] = self.controller_factory(device)
          print('{} added as input'.format(device))

    for device in self.input_device_list:
      if device not in new_input_device_list and device in self.inputs:
        #self.intputs[device].close()
        del self.inputs[device]
        print('{} removed from inputs'.format(device))

    self.input_device_list = new_input_device_list

  def on_device_changed(self):
    print('Devices changed')
    self.process_outputs()
    self.process_inputs()
