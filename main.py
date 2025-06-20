import pyvisa
from SG_test_sequence import run_test_sequence
from utils import slow_print

def main(test_mode=False):
    if test_mode:
        from SG_test_mode import MockInstrument  # ✅ Fix: import from correct file
        slow_print("Running in TEST MODE with mock instrument.")
        instr = MockInstrument()
    else:
        slow_print("Running in LIVE MODE with real instrument.")

        rm = pyvisa.ResourceManager()
        
        # ✅ Replace this with your real IP address or VISA string
        visa_address = "TCPIP0::192.168.1.100::inst0::INSTR"
        
        try:
            instr = rm.open_resource(visa_address)
            slow_print(f"Connected to: {instr.query('*IDN?').strip()}")
        except Exception as e:
            slow_print(f"Connection Failed: {e}")
            return

    slow_print("Starting Test Sequence...\n")

    result = run_test_sequence(instr)

    slow_print("\nTest Sequence Completed.")
    print("Result Dictionary:", result)

    instr.close()
    slow_print("Instrument session closed.")

if __name__ == "__main__":
    main(test_mode=True)  # 🔁 Toggle to False when testing live!
