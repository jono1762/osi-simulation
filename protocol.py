from config import name_to_ip, ROUTING_TABLE
import struct

# Application Layer

class Data:
    def __init__(self, value=None):
        self.value = struct.pack('B', value)
        self.type = "DATA" if value is not None else "ACK"

# Data Link Layer

class Frame:
    def init(self, src_mac, dest_mac, packet):
        self.src_mac = src_mac
        self.dest_mac = dest_mac
        self.type = 2
        self.payload = packet

class DataLinkLayer:
    name = "Layer 2"
    def run(self, device, data, next_hop_ip):
        if type(data) == Frame: #recieve frame from LAN
            print("Frame Recieved")
            if data.src_mac not in device.mac_table:
                device.mac_table[data.src_ip] = data.src_mac
                print("Layer 2: MAC Address Learned")
            self.deliver()
        elif type(data) == Packet: #recieve packet from network layer
            print("Layer 2: Packet recieved from Network Layer")
            #determine how the dest mac address
            #learn mac address
            dest_mac = device.mac_table[next_hop_ip]
            frame = self.encapsulate(device.mac_address, dest_mac, data)
            self.send_across_link(frame)

    def encapsulate(self, src_mac, dest_mac, packet):
        frame = Frame(src_mac, dest_mac, packet)
        print(f"Layer 2: Frame created: SRC_MAC={src_mac}, DST_MAC={dest_mac}")
        return frame

    def send_across_link(frame): #sends frame across a link -> print
        print("Layer 2: Frame forwarded")
        return frame
 
    def deliver(data): #delivers packet to Network layer -> print
        packet = data.payload
        print("Layer 2: Packet Delivered to Network Layer")
        return packet

class Packet:
    def __init__(self, payload, src_hostname, dest_hostname):
        self.src_ip = name_to_ip[src_hostname]
        self.dest_ip = name_to_ip[dest_hostname]
        self.ttl = struct.pack('B', 100)
        self.protocol = struct.pack('B', 17)
        self.length = struct.pack('H', 4 + 4 + 1 + 1 + 2 + payload.length)
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
            next_hop_ip = NetworkLayer.forward(device)
            print(f"{device}: {NetworkLayer.name}: Routing table lookup performed")
            print(f"{device}: {NetworkLayer.name}: Next-hop IP determined: {NetworkLayer.get_string_rep_ip(next_hop_ip)}")
            print(f"{device}: {NetworkLayer.name}: Outgoing interface selected.")
            print(f"{device}: {NetworkLayer.name}: Packet Forwarded to Data Link Layer")
            DataLinkLayer.run(device, packet, next_hop_ip)
        
        elif type(data) == Frame:
            packet = data.payload
            src_ip, dest_ip = NetworkLayer.get_string_rep_ip(packet.src_ip), NetworkLayer.get_string_rep_ip(packet.dest_ip)
            print(f"{device}: {NetworkLayer.name}: Segment received from Transport Layer: SRC_IP={src_ip}, DST_IP={dest_ip}, TTL={struct.unpack('B', packet.ttl)}")
            print(f"{device}: {NetworkLayer.name}: Destination IP read: {dest_ip}")
            if name_to_ip[device] == packet.dest_ip:
                print(f"{device}: {NetworkLayer.name}: Packet identified as local delivery")
                print(f"{device}: {NetworkLayer.name}: Segment delivered to Transport Layer")
                TransportLayer.run(device, packet)
            else:
                NetworkLayer.ttl_handling(packet)
                print(f"{device}: {NetworkLayer.name}: TTL decremented: {struct.unpack('B', packet.ttl) + 1} → {struct.unpack('B', packet.ttl)}")
                next_hop_ip = NetworkLayer.forward(device)
                print(f"{device}: {NetworkLayer.name}: Routing table lookup performed")
                print(f"{device}: {NetworkLayer.name}: Next-hop IP determined: {next_hop_ip}")
                print(f"{device}: {NetworkLayer.name}: Outgoing interface selected.")
                print(f"{device}: {NetworkLayer.name}: Packet Forwarded to Data Link Layer")
                DataLinkLayer.run(device, packet, next_hop_ip)
    
    @staticmethod
    def get_string_rep_ip(ip_addr):
        return '.'.join(list(map(lambda x: str(x), struct.unpack("4B", ip_addr))))

    @staticmethod
    def encapsulate(segment, src_hostname, dest_hostname):
        return Packet(segment, src_hostname, dest_hostname)

    @staticmethod
    def forward(device):
        return ROUTING_TABLE[name_to_ip[device]]

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
    def __init__(self, data, count=0):
        self.src_port = struct.pack('H', 5000)
        self.dest_port = struct.pack('H', 80)
        self.length = struct.pack('H', 2 + 2 + 2 + 2 + 1 + 1 + data.length)
        self.type = struct.pack('B', data.type)
        self.seq_num = struct.pack('B', count % 2)
        self.data = data
        self.checksum = self.generate_checksum()
    
    def generate_checksum(self):
        pass

class TransportLayer:
    def run(self, data):
        #take input and cr
        if type(data) == Data:
            #create segment
            segment = Segment(seq=sequence_number, data=data)
            #split segment if too long

            #Sender Side -> Use Sequence Number
            pass
        elif type(data) == Packet:
            #Reciever Side -> send ack
            #recieving device needs expected sequence number
            pass

    def send(data):

    def recieve(data):
        #if segment.sequence_number =  expected_sequence_number:
            #send ack  
            #update expected ack
    


