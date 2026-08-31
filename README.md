# CITS3002-Project
## Instructions to Run
To run the program, open the terminal and use the command:

```python main.py [IntValue]```

[IntValue] indicates the size of the message from the application layer in bytes. If this size exceeds 500 bytes, the message will be segmented.

## Implementation Overview
### main.py
- Outlines the control flow of the application.
- Inputs an integer argument corresponding to the application message size.
- Creates a `Data` object containing the application message.
- Passes the object into the `TransportLayer` of `Host A` which results in transmission of the message between the hosts.

### config.py
- Outlines the hard-coded information of the application.
- Contains all host and interface MAC and IP addresses, encoded into binary format.
- Generates routing table which gives the IP address for an outgoing link to reach a particular host.

### devices.py
- Outlines the devices used in the application.
- Defines each of the device classes: host, router and interface.
- Creates instances of them to generate sample network that can perform simulation on.

### protocol.py
- Outlines the core logic in the application.
- Defines each of the network layers: `DataLinkLayer`, `NetworkLayer` and `TransportLayer`.
- Defines each of the data types used on each layer: `Frame`, `Packet` and `Segment` in addition to `Data`.
