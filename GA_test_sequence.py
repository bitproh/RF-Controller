from utils import parse_frequency, slow_print
import time

def run_sg_sa_sequence(sg_instr, sa_instr):
    results = {}

    slow_print("Resetting both instruments to known state...")
    sg_instr.write("*RST")
    sa_instr.write("*RST")

    # --- Frequency Input ---
    while True:
        freq_str = input("Enter Frequency for both SG and SA (e.g., 1GHz, 500kHz): ")
        try:
            freq = parse_frequency(freq_str)
            break
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    # --- Power Input for SG ---
    while True:
        try:
            power = float(input("Enter Power for Signal Generator (in dBm, between -50 and 0): "))
            if -50 <= power <= 0:
                break
            else:
                slow_print("Power out of range! Please enter a value between -50 and 0 dBm.")
        except ValueError:
            slow_print("Invalid input! Please enter a numeric value.")

    # --- Span Input for SA ---
    while True:
        span_str = input("Enter Span for Spectrum Analyzer (e.g., 10MHz, 5kHz): ")
        try:
            span = parse_frequency(span_str)
            break
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    # --- Set Signal Generator ---
    slow_print(f"Setting SG Frequency to {freq} Hz...")
    sg_instr.write(f"FREQ {freq}")

    slow_print(f"Setting SG Power to {power} dBm...")
    sg_instr.write(f"POW {power}")

    slow_print("Turning SG Output ON...")
    sg_instr.write("OUTP ON")

    # --- Set Spectrum Analyzer ---
    slow_print(f"Setting SA Center Frequency to {freq} Hz...")
    sa_instr.write(f"FREQ:CENT {freq}")

    slow_print(f"Setting SA Span to {span} Hz...")
    sa_instr.write(f"FREQ:SPAN {span}")

    # --- Marker Peak Search on SA ---
    slow_print("Activating Marker at peak location on SA...")
    sa_instr.write("CALC:MARK1 ON")
    sa_instr.write("CALC:MARK1:MAX")
    time.sleep(0.5)  # Wait for peak capture

    peak_freq = sa_instr.query("CALC:MARK1:X?").strip()
    peak_power = sa_instr.query("CALC:MARK1:Y?").strip()

    results["Set Frequency (Hz)"] = freq
    results["Set Power (dBm)"] = power
    results["SA Span (Hz)"] = span
    results["Marker Frequency (Hz)"] = peak_freq
    results["Marker Power (dBm)"] = peak_power

    slow_print(f"Peak Frequency on SA: {peak_freq} Hz")
    slow_print(f"Peak Power on SA: {peak_power} dBm")

    slow_print("Turning SG Output OFF...")
    sg_instr.write("OUTP OFF")

    return results