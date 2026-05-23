import struct

DEVICES = ["Host A", "Host B"]
INTERFACES = ["Interface 1", "Interface 2"]

name_to_ip = {
    "Host A": "10.0.1.10", 
    "Host B": "10.0.2.20",
    "Interface 1": "10.0.1.1",
    "Interface 2": "10.0.2.1",
    "Network 1": "10.0.1.0",
    "Network 2": "10.0.2.0"
}

for name, ip_addr in name_to_ip.items():
    d1, d2, d3, d4 = list(map(lambda x: int(x), ip_addr.split('.')))
    name_to_ip[name] = struct.pack("4B", d1, d2, d3, d4)
    print([d1, d2, d3, d4], name_to_ip[name])

def ip_to_network(ip_addr):
    return "Network 1" if struct.unpack("4B", ip_addr)[:-1] == struct.unpack("4B", name_to_ip["Network 1"])[:-1] else "Network 2"

def generate_routing_table():
    routing_table = {}

    for device in DEVICES:
        routing_table[name_to_ip[device]] = name_to_ip["Interface 1"] if ip_to_network(name_to_ip[device]) == "Network 1" else name_to_ip["Interface 2"]
    
    for interface in INTERFACES:
        routing_table[name_to_ip[interface]] = name_to_ip["Interface 2"] if interface == "Interface 1" else name_to_ip["Interface 2"]
    
    return routing_table

ROUTING_TABLE = generate_routing_table()
print(ROUTING_TABLE)