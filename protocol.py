#Layer 2: Data Link Layer (Ethernet-like Frame)
#❖ Destination MAC (6 bytes) → e.g., BB:BB:BB:BB:BB:BB
#❖ Source MAC (6 bytes) → e.g., AA:AA:AA:AA:AA:AA
#❖ Type (2 bytes) → 0x0800 (indicates IPv4 payload)
#❖ Payload (variable) → contains the Layer 3 (IP) packet
class Frame:
    self.DestinationMAC = BB:BB:BB:BB:BB:BB
    self.SourceMAC = AA:AA:AA:AA:AA:AA
    self.Type = (indicates IPv4 payload)
    self.Payload = packet

class DataLinkLayer:
    def data_link_methods():
        pass
    def data_link_methods():
        pass
    def data_link_methods():
        pass

# Layer 3: Header (IP-like Packet)
#❖ Source IP (4 bytes) → e.g., 10.0.1.10
#❖ Destination IP (4 bytes) → e.g., 10.0.2.20
#❖ TTL (1 byte) → 100 (decremented at each router)
#❖ Protocol (1 byte) → 17 (indicates UDP payload)
#❖ Total Length (2 bytes) → e.g., 40 (header + payload size)
#❖ Payload (variable) → contains the Layer 4 (UDP segment)
class Packet:
        

class Header:
# Layer 4: Header (UDP-like Segment with ACK support)
#❖ Source Port (2 bytes) → e.g., 5000
#❖ Destination Port (2 bytes) → e.g., 80
#❖ Length (2 bytes) → e.g., 100 (header + data)
#❖ Checksum (2 bytes) → e.g., computed value for error detection
#❖ Type (1 byte) → 0 = DATA, 1 = ACK
#❖ Sequence Number (1 byte) → e.g., 0 or 1
#❖ Data (variable) → contains the application message (empty for ACK)