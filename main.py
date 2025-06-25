import pyvisa
#from SG_test_sequence import run_test_sequence
from SG_basic_sequence import run_basic_test_sequence
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
        visa_address = "TCPIP0::169.254.167.6::inst0::INSTR"
        
        try:
            instr = rm.open_resource(visa_address)
            slow_print(f"Connected to: {instr.query('*IDN?').strip()}")
        except Exception as e:
            slow_print(f"Connection Failed: {e}")
            return

    slow_print("Starting Test Sequence...\n")

    #result = run_test_sequence(instr)
    result = run_basic_test_sequence(instr)

    slow_print("\nTest Sequence Completed.")
    print("Result Dictionary:", result)

    instr.close()
    slow_print("Instrument session closed.")

if __name__ == "__main__":
    main(test_mode=False)  # 🔁 Toggle to False when testing live!