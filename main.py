import pyvisa
from utils import slow_print


rm = pyvisa.ResourceManager()
def main(test_mode=False):
    slow_print("Welcome to the RF Test Automation Suite!")
    
          
    slow_print("Please select the instrument to test:")
    slow_print("[1] Signal Generator")
    slow_print("[2] Spectrum Analyzer")

    choice = input("Enter your choice (1 or 2): ").strip()

    # --------------------------
    # Signal Generator Selected
    # --------------------------
    if choice == "1":
        if test_mode:
            from SG_test_mode import MockInstrument
            from SG_test_sequence import run_test_sequence
            slow_print("Running SIGNAL GENERATOR in TEST MODE.")
            instr = MockInstrument()
        else:
            from SG_test_sequence import run_test_sequence
            slow_print("Running SIGNAL GENERATOR in LIVE MODE.")
            rm = pyvisa.ResourceManager()
            visa_address = "TCPIP0::169.254.167.6::inst0::INSTR"  # 👈 Replace with actual SG IP
            try:
                instr = rm.open_resource(visa_address)
                slow_print(f"Connected to: {instr.query('*IDN?').strip()}")
            except Exception as e:
                slow_print(f"Connection Failed: {e}")
                return

        slow_print("Starting Signal Generator Test Sequence...\n")
        result = run_test_sequence(instr)

    # -------------------------------
    # Spectrum Analyzer Selected
    # -------------------------------

    elif choice == "2":
        if test_mode:
            from SA_test_mode import MockInstrument
            from SA_basic_sequence import run_spectrum_analysis
            slow_print("Running SPECTRUM ANALYZER in TEST MODE.")
            instr = MockInstrument()
        else:
            from SA_basic_sequence import run_basic_analyzer_sequence
            slow_print("Running SPECTRUM ANALYZER in LIVE MODE.")
            rm = pyvisa.ResourceManager()
            visa_address = "USB0::0x2A8D::0x5D0C::MY12345678::INSTR"  # 👈 Replace with actual SA VISA
            try:
                instr = rm.open_resource(visa_address)
                slow_print(f"Connected to: {instr.query('*IDN?').strip()}")
            except Exception as e:
                slow_print(f"Connection Failed: {e}")
                return

        slow_print("Starting Spectrum Analyzer Test Sequence...\n")
        result = run_basic_analyzer_sequence(instr)

    else:
        slow_print("Invalid choice! Exiting program.")
        return

    slow_print("\nTest Sequence Completed.")
    print("Result Dictionary:", result)

    instr.close()
    slow_print("Instrument session closed.")

if __name__ == "__main__":
    main(test_mode=True)  # 🔁 Toggle to False for live mode
