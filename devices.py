<<<<<<< HEAD
class Device:
    return 

class Router:
    return 
=======
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
>>>>>>> b195b71bd710017543b05c96a8c0e0f99139e4e3
