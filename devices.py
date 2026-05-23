from config import name_to_ip, INTERFACES

class Host:
    def __init__(self, device_name):
        self.device_name = device_name
        self.ip_address = name_to_ip[device_name]

class Router:
    def __init__(self, device_name):
        self.device_name = device_name
        self.ip_addresses = {}
        for interface in INTERFACES:
            self.ip_addresses[interface] = name_to_ip[interface]

def create_devices():
    return Host("Host A"), Host("Host B"), Router("Router R1")