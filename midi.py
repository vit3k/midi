from device_manager import DeviceManager
import time
import yaml
import argparse
import udev

parser = argparse.ArgumentParser(description='Midi bridge')
parser.add_argument('-c', '--config', default='config.yml', help='Path to config file')

args = parser.parse_args()

print('Starting midi bridge with config file {}'.format(args.config))

with open(args.config) as config_file:
  config = yaml.load(config_file)
  print('Using config: {}'.format(config))

device_manager = DeviceManager(config)
print('Initializing devices...')
udev = udev.Udev(device_manager)
udev_supported = udev.initialize()
device_manager.on_device_changed()

print('Bridge initialized. Listening for midi...')

try:
  if udev_supported:
    udev.loop()
  else:
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
