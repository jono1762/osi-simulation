from config import name_to_ip, ROUTING_TABLE

# Application Layer

class Data:
    def __init__(self, value=None):
        self.value = value
        self.type = "DATA" if value is not None else "ACK"

# Data Link Layer

class Frame:
<<<<<<< HEAD
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
 
=======
    pass

class DataLinkLayer:
    pass

# Network Layer
>>>>>>> b195b71bd710017543b05c96a8c0e0f99139e4e3

class Packet:
<<<<<<< HEAD
    def init(self, src_hostname, dest_hostname, payload):
=======
    def __init__(self, payload, src_hostname, dest_hostname):
>>>>>>> b195b71bd710017543b05c96a8c0e0f99139e4e3
        self.src_ip = name_to_ip[src_hostname]
        self.dest_ip = name_to_ip[dest_hostname]
        self.ttl = 100
        self.protocol = 17
        self.length = payload + (4 + 4 + 1 + 1 + 2)
        self.payload = payload

<<<<<<< HEAD
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
=======
class NetworkLayer:
    name = "Layer 3"

    @staticmethod
    def run(device, data):
        if type(data) == Segment:
            packet = NetworkLayer.encapsulate(data, device, "Host A" if device != "Host A" else "Host B")
            print(f"{device}: {NetworkLayer.name}: Segment received from Transport Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dest_ip}, TTL={packet.ttl}")
            print(f"{device}: {NetworkLayer.name}: Destination IP read: {packet.dest_ip}")
            next_hop_ip = NetworkLayer.forward(device)
            print(f"{device}: {NetworkLayer.name}: Routing table lookup performed")
            print(f"{device}: {NetworkLayer.name}: Next-hop IP determined: {next_hop_ip}")
            print(f"{device}: {NetworkLayer.name}: Outgoing interface selected.")
            print(f"{device}: {NetworkLayer.name}: Packet Forwarded to Data Link Layer")
        
        elif type(data) == Frame:
            packet = data.payload
            print(f"{device}: {NetworkLayer.name}: Segment received from Transport Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dest_ip}, TTL={packet.ttl}")
            print(f"{device}: {NetworkLayer.name}: Destination IP read: {packet.dest_ip}")
            if name_to_ip[device] == packet.dest_ip:
                print(f"{device}: {NetworkLayer.name}: Packet identified as local delivery")
                print(f"{device}: {NetworkLayer.name}: Segment delivered to Transport Layer")
            else:
                NetworkLayer.ttl_handling(packet)
                print(f"{device}: {NetworkLayer.name}: TTL decremented: {packet.ttl + 1} → {packet.ttl}")
                next_hop_ip = NetworkLayer.forward(device)
                print(f"{device}: {NetworkLayer.name}: Routing table lookup performed")
                print(f"{device}: {NetworkLayer.name}: Next-hop IP determined: {next_hop_ip}")
                print(f"{device}: {NetworkLayer.name}: Outgoing interface selected.")
                print(f"{device}: {NetworkLayer.name}: Packet Forwarded to Data Link Layer")

    @staticmethod
    def encapsulate(segment, src_hostname, dest_hostname):
        return Packet(segment, src_hostname, dest_hostname)

    @staticmethod
    def forward(device):
        return ROUTING_TABLE[name_to_ip[device]]["Outgoing Link"]

    @staticmethod
    def ttl_handling(packet):
        packet.ttl -= 1

        if packet.ttl == 0:
            del packet

# Transport Layer

class Segment:
    pass

class TransportLayer:
    pass
>>>>>>> b195b71bd710017543b05c96a8c0e0f99139e4e3
