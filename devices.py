from config import name_to_ip, name_to_mac, INTERFACES

class Host:
    def __init__(self, name):
        self.name = name
        self.ip_address = name_to_ip[name]
        self.mac_address = name_to_mac[name]
        self.mac_table = {self.ip_address:self.mac_address}

class Router:
    def __init__(self, name):
        self.name = name
        self.interfaces = {}
        for interface in INTERFACES:
            self.interfaces[interface] = Interface(interface, self, name_to_ip[interface], name_to_mac[interface])
        self.mac_table = {}

class Interface:
    def __init__(self, name, router, ip, mac):
        self.name = name
        self.router = router
        self.ip_address = ip
        self.mac_address = mac

def create_devices():
    devices = {"Host A": Host("Host A"), "Host B": Host("Host B"), "Router R1": Router("Router R1")}
    return devices

DEVICES = create_devices()