from utils import parse_frequency, slow_print
import time

def run_spectrum_analysis(instr):
    results = {}

    slow_print("Resetting analyzer to known state...")
    instr.write("*RST")

    
    while True:
        freq_str = input("Enter Center Frequency (e.g., 1GHz, 500kHz): ")
        try:
            center_freq = parse_frequency(freq_str)
            break
        except ValueError as e:
            slow_print(f" Error: {e}. Try again.")

    while True:
        span_str = input("Enter Span (e.g., 10MHz, 5kHz): ")
        try:
            span = parse_frequency(span_str)
            break
        except ValueError as e:
            slow_print(f" Error: {e}. Try again.")

   
    slow_print(f"Setting Center Frequency: {center_freq} Hz")
    instr.write(f"FREQ:CENT {center_freq}")

    slow_print(f"Setting Span: {span} Hz")
    instr.write(f"FREQ:SPAN {span}")

  

    slow_print("Activating Marker at peak location...")
    instr.write("CALC:MARK1 ON")
    instr.write("CALC:MARK1:MAX")
    time.sleep(0.5)  # Wait for peak capture

    peak_freq = instr.query("CALC:MARK1:X?").strip()
    peak_power = instr.query("CALC:MARK1:Y?").strip()

    results["Marker Frequency (Hz)"] = peak_freq
    results["Marker Power (dBm)"] = peak_power

    slow_print(f" Peak Frequency: {peak_freq} Hz")
    slow_print(f" Peak Power: {peak_power} dBm")

    return results
