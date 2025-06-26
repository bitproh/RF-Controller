from utils import parse_frequency, slow_print, SLOW_MODE
import datetime
import os
import time

def run_ga_monitor_sequence(sg_instr, sa_instr, sg_name="SignalGenerator", sa_name="SpectrumAnalyzer"):
    results = []

    slow_print("Resetting both instruments to known state...")
    sg_instr.write("*RST")
    sa_instr.write("*RST")

    # -------- Get Frequency and Power Inputs for SG --------
    while True:
        try:
            freq_str = input("Enter Frequency for Signal Generator (e.g., 1GHz): ")
            freq = parse_frequency(freq_str)
            break
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    while True:
        try:
            power = float(input("Enter Power for Signal Generator (in dBm, between -100 and 0): "))
            if -100 <= power <= 0:
                break
            else:
                slow_print("Power out of range! Please enter a value between -100 and 0 dBm.")
        except ValueError:
            slow_print("Invalid input! Please enter a numeric value.")

    # -------- Get Start/Stop, Ref Level, RBW, VBW for SA --------
    while True:
        try:
            start_str = input("Enter Start Frequency for Spectrum Analyzer (e.g., 900MHz): ")
            start_freq = parse_frequency(start_str)
            break
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    while True:
        try:
            stop_str = input("Enter Stop Frequency for Spectrum Analyzer (e.g., 1.1GHz): ")
            stop_freq = parse_frequency(stop_str)
            if stop_freq > start_freq:
                break
            else:
                slow_print("Stop frequency must be greater than start frequency.")
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    while True:
        try:
            ref_level = float(input("Enter Reference Level for Spectrum Analyzer (in dBm, e.g., 0): "))
            break
        except ValueError:
            slow_print("Invalid input! Please enter a numeric value.")

    while True:
        try:
            RBW = input("Enter Resolution Bandwidth for Spectrum Analyzer (e.g., 100kHz): ")
            RBW = parse_frequency(RBW)
            break
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    while True:
        try:
            VBW = input("Enter Video Bandwidth for Spectrum Analyzer (e.g., 10kHz): ")
            VBW = parse_frequency(VBW)
            break
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    # -------- Set Signal Generator --------
    slow_print(f"Setting SG Frequency: {freq} Hz")
    sg_instr.write(f"FREQ {freq}")

    slow_print(f"Setting SG Power: {power} dBm")
    sg_instr.write(f"POW {power}")

    sg_instr.write("OUTP ON")

    # -------- Set Spectrum Analyzer --------
    slow_print(f"Setting SA Start Frequency: {start_freq} Hz")
    sa_instr.write(f"FREQ:STAR {start_freq}")

    slow_print(f"Setting SA Stop Frequency: {stop_freq} Hz")
    sa_instr.write(f"FREQ:STOP {stop_freq}")

    slow_print(f"Setting SA Reference Level: {ref_level} dBm")
    sa_instr.write(f"DISP:WIND:TRAC:Y:RLEV {ref_level}")

    slow_print(f"Setting SA RBW: {RBW} Hz")
    sa_instr.write(f"BAND {RBW}")

    slow_print(f"Setting SA VBW: {VBW} Hz")
    sa_instr.write(f"BAND:VID {VBW}")

    # -------- Start Sweep and Wait for Completion --------
    slow_print("Starting sweep on Spectrum Analyzer...")
    sa_instr.write("INIT:IMM")
    sa_instr.write("*WAI")  # Wait for sweep to complete
    sa_instr.query("*OPC?")  # Wait for sweep to complete

    # -------- Marker Peak Search --------
    slow_print("Activating Marker at peak location on SA...")
    sa_instr.write("CALC:MARK1 ON")
    sa_instr.write("CALC:MARK1:MAX")

    # -------- Query Outputs --------
    sg_set_freq = sg_instr.query("FREQ?").strip()
    sg_set_power = sg_instr.query("POW?").strip()

    peak_freq = sa_instr.query("CALC:MARK1:X?").strip()
    peak_power = sa_instr.query("CALC:MARK1:Y?").strip()

    results.append({
        'SG Frequency (Hz)': sg_set_freq,
        'SG Power (dBm)': sg_set_power,
        'SA Start Frequency (Hz)': start_freq,
        'SA Stop Frequency (Hz)': stop_freq,
        'SA Reference Level (dBm)': ref_level,
        'SA RBW (Hz)': RBW,
        'SA VBW (Hz)': VBW,
        'Marker Frequency (Hz)': peak_freq,
        'Marker Power (dBm)': peak_power
    })

    slow_print(f"Signal Generator Set Frequency: {sg_set_freq} Hz")
    slow_print(f"Signal Generator Set Power: {sg_set_power} dBm")
    slow_print(f"Spectrum Analyzer Marker Frequency: {peak_freq} Hz")
    slow_print(f"Spectrum Analyzer Marker Power: {peak_power} dBm")

    # -------- Screenshot Section --------
    save_to_instr = input("Do you want to save the screenshot to your Instrument? (y/n): ").strip().lower()
    if save_to_instr == "y":
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_on_instr = r"D:\GA monitor"
        filename = f"{sa_name}_{now}.png"
        full_instr_path = f"{folder_on_instr}\\{filename}"
        sa_instr.write(f':MMEM:STOR:SCR "{full_instr_path}"')
        slow_print(f"Screenshot saved as {full_instr_path} on instrument.")

        save_to_pc = input("Do you want to save the screenshot to your PC? (y/n): ").strip().lower()
        if save_to_pc == "y":
            # Create folder if it doesn't exist
            save_folder = r"D:\GA monitor"
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, filename)

            slow_print("Transferring screenshot to PC...")
            screenshot_data = sa_instr.query_binary_values(f':MMEM:DATA? "{full_instr_path}"', datatype='B')
            with open(save_path, "wb") as f:
                f.write(bytearray(screenshot_data))
            slow_print(f"Screenshot saved as {save_path} on your PC.")

    # -------- Ask to Reset Parameters --------
    reset_params = input("Do you want to reset the instrument parameters? (y/n): ").strip().lower()
    if reset_params == "y":
        sg_instr.write("*RST")
        sa_instr.write("*RST")
        slow_print("Both instrument parameters have been reset.")

    sg_instr.write("OUTP OFF")
    return results
