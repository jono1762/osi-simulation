import struct

HOSTS = ["Host A", "Host B"]
INTERFACES = ["Interface 1", "Interface 2"]

name_to_ip = {
    "Host A": "10.0.1.10", 
    "Host B": "10.0.2.20",
    "Interface 1": "10.0.1.1",
    "Interface 2": "10.0.2.1",
    "Network 1": "10.0.1.0",
    "Network 2": "10.0.2.0"
}

name_to_mac = {
    "Host A": "AA:AA:AA:AA:AA:AA",
    "Interface 1": "BB:BB:BB:BB:BB:BB", 
    "Interface 2": "CC:CC:CC:CC:CC:CC",
    "Host B": "DD:DD:DD:DD:DD:DD"
}

def bitwise_and(num1, num2):
    result = ""
    
    for i in range(len(num1)):
        if num1[i] == num2[i] == 1:
            result += '1'
        else:
            result += '0'
    
    return result

for name, ip_addr in name_to_ip.items():
    d1, d2, d3, d4 = list(map(lambda x: int(x), ip_addr.split('.')))
    name_to_ip[name] = struct.pack("4B", d1, d2, d3, d4)

def ip_to_binary(ip_addr):
    return ''.join([bin(int(num))[2:].zfill(8) for num in ip_addr.split('.')])

def ip_to_network(ip_addr):
    return "Network 1" if struct.unpack("4B", ip_addr)[:-1] == struct.unpack("4B", name_to_ip["Network 1"])[:-1] else "Network 2"

def generate_routing_table():
    routing_table = {}

    for host in HOSTS:
        routing_table[host] = name_to_ip["Interface 1"] if ip_to_network(name_to_ip[host]) == "Network 1" else name_to_ip["Interface 2"]
    
    routing_table["Router R1"] = {}
    routing_table["Router R1"]["Interface 1"] = name_to_ip["Host A"]
    routing_table["Router R1"]["Interface 2"] = name_to_ip["Host B"]
    
    # routing_table[[name_to_ip]]
    # # Make interfaces routing table under one router
    # for interface in INTERFACES:
    #     routing_table[name_to_ip[interface]] = name_to_ip["Interface 2"] if interface == "Interface 1" else name_to_ip["Interface 2"]
    
    return routing_table

ROUTING_TABLE = generate_routing_table()