from device_manager import DeviceManager
import time
import yaml
import re
import sys
import argparse

parser = argparse.ArgumentParser(description='Midi bridge')
parser.add_argument('-c', '--config', default='config.yml', help='Path to config file')

args = parser.parse_args()

print('Starting midi bridge with config file {}'.format(args.config))

with open(args.config) as config_file:
  config = yaml.load(config_file)
  print('Using config:')
  print(config)

device_manager = DeviceManager(config)
print('Initializing devices...')
device_manager.on_device_changed()

try:
  import pyudev 
except Exception:
  print('No UDEV support.')

print('Bridge initialized. Listening for midi...')

try:
  try:
    udev_context = pyudev.Context()
    print('UDEV supported. Setup monitoring...')
    udev_monitor = pyudev.Monitor.from_netlink(udev_context)
    udev_monitor.filter_by('sound')
    reg = re.compile('midi[A-Za-z0-9]+')
    while True:
      device = udev_monitor.poll()
      
      if reg.match(device.sys_name):
        print('{}: {}'.format(device.action, device.sys_name))
        device_manager.on_device_changed()
  except NameError:
    while True:
      try:
        with open('/midi') as fifo:
          while True:
            print('Waiting for devices changes...')
            data = fifo.read()
            if len(data) == 0:
              break
            print('Updating devices...')
            device_manager.on_device_changed()
      except IOError:
        time.sleep(0.5)  
except KeyboardInterrupt:
  print('Shutting down...')
