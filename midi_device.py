class MidiDevice:
  def get_port(self, ports, name):
    return next(iter([x for x in ports if name in x] or []), None)