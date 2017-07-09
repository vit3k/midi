from midi_device import MidiDevice
import mido

class OutputDevice(MidiDevice):
  def get_mapping(self, program):
    if program in self.mapping:
      return self.mapping[program]
    return program % self.max_patches

  def __init__(self, output_name, mapping, max_patches):
    self.output_name = self.get_port(mido.get_output_names(), output_name)
    self.output = mido.open_output(self.output_name)
    self.mapping = mapping
    self.max_patches = max_patches

  def change_patch(self, number):
    program = self.get_mapping(number)
    print('[{}] Changing program to {}'.format(self.output_name, program))
    program_change = mido.Message('program_change', program=program)
    self.output.send(program_change)    

  def close(self):
    self.output.close()