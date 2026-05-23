from devices import create_devices
from protocol import Data, DataLinkLayer, NetworkLayer, TransportLayer
import sys

def transmit(value):
    host_A, host_B, router = create_devices()
    data = Data(value)

    TransportLayer.run(host_A, data)
    NetworkLayer.run(host_A, data)
    DataLinkLayer.run(host_A, data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid input.")
    
    else:
        transmit(sys.argv[1])