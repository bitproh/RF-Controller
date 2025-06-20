from test_mode import MockInstrument
from test_sequence import run_test_sequence
from utils import slow_print

def main(test_mode=True):
    if test_mode:
        slow_print("Running in TEST MODE with mock instrument.")
        instr = MockInstrument()
    else:
        slow_print("LIVE MODE not configured in this version.")
        return

    slow_print("Starting Test Sequence...\n")

    result = run_test_sequence(instr)

    slow_print("\nTest Sequence Completed.")
    print("Result Dictionary:", result)

    instr.close()
    slow_print("Instrument session closed.")

if __name__ == "__main__":
    main()