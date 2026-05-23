from config import name_to_ip, name_to_mac, ip_to_network, ROUTING_TABLE, HOSTS, INTERFACES
from devices import DEVICES, Router
import struct

# Application Layer

class Data:
    def __init__(self, value=None):
        self.value = struct.pack('B', value)
        self.type = 0 if value is None else 1

# Data Link Layer

class Frame:
    def __init__(self, src_mac, dest_mac, packet):
        self.src_mac = src_mac
        self.dest_mac = dest_mac
        self.type = 2
        self.payload = packet

class DataLinkLayer:
    name = "Layer 2"

    def run(device, data, next_hop_ip=None):
        if type(data) == Frame: #receive frame from LAN
            print(f"{device.name}: {DataLinkLayer.name}: Frame received")
            if data.src_mac not in device.mac_table:
                device.mac_table[data.payload.src_ip] = data.src_mac
                print(f"{device.name}: {DataLinkLayer.name}: MAC Address Learned")
            print(f"{device.name}: {DataLinkLayer.name}: Packet Delivered to Network Layer\n")
            NetworkLayer.run(device, data)
        
        elif type(data) == Packet: #receive packet from network layer
            print(f"{device.name}: {DataLinkLayer.name}: Packet received from Network Layer")
            # Determine how to learn MAC address
            for name, ip in name_to_ip.items():
                if ip == next_hop_ip:
                    dest_name = name
                    dest_mac = name_to_mac[name]
                    break
            print(f"{device.name}: {DataLinkLayer.name}: MAC lookup for next-hop IP ({NetworkLayer.get_string_rep_ip(next_hop_ip)}) → {dest_mac}")
            if type(device) == Router:
                frame = DataLinkLayer.encapsulate(device.mac_address, dest_mac, data)
            else:
                frame = DataLinkLayer.encapsulate(device.mac_address, dest_mac, data)
            print(f"{device.name}: {DataLinkLayer.name}: Frame created: SRC_MAC={device.mac_address}, DST_MAC={dest_mac}")
            print(f"{device.name}: {DataLinkLayer.name}: Frame sent\n")
            if dest_name in HOSTS:
                DataLinkLayer.run(DEVICES[dest_name], frame)
            if dest_name in INTERFACES:
                DataLinkLayer.run(DEVICES["Router R1"], frame)

    def encapsulate(src_mac, dest_mac, packet):
        frame = Frame(src_mac, dest_mac, packet)
        return frame

class Packet:
    def __init__(self, payload, src_hostname, dest_hostname):
        self.src_ip = name_to_ip[src_hostname]
        self.dest_ip = name_to_ip[dest_hostname]
        self.ttl = struct.pack('B', 100)
        self.protocol = struct.pack('B', 17)
        self.length = struct.pack('H', 4 + 4 + 1 + 1 + 2 + struct.unpack('H', payload.length)[0])
        self.payload = payload

class NetworkLayer:
    name = "Layer 3"

    @staticmethod
    def run(device, data):
        if type(data) == Segment:
            packet = NetworkLayer.encapsulate(data, device.name, "Host B" if device.name == "Host A" else "Host A")
            src_ip, dest_ip = NetworkLayer.get_string_rep_ip(packet.src_ip), NetworkLayer.get_string_rep_ip(packet.dest_ip)
            print(f"{device.name}: {NetworkLayer.name}: Segment received from Transport Layer: SRC_IP={src_ip}, DST_IP={dest_ip}, TTL={struct.unpack('B', packet.ttl)[0]}")
            print(f"{device.name}: {NetworkLayer.name}: Destination IP read: {dest_ip}")
            next_hop_ip = NetworkLayer.forward(device)
            print(f"{device.name}: {NetworkLayer.name}: Routing table lookup performed")
            print(f"{device.name}: {NetworkLayer.name}: Next-hop IP determined: {NetworkLayer.get_string_rep_ip(next_hop_ip)}")
            print(f"{device.name}: {NetworkLayer.name}: Outgoing interface selected.")
            print(f"{device.name}: {NetworkLayer.name}: Packet Forwarded to Data Link Layer\n")
            DataLinkLayer.run(device, packet, next_hop_ip)
        
        elif type(data) == Frame:
            packet = data.payload
            src_ip, dest_ip = NetworkLayer.get_string_rep_ip(packet.src_ip), NetworkLayer.get_string_rep_ip(packet.dest_ip)
            print(f"{device.name}: {NetworkLayer.name}: Segment received from Transport Layer: SRC_IP={src_ip}, DST_IP={dest_ip}, TTL={struct.unpack('B', packet.ttl)[0]}")
            print(f"{device.name}: {NetworkLayer.name}: Destination IP read: {dest_ip}")
            if type(device) != Router and name_to_ip[device.name] == packet.dest_ip:
                print(f"{device.name}: {NetworkLayer.name}: Packet identified as local delivery")
                print(f"{device.name}: {NetworkLayer.name}: Segment delivered to Transport Layer\n")
                TransportLayer.run(device, packet)
            else:
                NetworkLayer.ttl_handling(packet)
                ttl = struct.unpack('B', packet.ttl)[0]
                print(f"{device.name}: {NetworkLayer.name}: TTL decremented: {ttl + 1} → {ttl}")
                if type(device) != Router:
                    next_hop_ip = NetworkLayer.forward(device)
                else:
                    interface = "Interface 1" if ip_to_network(packet.dest_ip) == ip_to_network(name_to_ip["Interface 1"]) else "Interface 2"
                    next_hop_ip = NetworkLayer.forward(device, interface)
                print(f"{device.name}: {NetworkLayer.name}: Routing table lookup performed")
                print(f"{device.name}: {NetworkLayer.name}: Next-hop IP determined: {NetworkLayer.get_string_rep_ip(next_hop_ip)}")
                print(f"{device.name}: {NetworkLayer.name}: Outgoing interface selected.")
                print(f"{device.name}: {NetworkLayer.name}: Packet Forwarded to Data Link Layer\n")
                DataLinkLayer.run(device, packet, next_hop_ip)
    
    @staticmethod
    def get_string_rep_ip(ip_addr):
        return '.'.join(list(map(lambda x: str(x), struct.unpack("4B", ip_addr))))

    @staticmethod
    def encapsulate(segment, src_hostname, dest_hostname):
        return Packet(segment, src_hostname, dest_hostname)

    @staticmethod
    def forward(device, interface=None):
        if interface is not None:
            return ROUTING_TABLE[device.name][interface]
        return ROUTING_TABLE[device.name]

    @staticmethod
    def ttl_handling(packet):
        ttl = struct.unpack('B', packet.ttl)[0]
        ttl -= 1

        if ttl == 0:
            del packet
        else:
            packet.ttl = struct.pack('B', ttl)

# Transport Layer

class Segment:
    def __init__(self, data, count=0):
        self.src_port = struct.pack('H', 5000)
        self.dest_port = struct.pack('H', 80)
        self.length = struct.pack('H', 2 + 2 + 2 + 2 + 1 + 1 + struct.unpack('B', data.value)[0])
        self.type = struct.pack('B', data.type)
        self.seq_num = struct.pack('B', count % 2)
        self.data = data
        self.checksum = self.generate_checksum()
    
    def generate_checksum(self):
        rep_segment = self.src_port + self.dest_port + self.length + self.type + self.seq_num + self.data.value
        if len(rep_segment) % 2 != 0:
            rep_segment += struct.pack('B', 0)
        
        words = []
        for idx in range(0, len(rep_segment), 2):
            words.append(rep_segment[idx] + rep_segment[idx + 1])
        
        result = sum(words)
        while result > (2 ** 16 - 1):
            result %= (2 ** 16 - 1)
        
        checksum = 2 ** 16 - 1 - result
        
        return struct.pack('H', checksum)

class TransportLayer:
    name = "Layer 4"

    @staticmethod
    def run(device, data, count):
        if type(data) == Data:
            print(f"{device.name}: {TransportLayer.name}: Data received from Application Layer. Data size={struct.unpack('B', data.value)[0]}")
            segment = Segment(data, count)
            print(f"{device.name}: {TransportLayer.name}: Checksum computed")
            print(f"{device.name}: {TransportLayer.name}: Segment created by adding transport layer header (DATA, seq={struct.unpack('B', segment.seq_num)[0]}) (encapsulation)")
            print(f"{device.name}: {TransportLayer.name}: Segment sent to Network Layer\n")
            NetworkLayer.run(device, segment)
        
        elif type(data) == Packet:
            print(f"{device.name}: {TransportLayer.name}: Segment received from Network Layer")
            segment = data.payload
            if segment.generate_checksum() == segment.checksum:
                print(f"{device.name}: {TransportLayer.name}: Checksum verified")
                print(f"{device.name}: {TransportLayer.name}: DATA segment delivered to Application Layer. Data size={struct.unpack('B', segment.data.value)[0]}\n")

    @staticmethod
    def rdt():
        pass