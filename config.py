DEVICES = ["Host A", "Host B"]
INTERFACES = ["Interface 1", "Interface 2"]
SUBNET_MASK = '1' * 24 + '0' * 8

name_to_ip = {
    "Host A": "10.0.1.10", 
    "Host B": "10.0.2.20",
    "Interface 1": "10.0.1.1",
    "Interface 2": "10.0.2.1",
    "Network 1": "10.0.1.0",
    "Network 2": "10.0.2.0"
}

def bitwise_and(num1, num2):
    result = ""
    
    for i in range(len(num1)):
        if num1[i] == num2[i] == 1:
            result += '1'
        else:
            result += '0'
    
    return result

def ip_to_binary(ip_addr):
    return ''.join([bin(int(num))[2:].zfill(8) for num in ip_addr.split('.')])

def ip_to_network(ip_addr):
    binary_ip_addr = ip_to_binary(ip_addr)
    binary_network_1_addr = ip_to_binary(name_to_ip["Network 1"])
    binary_network_2_addr = ip_to_binary(name_to_ip["Network 2"])

    if bitwise_and(binary_ip_addr, SUBNET_MASK) == binary_network_1_addr:
        return "Network 1"
    
    elif bitwise_and(binary_ip_addr, SUBNET_MASK) == binary_network_2_addr:
        return "Network 2"

def generate_routing_table():
    routing_table = {}

    for device in DEVICES:
        routing_table[name_to_ip[device]]["Outgoing Link"] = name_to_ip["Interface 1"] if ip_to_network(name_to_ip[device]) == "Network 1" else name_to_ip["Interface 2"]

ROUTING_TABLE = generate_routing_table()
