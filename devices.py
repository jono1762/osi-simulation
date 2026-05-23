from config import name_to_ip, name_to_mac

class Host:
    def __init__(self, name):
        self.name = name
        self.ip_address = name_to_ip[name]
        self.mac_address = name_to_mac[name]
        self.mac_table = {self.ip_address:self.mac_address}

class Router:
    def __init__(self, name):
        self.name = name
        self.ip_addresses = {"Interface 1": name_to_ip["Interface 1"], "Interface 2": name_to_ip["Interface 2"]}
        self.mac_addresses = {"Interface 1": name_to_mac["Interface 1"], "Interface 2": name_to_mac["Interface 2"]}
        # self.interfaces = []
        # for interface in INTERFACES:
        #     # interface = Interface(interface, name_to_ip[interface], name_to_mac[interface], self)
        #     self.interfaces.append(interface)
        self.mac_table = {}

# class Interface:
#     def __init__(self, name, ip, mac, router):
#         self.mac_address = mac
#         self.ip_address = ip
#         self.name = name
#         self.router = router

def create_devices():
    devices = {"Host A": Host("Host A"), "Host B": Host("Host B"), "Router R1": Router("Router R1")}
    return devices

DEVICES = create_devices()