from utils import parse_frequency, slow_print

def run_test_sequence(instr):
    results = []

    slow_print("Resetting analyzer to known state...")
    instr.write("*RST")

    # -------- Get Center Frequency and Span Inputs --------
    while True:
        try:
            center_freq_str = input("Enter Center Frequency (e.g., 1GHz): ")
            center_freq = parse_frequency(center_freq_str)

            span_str = input("Enter Span (e.g., 10MHz): ")
            span = parse_frequency(span_str)

            break
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    # -------- Get Reference Level Input --------
    while True:
        try:
            ref_level = float(input("Enter Reference Level (in dBm, e.g., 0): "))
            break
        except ValueError:
            slow_print("Invalid input! Please enter a numeric value.")

    slow_print(f"Setting Center Frequency: {center_freq} Hz")
    instr.write(f"FREQ:CENT {center_freq}")

    slow_print(f"Setting Span: {span} Hz")
    instr.write(f"FREQ:SPAN {span}")

    slow_print(f"Setting Reference Level: {ref_level} dBm")
    instr.write(f"DISP:WIND:TRAC:Y:RLEV {ref_level}")

    # -------- Marker Peak Search --------
    slow_print("Activating Marker at peak location...")
    instr.write("CALC:MARK1 ON")
    instr.write("CALC:MARK1:MAX")

    # Query marker values
    peak_freq = instr.query("CALC:MARK1:X?").strip()
    peak_power = instr.query("CALC:MARK1:Y?").strip()

    results.append({
        'Marker Frequency (Hz)': peak_freq,
        'Marker Power (dBm)': peak_power
    })

    slow_print(f"Peak Frequency: {peak_freq} Hz")
    slow_print(f"Peak Power: {peak_power} dBm")

    return results