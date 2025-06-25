from utils import parse_frequency, slow_print

def run_basic_test_sequence(instr):
    results = {}

    slow_print("Resetting instrument to known state...")
    instr.write("*RST")

    while True:
        freq_str = input("Enter the Frequency to be set (e.g., 2GHz, 500kHz, 1.5MHz): ")
        try:
            freq = parse_frequency(freq_str)
            break  # valid, exit loop
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    slow_print(f"Parsed frequency: {freq} Hz")

    while True:
        try:
            power = float(input("Enter the Power to be set (in dBm, between -50 and 0): "))
            if -50 <= power <= 0:
                break
            else:
                slow_print("Power out of range! Please enter a value between -50 and 0 dBm.")
        except ValueError:
            slow_print("Invalid input! Please enter a numeric value.")

    slow_print(f"Setting Frequency to {freq} Hz...")
    instr.write(f"FREQ {freq}")

    slow_print(f"Setting Power to {power} dBm...")
    instr.write(f"POW {power}")

    slow_print("Turning Output ON...")
    instr.write("OUTP ON")

    slow_print("Reading back values from instrument...")
    results['Set Frequency (Hz)'] = instr.query("FREQ?").strip()
    results['Set Power (dBm)'] = instr.query("POW?").strip()

    slow_print("Turning Output OFF...")
    instr.write("OUTP OFF")

    return results