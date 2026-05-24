from devices import DEVICES
from protocol import Data, TransportLayer
import sys

def transmit(value):
    '''
    Function that inputs the application message size from the terminal then passes it 
    into the transport layer of host A to simulate sending the message from host A to B.
    '''
    data = Data(value)

    TransportLayer.run(DEVICES["Host A"], data) 

if __name__ == "__main__":
    '''
    Code below run when main.py run directly (intended as entry-point to project)
    '''
    if len(sys.argv) != 2: # Ensures single argument passed in
        print("Must provide one argument when running this script.")
    
    elif int(sys.argv[1]) <= 0: # Ensures the argument is a positive integer
        print("Argument provided must be a positive integer.")
    
    else: # Calls function to transmit the data of a specified size
        transmit(int(sys.argv[1]))