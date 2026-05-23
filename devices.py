from config import name_to_ip, name_to_mac, INTERFACES

class Host:
    def __init__(self, device_name):
        self.device_name = device_name
        self.ip_address = name_to_ip[device_name]
        self.mac_address = name_to_mac[device_name]
        self.mac_table = {self.device_name:self.mac_address}

class Router:
    def __init__(self, device_name):
        self.device_name = device_name
        self.interfaces = []
        for interface in INTERFACES:
            interface = Interface(interface, name_to_ip[interface], name_to_mac[interface])
        self.mac_table = {}

class Interface:
    def __init__(self, name, ip, mac):
        self.mac_address = mac
        self.ip_address = ip
        self.name = name

def create_devices():
    return Host("Host A",), Host("Host B"), Router("Router R1")