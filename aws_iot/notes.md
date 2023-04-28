# Notes on this codebase project 

Also note that I've quickly moved a good few files into the `old` folder, so they might not work immediately with imports.


- `IOTClient.py`
  - This file defines the IOTClient class
    - Initliazation and connection to AWS IOT
    - Methods for connecting, disconnecting, subscribing and publishing
    - There are also methods for handling `_on_conn_interrupted()` and `_on_conn_resumed()` events. However, these are 
      not yet implemented.


- `IOTContext.py`
  - This file defines the IOTContext class and also the IOTCredetials `@dataclass`
    - Used in initialization of IOTClient
      - I'm not entirely sure of the purpose (of the context class), however can Google it when the time comes. 

- `IOTDiscovery.py`
  - This file defines the IOTDiscovery class
    - Not 100% sure but this class seems to be used to find our AWS IOT devices (i.e. the Jetsons) on the network.
      And then initialized our IOTClient on each of the devices, connecting it (or letting us know if it wasn't able
      to connect).
    - It also seems that this class/ file is _specifically for finding aws greengrass devices_.

- `test.py`
  - This file tests publishing messages to an MQTT topic 

- `test_gg.py`
  - This files tests discovering AWS Greengrass devices on the network and then connecting to them, and then publishing
    messages to an MQTT topic. 
  