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