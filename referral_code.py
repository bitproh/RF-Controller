#connection to the device. 
#how the device is connected to the computer, such as via USB, Ethernet, or GPIB.
# This script generates a referral code based on user input for identity, VISA resource, and IP address.
import pyvisa

rm = pyvisa.ResourceManager()

# List all VISA devices connected
resources = rm.list_resources()
print("Connected VISA devices:")
for res in resources:
    print(f" - {res}")

# Variables to hold devices
siggen = None
specan = None

# Search and assign based on IDN response
for res in resources:
    try:
        dev = rm.open_resource(res)
        idn = dev.query("*IDN?").strip()
        print(f"{res} → {idn}")

        if "E8257D" in idn:
            siggen = dev
            print("→ Signal Generator found and assigned.")
        elif "N9010B" in idn:
            specan = dev
            print("→ Spectrum Analyzer found and assigned.")
    except Exception as e:
        print(f"Error with {res}: {e}")

# Check status
if siggen:
    print("\n✅ Signal Generator ready.")
else:
    print("\n❌ Signal Generator not found.")

if specan:
    print("✅ Spectrum Analyzer ready.")
else:
    print("❌ Spectrum Analyzer not found.")
