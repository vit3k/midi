import re
try:
  import pyudev 
except Exception:
  pass

class Udev:
  def __init__(self, device_manager):
    self.device_manager = device_manager

  def initialize(self):
    try:     
      self.udev_context = pyudev.Context()
      print('UDEV supported. Setup device monitoring...')
      self.udev_monitor = pyudev.Monitor.from_netlink(self.udev_context)
      self.udev_monitor.filter_by('sound')
      self.reg = re.compile('midi[A-Za-z0-9]+')
      return True

    except NameError:
      print('UDEV not supported')
      return False

  def poll(self):
    device = self.udev_monitor.poll()
    if self.reg.match(device.sys_name):
      print('{}: {}'.format(device.action, device.sys_name))
      self.device_manager.on_device_changed()

  def loop(self):
    while True:
      self.poll()
      