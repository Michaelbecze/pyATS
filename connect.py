from genie.testbed import load

testbed = load('testbed.yml')
device = testbed.devices['R1']          # pull device from testbed

device.connect(log_stdout=False)         # quiet; drop the kwarg to watch the session
print('connected:', device.is_connected())

print(device.execute('show version | include uptime'))

device.disconnect()