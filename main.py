<<<<<<< HEAD
#take an input from command line

'''
HostA(Package).runTransportLayer()
    alternative -> Host Device is argument to TransportLayer()
Transport Layer Down()
    #Recieve Data from Application Layer
    #Checksum
    #Encapsulation
    #Send to Network Layer
Network Layer Down()
    #Recieved
    #Read Desitination IP
    #Routing Table Lookup Performed
    #Hop Determined
    #Outgoing interface selected
Datalink()
    #MAC Address
    Lookup
    Frame Created 
    Frame Sent

Router()
Recieved ACK
Reverse when current ip doesn't match destination
'''

#
#
#
#
#
#
=======
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
>>>>>>> b195b71bd710017543b05c96a8c0e0f99139e4e3
