from config import name_to_ip, ROUTING_TABLE

# Application Layer

class Data:
    def __init__(self, value=None):
        self.value = value
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
            print("Packet recieved from Network Layer")
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
        print("Frame forwarded")
        return frame

    def deliver(data): #delivers packet to Network layer -> print
        packet = data.payload
        print("Packet Delivered to Network Layer")
        return packet

class Packet:
    def __init__(self, payload, src_hostname, dest_hostname):
        self.src_ip = name_to_ip[src_hostname]
        self.dest_ip = name_to_ip[dest_hostname]
        self.ttl = 100
        self.protocol = 17
        self.length = payload + (4 + 4 + 1 + 1 + 2)
        self.payload = payload

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
