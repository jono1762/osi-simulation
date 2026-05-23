from config import name_to_ip, ROUTING_TABLE
import struct

# Application Layer

class Data:
    def __init__(self, value=None):
        self.value = value
        self.type = "DATA" if value is not None else "ACK"

# Data Link Layer

class Frame:
    pass

class DataLinkLayer:
    pass

# Network Layer

class Packet:
    def __init__(self, payload, src_hostname, dest_hostname):
        self.src_ip = name_to_ip[src_hostname]
        self.dest_ip = name_to_ip[dest_hostname]
        self.ttl = struct.pack('B', 100)
        self.protocol = struct.pack('B', 17)
        self.length = struct.pack('S', 4 + 4 + 1 + 1 + 2 + payload.length)
        self.payload = payload

class NetworkLayer:
    name = "Layer 3"

    @staticmethod
    def run(device, data):
        if type(data) == Segment:
            packet = NetworkLayer.encapsulate(data, device, "Host A" if device != "Host A" else "Host B")
            src_ip, dest_ip = NetworkLayer.get_string_rep_ip(packet.src_ip), NetworkLayer.get_string_rep_ip(packet.dest_ip)
            print(f"{device}: {NetworkLayer.name}: Segment received from Transport Layer: SRC_IP={src_ip}, DST_IP={dest_ip}, TTL={struct.unpack('B', packet.ttl)}")
            print(f"{device}: {NetworkLayer.name}: Destination IP read: {dest_ip}")
            next_hop_ip = NetworkLayer.get_string_rep_ip(NetworkLayer.forward(device))
            print(f"{device}: {NetworkLayer.name}: Routing table lookup performed")
            print(f"{device}: {NetworkLayer.name}: Next-hop IP determined: {next_hop_ip}")
            print(f"{device}: {NetworkLayer.name}: Outgoing interface selected.")
            print(f"{device}: {NetworkLayer.name}: Packet Forwarded to Data Link Layer")
        
        elif type(data) == Frame:
            packet = data.payload
            src_ip, dest_ip = NetworkLayer.get_string_rep_ip(packet.src_ip), NetworkLayer.get_string_rep_ip(packet.dest_ip)
            print(f"{device}: {NetworkLayer.name}: Segment received from Transport Layer: SRC_IP={src_ip}, DST_IP={dest_ip}, TTL={struct.unpack('B', packet.ttl)}")
            print(f"{device}: {NetworkLayer.name}: Destination IP read: {dest_ip}")
            if name_to_ip[device] == packet.dest_ip:
                print(f"{device}: {NetworkLayer.name}: Packet identified as local delivery")
                print(f"{device}: {NetworkLayer.name}: Segment delivered to Transport Layer")
            else:
                NetworkLayer.ttl_handling(packet)
                print(f"{device}: {NetworkLayer.name}: TTL decremented: {struct.unpack('B', packet.ttl) + 1} → {struct.unpack('B', packet.ttl)}")
                next_hop_ip = NetworkLayer.forward(device)
                print(f"{device}: {NetworkLayer.name}: Routing table lookup performed")
                print(f"{device}: {NetworkLayer.name}: Next-hop IP determined: {next_hop_ip}")
                print(f"{device}: {NetworkLayer.name}: Outgoing interface selected.")
                print(f"{device}: {NetworkLayer.name}: Packet Forwarded to Data Link Layer")
    
    @staticmethod
    def get_string_rep_ip(ip_addr):
        return '.'.join(list(map(lambda x: str(x), struct.unpack("4H", ip_addr))))

    @staticmethod
    def encapsulate(segment, src_hostname, dest_hostname):
        return Packet(segment, src_hostname, dest_hostname)

    @staticmethod
    def forward(device):
        return ROUTING_TABLE[name_to_ip[device]]["Outgoing Link"]

    @staticmethod
    def ttl_handling(packet):
        ttl = struct.unpack('B', packet.ttl)
        ttl -= 1

        if ttl == 0:
            del packet
        else:
            packet.ttl = struct.pack('B', ttl)

# Transport Layer

class Segment:
    pass

class TransportLayer:
    pass
