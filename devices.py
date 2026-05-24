from config import name_to_ip, name_to_mac, INTERFACES

class Host:
    '''
    Define blueprint for Host A and Host B respectively.
    '''
    def __init__(self, name):
        self.name = name
        self.ip_address = name_to_ip[name]
        self.mac_address = name_to_mac[name]
        self.mac_table = {self.ip_address:self.mac_address}

class Router:
    '''
    Define blueprint for Router R1, with access to its interfaces, Interface 1
    and Interface 2 through a parent-child relationship.
    '''
    def __init__(self, name):
        self.name = name
        self.interfaces = {}
        for interface in INTERFACES:
            self.interfaces[interface] = Interface(interface, self, name_to_ip[interface], name_to_mac[interface])
        self.mac_table = {}

class Interface:
    '''
    Define blueprint for Interface 1 and Interface 2, associating it with its
    parent router, Router R1.
    '''
    def __init__(self, name, router, ip, mac):
        self.name = name
        self.router = router
        self.ip_address = ip
        self.mac_address = mac

def create_devices():
    '''
    Specifies the devices defined above for use in the simulation.
    '''
    devices = {"Host A": Host("Host A"), "Host B": Host("Host B"), "Router R1": Router("Router R1")}
    return devices

# Instantiates the specified devices needed for the simulation
DEVICES = create_devices()