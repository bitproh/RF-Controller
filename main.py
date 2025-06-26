import pyvisa
from utils import slow_print, export_results_to_excel, SLOW_MODE
slow_print("Welcome to the RF Test Automation Suite!")
# ✅ List your known instruments (Signal Generator and Spectrum Analyzer)
known_instruments = {
    "Signal Generator": "TCPIP0::169.254.167.6::inst0::INSTR",
    "Spectrum Analyzer2": "USB0::0x2A8D::0x5D0C::MY12345678::INSTR",
    "Spectrum Analyzer" : "USB0::0x2A8D::0x1B0B::MY63440324::0::INSTR"

}

# ✅ Function to check and return only connected instruments
def check_connected_instruments():
    slow_print("🔍 Checking connected instruments...")
    rm = pyvisa.ResourceManager()
    connected = {}

    for name, addr in known_instruments.items():
        try:
            instr = rm.open_resource(addr)
            idn = instr.query("*IDN?").strip()
            print(f"✅ {name} connected: {idn}")
            connected[name] = (addr, idn)
            instr.close()
        except Exception as e:
            print(f"❌ {name} NOT connected. Error: {e}")

    return connected


def main(test_mode=False):
    # ✅ Check connected instruments first
    connected_devices = check_connected_instruments()

    
    
          
    slow_print("Please select the instrument to test:")
    slow_print("[1] Signal Generator")
    slow_print("[2] Spectrum Analyzer")

    choice = input("Enter your choice (1 or 2): ").strip()

    # --------------------------
    # Signal Generator Selected
    # --------------------------
    if choice == "1":
        name = "Signal Generator"
        if test_mode:
            from SG_test_mode import MockInstrument
            from SG_test_sequence import run_test_sequence
            #from SG_basic_sequence import run_basic_test_sequence

            slow_print("Running SIGNAL GENERATOR in TEST MODE.")
            instr = MockInstrument()
        else:
            if name not in connected_devices:
                slow_print(f"{name} is not connected. Exiting.")
                return

            from SG_test_sequence import run_test_sequence
            #from SG_basic_sequence import run_basic_test_sequence
            slow_print("Running SIGNAL GENERATOR in LIVE MODE.")
            rm = pyvisa.ResourceManager()
            visa_address = connected_devices[name][0]  # Get address from check
            try:
                instr = rm.open_resource(visa_address)
                slow_print(f"Connected to: {instr.query('*IDN?').strip()}")
            except Exception as e:
                slow_print(f"Connection Failed: {e}")
                return

        slow_print("Starting Signal Generator Test Sequence...\n")
        result = run_test_sequence(instr)
        #result = run_basic_test_sequence(instr)

    # -------------------------------
    # Spectrum Analyzer Selected
    # -------------------------------
    
    elif choice == "2":
        name = "Spectrum Analyzer"
        if test_mode:
            from SA_test_mode import MockInstrument
            #from SA_basic_sequence import run_spectrum_analysis
            from SA_test_sequence import run_test_sequence
            slow_print("Running SPECTRUM ANALYZER in TEST MODE.")
            instr = MockInstrument()
        else:
            if name not in connected_devices:
                slow_print(f"{name} is not connected. Exiting.")
                return

            #from SA_basic_sequence import run_spectrum_analysis
            from SA_test_sequence import run_test_sequence
            slow_print("Running SPECTRUM ANALYZER in LIVE MODE.")
            rm = pyvisa.ResourceManager()
            visa_address = connected_devices[name][0]  # Get address from check
            try:
                instr = rm.open_resource(visa_address)
                slow_print(f"Connected to: {instr.query('*IDN?').strip()}")
            except Exception as e:
                slow_print(f"Connection Failed: {e}")
                return

        slow_print("Starting Spectrum Analyzer Test Sequence...\n")
        #result = run_spectrum_analysis(instr)
        result = run_test_sequence(instr)

    else:
        slow_print("Invalid choice! Exiting program.")
        return

    slow_print("\nTest Sequence Completed.")
    print("Result Dictionary:", result)
    export_results_to_excel(result, filename_prefix=name.replace(" ", "_"))

    instr.close()
    slow_print("Instrument session closed.")


if __name__ == "__main__":
    main(test_mode=False)  # 🔁 Toggle to False for live mode
