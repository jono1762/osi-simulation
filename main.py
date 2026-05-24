from devices import DEVICES
from protocol import Data, TransportLayer
import sys

def transmit(value):
    data = Data(value)

    TransportLayer.run(DEVICES["Host A"], data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid input.")
    
    else:
        transmit(int(sys.argv[1]))