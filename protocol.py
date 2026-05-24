from config import name_to_ip, name_to_mac, ROUTING_TABLE, HOSTS, INTERFACES
from devices import DEVICES, Router
import struct # Used to encode data into binary bytes to meet task specifications and for use in computing checksum
from copy import deepcopy

# APPLICATION LAYER

class Data:
    '''
    Create data object containing application message.
    '''
    def __init__(self, value):
        self.value = struct.pack('H', value)
        self.type = struct.pack('B', 0 if value != 0 else 1)

# DATA LINK LAYER

class Frame:
    '''
    Create frame object which encapsulates packet accessed via payload.
    '''
    def __init__(self, src_mac, dest_mac, packet):
        self.src_mac = src_mac
        self.dest_mac = dest_mac
        self.type = struct.pack('H', 8 * 16 ** 2) # 8 * 16 ** 2 = 2048 (decimal) = 0800 (hexadecimal)
        self.payload = packet

class DataLinkLayer:
    '''
    Functions as a static class to group related methods together to
    implement the data link layer.
    '''
    name = "Layer 2"

    @staticmethod
    def run(device, data, next_hop_ip=None, interface=None):
        '''
        Core code that implements the data link layer, calling the other 
        methods grouped under the same class as relevant.
        '''
        if type(data) == Frame: # Checks if previous layer was data link layer (implies sending frame between devices)
            if interface is not None:
                print(f"{device.name}: {DataLinkLayer.name}: Frame received on {interface}")             
            else:
                print(f"{device.name}: {DataLinkLayer.name}: Frame received")
            
            if data.src_mac not in device.mac_table: # Learn MAC address if not learnt before
                device.mac_table[data.src_mac] = interface
                print(f"{device.name}: {DataLinkLayer.name}: Source MAC learned: {DataLinkLayer.get_string_rep_mac(data.src_mac)}")
            print(f"{device.name}: {DataLinkLayer.name}: Packet delivered to Network Layer\n")
            NetworkLayer.run(device, data) # Pass frame into network layer
        
        elif type(data) == Packet: # Checks if previous layer was network layer (implies moving down protocol stack)
            print(f"{device.name}: {DataLinkLayer.name}: Packet received from Network Layer")
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
                DataLinkLayer.run(DEVICES[dest_name], frame, None) # Pass frame to destination host's data link layer
            if dest_name in INTERFACES:
                DataLinkLayer.run(DEVICES["Router R1"], frame, None, dest_name) # Pass frame to router's data link layer via interface

    @staticmethod
    def encapsulate(src_mac, dest_mac, packet):
        '''
        Encapsulates packet into frame.
        '''
        return Frame(src_mac, dest_mac, packet)

    @staticmethod
    def get_dest_mac_address(next_hop_ip):
        '''
        For a given IP address, return the corresponding MAC address.
        '''
        for name, ip in name_to_ip.items():
            if ip == next_hop_ip:
                return name, name_to_mac[name]
    
    @staticmethod
    def get_string_rep_mac(mac_addr):
        '''
        Generate the string representation of a MAC address represented using binary for log output.
        '''
        return ':'.join(list(map(lambda x: hex(x)[2:].upper(), struct.unpack("6B", mac_addr))))

# NETWORK LAYER

class Packet:
    '''
    Create packet object which encapsulates segment accessed via payload.
    '''
    def __init__(self, payload, src_hostname, dest_hostname):
        self.src_ip = name_to_ip[src_hostname]
        self.dest_ip = name_to_ip[dest_hostname]
        self.ttl = struct.pack('B', 100)
        self.protocol = struct.pack('B', 17)
        self.length = struct.pack('H', 4 + 4 + 1 + 1 + 2 + struct.unpack('H', payload.length)[0])
        self.payload = payload

class NetworkLayer:
    '''
    Functions as a static class to group related methods together to
    implement the network layer.
    '''
    name = "Layer 3"

    @staticmethod
    def run(device, data):
        '''
        Core code that implements the network layer, calling the other 
        methods grouped under the same class as relevant.
        '''
        if type(data) == Segment: # Checks if previous layer was transport layer (implies moving down protocol stack)
            packet = NetworkLayer.encapsulate(data, device.name, "Host B" if device.name == "Host A" else "Host A")
            src_ip, dest_ip = NetworkLayer.get_string_rep_ip(packet.src_ip), NetworkLayer.get_string_rep_ip(packet.dest_ip)
            print(f"{device.name}: {NetworkLayer.name}: Segment received from Transport Layer: SRC_IP={src_ip}, DST_IP={dest_ip}, TTL={struct.unpack('B', packet.ttl)[0]}")
            print(f"{device.name}: {NetworkLayer.name}: Destination IP read: {dest_ip}")
            interface, next_hop_ip = NetworkLayer.forward(device, packet.dest_ip)
            print(f"{device.name}: {NetworkLayer.name}: Routing table lookup performed")
            print(f"{device.name}: {NetworkLayer.name}: Next-hop IP determined: {NetworkLayer.get_string_rep_ip(next_hop_ip)}")
            print(f"{device.name}: {NetworkLayer.name}: Outgoing interface selected")
            print(f"{device.name}: {NetworkLayer.name}: Packet forwarded to Data Link Layer\n")
            DataLinkLayer.run(device, packet, next_hop_ip) # Pass packet into data link layer
        
        elif type(data) == Frame: # Checks if previous layer was data link layer (implies moving up protocol stack)
            packet = data.payload
            src_ip, dest_ip = NetworkLayer.get_string_rep_ip(packet.src_ip), NetworkLayer.get_string_rep_ip(packet.dest_ip)
            print(f"{device.name}: {NetworkLayer.name}: Packet received from Data Link Layer: SRC_IP={src_ip}, DST_IP={dest_ip}, TTL={struct.unpack('B', packet.ttl)[0]}")
            print(f"{device.name}: {NetworkLayer.name}: Destination IP read: {dest_ip}")
            if type(device) != Router and name_to_ip[device.name] == packet.dest_ip: # Check if IP address matches current device's (know if reached destination)
                print(f"{device.name}: {NetworkLayer.name}: Packet identified as local delivery")
                print(f"{device.name}: {NetworkLayer.name}: Segment delivered to Transport Layer\n")
                TransportLayer.run(device, packet)  # Pass packet into transport layer
            else:
                dropped = NetworkLayer.ttl_handling(packet)
                if dropped: # Terminate execution if packet expired.
                    print(f"{device.name}: {NetworkLayer.name}: Packet TTL expired")
                    return
                ttl = struct.unpack('B', packet.ttl)[0]
                print(f"{device.name}: {NetworkLayer.name}: TTL decremented: {ttl + 1} → {ttl}")
                interface, next_hop_ip = NetworkLayer.forward(device, packet.dest_ip)
                print(f"{device.name}: {NetworkLayer.name}: Routing table lookup performed")
                print(f"{device.name}: {NetworkLayer.name}: Next-hop IP determined: {NetworkLayer.get_string_rep_ip(next_hop_ip)}")
                print(f"{device.name}: {NetworkLayer.name}: Outgoing interface selected ({interface})")
                print(f"{device.name}: {NetworkLayer.name}: Packet forwarded to Data Link Layer\n")
                DataLinkLayer.run(device, packet, next_hop_ip)  # Pass packet into data link layer
    
    @staticmethod
    def get_string_rep_ip(ip_addr):
        '''
        Generate the string representation of an IP address represented using binary for log output.
        '''
        return '.'.join(list(map(lambda x: str(x), struct.unpack("4B", ip_addr))))

    @staticmethod
    def encapsulate(segment, src_hostname, dest_hostname):
        '''
        Encapsulates segment into packet.
        '''
        return Packet(segment, src_hostname, dest_hostname)

    @staticmethod
    def forward(device, dest_ip):
        '''
        Return the next-hop IP address to reach a specific host 
        from the current device.
        '''
        return ROUTING_TABLE[device.name][dest_ip].values()

    @staticmethod
    def ttl_handling(packet):
        '''
        Decrement TTL every time packet reaches new router.
        '''
        ttl = struct.unpack('B', packet.ttl)[0]
        ttl -= 1

        if ttl == 0: # Discard packet if ttl hits 0 (expired)
            del packet
            return True
        else:
            packet.ttl = struct.pack('B', ttl)

        return False

# TRANSPORT LAYER
LARGEST_NUM = 2 ** 16 - 1

class Segment:
    '''
    Create segment object which encapsulates data message accessed via payload.
    '''
    def __init__(self, data, seq_num):
        self.src_port = struct.pack('H', 5000)
        self.dest_port = struct.pack('H', 80)
        self.length = struct.pack('H', 2 + 2 + 2 + 2 + 1 + 1 + struct.unpack('H', data.value)[0])
        self.type = struct.pack('B', struct.unpack('B', data.type)[0])
        self.seq_num = struct.pack('B', seq_num)
        self.data = data
        self.checksum = struct.pack('H', LARGEST_NUM - self.generate_checksum())
    
    def generate_checksum(self):
        '''
        Generate a checksum for a given segment then stores it.
        '''
        rep_segment = self.src_port + self.dest_port + self.length + self.type + self.seq_num + self.data.value # Concatenate byte representations of fields
        if len(rep_segment) % 2 != 0: # Pad if odd number of bytes
            rep_segment += struct.pack('B', 0)
        
        words = []
        for i in range(0, len(rep_segment), 2):
            words.append(rep_segment[i: i + 2]) # Segment byte string into 16-bit (2-byte) words
        
        result = 0
        for word in words:
            result += struct.unpack('H', word)[0] # Sum words together

        while result > LARGEST_NUM: # Account for overflow
            result = result // LARGEST_NUM + result % LARGEST_NUM
               
        return result

data_left = None
original_data = None
last_segment = None
expected_seq_num = 0
last_seq_num = 1

class TransportLayer:
    '''
    Functions as a static class to group related methods together to
    implement the transport layer.
    '''
    name = "Layer 4"

    @staticmethod
    def run(device, data):
        '''
        Core code that implements the transport layer, calling the other 
        methods grouped under the same class as relevant.
        '''
        global data_left, expected_seq_num, original_data, last_seq_num, last_segment

        if type(data) == Data: # Checks if previous layer was application layer (implies moving down protocol stack)
            if data_left == 0: # No more segments to send
                return
            
            if data_left is None: # Scenario when initially receive data from application layer
                data_left = struct.unpack('H', data.value)[0]
                original_data = data
                print(f"{device.name}: {TransportLayer.name}: Data received from Application Layer. Data size={struct.unpack('H', data.value)[0]}")
            
            segment = TransportLayer.create_segment(data, expected_seq_num)
            last_segment = segment
            print(f"{device.name}: {TransportLayer.name}: Checksum computed")
            print(f"{device.name}: {TransportLayer.name}: Segment created by adding transport layer header (DATA, seq={struct.unpack('B', segment.seq_num)[0]}) (encapsulation)")
            print(f"{device.name}: {TransportLayer.name}: Segment sent to Network Layer\n")
            NetworkLayer.run(device, segment)    
        
        elif type(data) == Packet: # Checks if previous layer was network layer (implies moving up protocol stack)
            print(f"{device.name}: {TransportLayer.name}: Segment received from Network Layer")
            segment = data.payload
            is_data = struct.unpack('B', segment.type)[0] == 0

            checksum_matches = LARGEST_NUM - segment.generate_checksum() == struct.unpack('H', segment.checksum)[0]
            not_duplicate = last_seq_num != struct.unpack('B', segment.seq_num)[0]
            seq_num_matches = expected_seq_num == struct.unpack('B', segment.seq_num)[0]
            seq_num = struct.unpack('B', segment.seq_num)[0]

            if is_data: # Check the message type is DATA
                if checksum_matches: # Check if checksum matches (data received correctly)
                    print(f"{device.name}: {TransportLayer.name}: Checksum verified")
                    last_seq_num = 1 - last_seq_num
                    if not_duplicate: # Check message not been received before
                        print(f"{device.name}: {TransportLayer.name}: DATA segment delivered to Application Layer. Data size={struct.unpack('H', segment.data.value)[0]}")
                    else:
                        print(f"{device.name}: {TransportLayer.name}: Duplicate DATA segment but will send ACK")
                    ack = TransportLayer.create_ack(seq_num)
                    print(f"{device.name}: {TransportLayer.name}: Segment created by adding transport layer header (ACK, seq={seq_num})")
                    print(f"{device.name}: {TransportLayer.name}: Segment sent to Network Layer\n")
                    NetworkLayer.run(device, ack) # Pass segment into network layer

                else:
                    ack = TransportLayer.create_ack(last_seq_num) # Re-send last ACK
                    print(f"{device.name}: {TransportLayer.name}: Checksum failed")
                    print(f"{device.name}: {TransportLayer.name}: Retransmitting last segment (ACK, seq={last_seq_num})")
                    print(f"{device.name}: {TransportLayer.name}: Segment sent to Network Layer\n")
                    NetworkLayer.run(device, ack) # Pass segment into network layer

            else: # Check the message type is ACK
                if checksum_matches and seq_num_matches: # Check the checksum and sequence number match (expected ACK received correctly)
                    print(f"{device.name}: {TransportLayer.name}: Checksum verified")
                    seq_num = struct.unpack('B', segment.seq_num)[0]
                    last_seq_num = seq_num
                    expected_seq_num = 1 - expected_seq_num
                    print(f"{device.name}: {TransportLayer.name}: ACK received: seq={seq_num}\n")
                    TransportLayer.run(device, original_data) # Run transmission for next segment of data

                else:
                    print(f"{device.name}: {TransportLayer.name}: Checksum failed or unexpected ACK")
                    print(f"{device.name}: {TransportLayer.name}: Retransmitting last segment\n")
                    NetworkLayer.run(device, last_segment) # Run transmission for current segment of data again

    @staticmethod
    def create_segment(data, seq_num):
        '''
        Create a segment, accounting for limit of 500 bytes by
        segmentation.
        '''
        global data_left
        split_data = deepcopy(data)
        value = 500 if data_left > 500 else data_left
        split_data.value = struct.pack('H', value)
        data_left -= value
        return Segment(split_data, seq_num)

    @staticmethod
    def create_ack(seq_num):
        '''
        Create ACK with correct sequence number for segment verification.
        '''
        ack = Data(0)
        return Segment(ack, seq_num)