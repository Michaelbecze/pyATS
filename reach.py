import json
from genie.testbed import load
from dotenv import load_dotenv

load_dotenv() 
testbed = load('testbed.yml')

for device in testbed:
  device.connect(log_stdout=False)         
  print('connected:', device.is_connected())
  
  version = device.parse('show version')
  brief = device.parse('show ip interface brief')

  print(f'-------------{device}-------------------')
  print(version.q.get_values('uptime'))
  print(json.dumps(brief["interface"]["Loopback0"], indent=2))
device.disconnect()