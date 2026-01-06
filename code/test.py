from genie.testbed import load
import sys

testbed = load('testbed.yaml')
device = testbed.devices["Router1"]
device.connect(learn_hostname = True)

test = device.execute("ping 192.168.178.202")

if "!!" in test:
    print("Ping successful")
else:
    print("Ping unsuccessful")
    sys.exit()
