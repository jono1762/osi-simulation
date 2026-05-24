from config import name_to_ip, name_to_mac, ip_to_network, ROUTING_TABLE, HOSTS, INTERFACES
from devices import DEVICES, Router
import struct
from copy import deepcopy

# Application Layer

class Data:
    def __init__(self, value=None):
        self.value = struct.pack('H', value)
        self.type = struct.pack('B', 0 if value != 0 else 1)

# Data Link Layer

class Frame:
    def __init__(self, src_mac, dest_mac, packet):
        self.src_mac = src_mac
        self.dest_mac = dest_mac
        self.type = struct.pack('H', 8 * 16 ** 2)
        self.payload = packet

class DataLinkLayer:
    name = "Layer 2"

    @staticmethod
    def run(device, data, next_hop_ip=None, interface=None):
        if type(data) == Frame: #receive frame from LAN
            if interface is not None:
                print(f"{device.name}: {DataLinkLayer.name}: Frame received on {interface}")
                print(f"{device.name}: {DataLinkLayer.name}: Source MAC learned: {DataLinkLayer.get_string_rep_mac(data.src_mac)} on {interface}")
            else:
                print(f"{device.name}: {DataLinkLayer.name}: Frame received")
                print(f"{device.name}: {DataLinkLayer.name}: Source MAC learned: {DataLinkLayer.get_string_rep_mac(data.src_mac)}")
            # if data.src_mac not in device.mac_table:
            #     device.mac_table[data.payload.src_ip] = data.src_mac
            print(f"{device.name}: {DataLinkLayer.name}: Packet delivered to Network Layer\n")
            NetworkLayer.run(device, data)
        
        elif type(data) == Packet: #receive packet from network layer
            print(f"{device.name}: {DataLinkLayer.name}: Packet received from Network Layer")
            # Determine how to learn MAC address
            src_name = device.name if type(device) != Router else "Interface 1" if name_to_ip["Host A"] == next_hop_ip else "Interface 2"
            src_mac = device.mac_address if type(device) != Router else name_to_mac[src_name]
            dest_name, dest_mac = DataLinkLayer.get_dest_mac_address(next_hop_ip)
            print(f"{device.name}: {DataLinkLayer.name}: Destination MAC lookup for next-hop IP ({NetworkLayer.get_string_rep_ip(next_hop_ip)}) → {DataLinkLayer.get_string_rep_mac(dest_mac)}")
            frame = DataLinkLayer.encapsulate(src_mac, dest_mac, data)
            print(f"{device.name}: {DataLinkLayer.name}: Frame created: SRC_MAC={DataLinkLayer.get_string_rep_mac(src_mac)}, DST_MAC={DataLinkLayer.get_string_rep_mac(dest_mac)}")
            if type(device) != Router:
                print(f"{device.name}: {DataLinkLayer.name}: Frame sent\n")
            else:
                print(f"{device.name}: {DataLinkLayer.name}: Frame forwarded on {src_name}\n")
            if dest_name in HOSTS:
                DataLinkLayer.run(DEVICES[dest_name], frame, None)
            if dest_name in INTERFACES:
                DataLinkLayer.run(DEVICES["Router R1"], frame, None, dest_name)

    @staticmethod
    def encapsulate(src_mac, dest_mac, packet):
        return Frame(src_mac, dest_mac, packet)

    @staticmethod
    def get_dest_mac_address(next_hop_ip):
        for name, ip in name_to_ip.items():
            if ip == next_hop_ip:
                return name, name_to_mac[name]
    
    @staticmethod
    def get_string_rep_mac(mac_addr):
        return struct.unpack("17s", mac_addr)[0].decode('utf-8')

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
            print(f"{device.name}: {NetworkLayer.name}: Outgoing interface selected")
            print(f"{device.name}: {NetworkLayer.name}: Packet forwarded to Data Link Layer\n")
            DataLinkLayer.run(device, packet, next_hop_ip)
        
        elif type(data) == Frame:
            packet = data.payload
            src_ip, dest_ip = NetworkLayer.get_string_rep_ip(packet.src_ip), NetworkLayer.get_string_rep_ip(packet.dest_ip)
            print(f"{device.name}: {NetworkLayer.name}: Packet received from Data Link Layer: SRC_IP={src_ip}, DST_IP={dest_ip}, TTL={struct.unpack('B', packet.ttl)[0]}")
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
                print(f"{device.name}: {NetworkLayer.name}: Outgoing interface selected ({interface})")
                print(f"{device.name}: {NetworkLayer.name}: Packet forwarded to Data Link Layer\n")
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
LARGEST_NUM = 2 ** 16 - 1

class Segment:
    def __init__(self, data, seq_num):
        self.src_port = struct.pack('H', 5000)
        self.dest_port = struct.pack('H', 80)
        self.length = struct.pack('H', 2 + 2 + 2 + 2 + 1 + 1 + struct.unpack('H', data.value)[0])
        self.type = struct.pack('B', struct.unpack('B', data.type)[0])
        self.seq_num = struct.pack('B', seq_num)
        self.data = data
        self.checksum = struct.pack('H', LARGEST_NUM - self.generate_checksum())
    
    def generate_checksum(self):
        rep_segment = self.src_port + self.dest_port + self.length + self.type + self.seq_num + self.data.value
        if len(rep_segment) % 2 != 0:
            rep_segment += struct.pack('B', 0)
        
        words = []
        for i in range(0, len(rep_segment), 2):
            words.append(rep_segment[i: i + 2])

        result = 0
        for word in words:
            result += struct.unpack('H', word)[0]

        if result > LARGEST_NUM:
            result = result // LARGEST_NUM + result % LARGEST_NUM
               
        return result

data_left = None
expected_seq = None
original_data = None

class TransportLayer:
    name = "Layer 4"

    @staticmethod
    def run(device, data):
        global data_left, expected_seq, original_data

        if type(data) == Data:
            if data_left == 0:
                return
            
            if data_left is None and expected_seq is None:
                data_left = struct.unpack('H', data.value)[0]
                expected_seq = 0
                original_data = data
                print(f"{device.name}: {TransportLayer.name}: Data received from Application Layer. Data size={struct.unpack('H', data.value)[0]}")
            
            segment = TransportLayer.create_segment(data, expected_seq)
            print(f"{device.name}: {TransportLayer.name}: Checksum computed")
            print(f"{device.name}: {TransportLayer.name}: Segment created by adding transport layer header (DATA, seq={struct.unpack('B', segment.seq_num)[0]}) (encapsulation)")
            print(f"{device.name}: {TransportLayer.name}: Segment sent to Network Layer\n")
            NetworkLayer.run(device, segment)    
        
        elif type(data) == Packet:
            print(f"{device.name}: {TransportLayer.name}: Segment received from Network Layer")
            segment = data.payload
            if LARGEST_NUM - segment.generate_checksum() == struct.unpack('H', segment.checksum)[0]:
                print(f"{device.name}: {TransportLayer.name}: Checksum verified")
                if struct.unpack('B', segment.type)[0] == 0:
                    print(f"{device.name}: {TransportLayer.name}: DATA segment delivered to Application Layer. Data size={struct.unpack('H', segment.data.value)[0]}")
                    ack = Data(0)
                    seq_num = struct.unpack('B', segment.seq_num)[0]
                    ack_segment = Segment(ack, seq_num)
                    print(f"{device.name}: {TransportLayer.name}: Segment created by adding transport layer header (ACK, seq={seq_num})")
                    print(f"{device.name}: {TransportLayer.name}: Segment sent to Network Layer\n")
                    NetworkLayer.run(device, ack_segment)
                else:
                    ack_seq = struct.unpack('B', segment.seq_num)[0]
                    if expected_seq == ack_seq:
                        print(f"{device.name}: {TransportLayer.name}: ACK received: seq={ack_seq}")
                        expected_seq = 1 - ack_seq
                        TransportLayer.run(device, original_data)

    @staticmethod
    def create_segment(data, seq_num):
        global data_left
        split_data = deepcopy(data)
        value = 500 if data_left > 500 else data_left
        split_data.value = struct.pack('H', value)
        data_left -= value
        return Segment(split_data, seq_num)