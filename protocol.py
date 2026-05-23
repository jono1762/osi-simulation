#Layer 2: Data Link Layer (Ethernet-like Frame)
#❖ Destination MAC (6 bytes) → e.g., BB:BB:BB:BB:BB:BB
#❖ Source MAC (6 bytes) → e.g., AA:AA:AA:AA:AA:AA
#❖ Type (2 bytes) → 0x0800 (indicates IPv4 payload)
#❖ Payload (variable) → contains the Layer 3 (IP) packet
class Frame:
    def init(self, src_mac, dest_mac, packet):
        self.dest_mac = dest_mac
        self.source_mac = src_mac
        self.type = 2
        self.payload = packet

def encapsulate(packet, dest):
    #lookup mac address
    

    #contruct frame
    frame = Frame(src_mac, dest, packet)

def MAC Address

def switches/interfaces

def local forwarding
 

# Layer 3: Header (IP-like Packet)
#❖ Source IP (4 bytes) → e.g., 10.0.1.10
#❖ Destination IP (4 bytes) → e.g., 10.0.2.20
#❖ TTL (1 byte) → 100 (decremented at each router)
#❖ Protocol (1 byte) → 17 (indicates UDP payload)
#❖ Total Length (2 bytes) → e.g., 40 (header + payload size)
#❖ Payload (variable) → contains the Layer 4 (UDP segment)
class Packet:
    def init(self, src_hostname, dest_hostname, payload):
        self.src_ip = name_to_ip[src_hostname]
        self.dest_ip = name_to_ip[dest_hostname]
        self.ttl = 100
        self.protocol = 17
        self.length = payload + (4 + 4 + 1 + 1 + 2)
        self.payload = payload

class Segment:
# Layer 4: Header (UDP-like Segment with ACK support)
#❖ Source Port (2 bytes) → e.g., 5000
#❖ Destination Port (2 bytes) → e.g., 80
#❖ Length (2 bytes) → e.g., 100 (header + data)
#❖ Checksum (2 bytes) → e.g., computed value for error detection
#❖ Type (1 byte) → 0 = DATA, 1 = ACK
#❖ Sequence Number (1 byte) → e.g., 0 or 1
#❖ Data (variable) → contains the application message (empty for ACK)
     def __init__(self, payload):
        self.source_port = 
        self.destination_port = 
        self.length
        self.checksum = 
        self.sequence_number
        self.type
        self.data

#Transport Layer Functions
def 

def

def
