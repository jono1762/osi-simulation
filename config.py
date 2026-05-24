import struct

HOSTS = ["Host A", "Host B"]
INTERFACES = ["Interface 1", "Interface 2"]

# Map device names to IP addresses
name_to_ip = {
    "Host A": "10.0.1.10", 
    "Host B": "10.0.2.20",
    "Interface 1": "10.0.1.1",
    "Interface 2": "10.0.2.1",
    "Network 1": "10.0.1.0",
    "Network 2": "10.0.2.0"
}

# Map device names to MAC addresses
name_to_mac = {
    "Host A": "AA:AA:AA:AA:AA:AA",
    "Interface 1": "BB:BB:BB:BB:BB:BB", 
    "Interface 2": "CC:CC:CC:CC:CC:CC",
    "Host B": "DD:DD:DD:DD:DD:DD"
}

# Convert IP and MAC addresses from strings to binary bytes
for name, ip_addr in name_to_ip.items():
    d1, d2, d3, d4 = list(map(lambda x: int(x), ip_addr.split('.')))
    name_to_ip[name] = struct.pack("4B", d1, d2, d3, d4)

for name, mac_addr in name_to_mac.items():
    d1, d2, d3, d4, d5, d6 = list(map(lambda x: int(x, 16), mac_addr.split(':')))
    name_to_mac[name] = struct.pack("6B", d1, d2, d3, d4, d5, d6)

def generate_routing_table():
    '''
    Generates routing table for each device on the network, allowing efficient 
    access to the next-hop IP given a destination IP address. Only need to generate
    once while it remains static as it is assumed the network topology never changes.
    '''
    routing_table = {}
    for host in HOSTS:
        routing_table[host] = {}
    routing_table["Router R1"] = {}

    for host in HOSTS:
        dest = "Host B" if host == "Host A" else "Host A"
        interface = "Interface 2" if dest == "Host A" else "Interface 1"
        routing_table[host] = {}

        routing_table[host][name_to_ip[dest]] = {
            "Interface": interface,
            "Next-hop IP": name_to_ip[interface]
        }
    
        routing_table["Router R1"][name_to_ip[host]] = {
            "Interface": interface,
            "Next-hop IP": name_to_ip[host]
        }
    
    return routing_table

# Instantiate routing table
ROUTING_TABLE = generate_routing_table()