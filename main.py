from devices import DEVICES
from protocol import Data, TransportLayer
import sys

data_left = None

def transmit(value):
    data = Data(value)

    TransportLayer.run(DEVICES["Host A"], data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of arguments provided - provide exactly one positive integer value when running this script.")
    
    elif int(sys.argv[1]) <= 0:
        print("Integer value argument must be a positive number.")
    
    else:
        transmit(int(sys.argv[1]))