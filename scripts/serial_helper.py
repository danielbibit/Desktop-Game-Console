import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    print("\nport: {}\n \tdesc: {}\n \thwid: {}".format(port, desc, hwid))
    print(hwid)
