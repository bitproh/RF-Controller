RF_devices = [
    {
        "identity": "Signal_Generator",
        "visa_resource": "TCPIP0::192.168.1.10::inst0::INSTR",
        "ip_address": "192.168.1.10"
    },
    {
        "identity": "Spectrum_Analyzer",
        "visa_resource": "TCPIP0::192.168.1.11::inst0::INSTR",
        "ip_address": "192.168.1.11"
    },
    {
        "identity": "Signal_Analyzer",
        "visa_resource": "TCPIP0::192.168.1.12::inst0::INSTR",
        "ip_address": "192.168.1.12"
    }
]

search_identity = input("Enter device identity: ")
search_resource = input("Enter VISA resource: ")
search_ip = input("Enter IP address: ")


# Exact match on all three
results = [
    device for device in RF_devices
    if device["identity"] == search_identity and
       device["visa_resource"] == search_resource and
       device["ip_address"] == search_ip
]

if results:
    print("Matching device(s):")
    for device in results:
        print(f"Identity      : {device['identity']}")
        print(f"Resource Name : {device['visa_resource']}")
        print(f"IP Address    : {device['ip_address']}")
        print()  # Add a blank line between devices
else:
    print("No matching devices found.")
