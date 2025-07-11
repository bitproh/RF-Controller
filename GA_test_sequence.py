from utils import parse_frequency, slow_print, SLOW_MODE, save_screenshot
import datetime
import os
import time

def run_ga_monitor_sequence(sg_instr, sa_instr, sg_name="SignalGenerator", sa_name="SpectrumAnalyzer"):
    results = []

    # Helper input function to allow quitting with 'q'
    def user_input(prompt):
        val = input(prompt).strip()
        if val.lower() == "q":
            slow_print("Quitting sequence.")
            raise KeyboardInterrupt
        return val

    # Initial parameter input
    def get_sg_params():
        while True:
            try:
                freq_str = user_input("Enter Frequency for Signal Generator (e.g., 1GHz) [q to quit]: ")
                freq = parse_frequency(freq_str)
                break
            except ValueError as e:
                slow_print(f"Error: {e}. Please try again.")
        while True:
            try:
                power_str = user_input("Enter Power for Signal Generator (in dBm, between -100 and 0) [q to quit]: ")
                power = float(power_str)
                if -100 <= power <= 0:
                    break
                else:
                    slow_print("Power out of range! Please enter a value between -100 and 0 dBm.")
            except ValueError:
                slow_print("Invalid input! Please enter a numeric value.")
        while True:
            rf_state = user_input("Should RF output be ON or OFF? (on/off/q): ").lower()
            if rf_state == "q":
                slow_print("Quitting sequence.")
                raise KeyboardInterrupt
            if rf_state in ["on", "off"]:
                break
            else:
                slow_print("Please enter 'on' or 'off'.")
        return freq, power, rf_state


    def get_sa_params():
        while True:
            try:
                start_str = user_input("Enter Start Frequency for Spectrum Analyzer (e.g., 900MHz) [q to quit]: ")
                start_freq = parse_frequency(start_str)
                break
            except ValueError as e:
                slow_print(f"Error: {e}. Please try again.")
        while True:
            try:
                stop_str = user_input("Enter Stop Frequency for Spectrum Analyzer (e.g., 1.1GHz) [q to quit]: ")
                stop_freq = parse_frequency(stop_str)
                if stop_freq > start_freq:
                    break
                else:
                    slow_print("Stop frequency must be greater than start frequency.")
            except ValueError as e:
                slow_print(f"Error: {e}. Please try again.")
        while True:
            try:
                ref_level_str = user_input("Enter Reference Level for Spectrum Analyzer (in dBm, e.g., 0) [q to quit]: ")
                ref_level = float(ref_level_str)
                break
            except ValueError:
                slow_print("Invalid input! Please enter a numeric value.")
        while True:
            try:
                RBW_str = user_input("Enter Resolution Bandwidth for Spectrum Analyzer (e.g., 100kHz) [q to quit]: ")
                RBW = parse_frequency(RBW_str)
                break
            except ValueError as e:
                slow_print(f"Error: {e}. Please try again.")
        while True:
            try:
                VBW_str = user_input("Enter Video Bandwidth for Spectrum Analyzer (e.g., 10kHz) [q to quit]: ")
                VBW = parse_frequency(VBW_str)
                break
            except ValueError as e:
                slow_print(f"Error: {e}. Please try again.")
        return start_freq, stop_freq, ref_level, RBW, VBW

    try:
        # Get initial parameters
        freq, power = get_sg_params()
        start_freq, stop_freq, ref_level, RBW, VBW = get_sa_params()

        while True:
            slow_print("Resetting both instruments to known state...")
            sg_instr.write("*RST")
            sa_instr.write("*RST")

            # Set SG
            slow_print(f"Setting SG Frequency: {freq} Hz")
            sg_instr.write(f"FREQ {freq}")
            slow_print(f"Setting SG Power: {power} dBm")
            sg_instr.write(f"POW {power}")
            sg_instr.write("OUTP ON")

            # Set SA
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

            # Sweep and marker
            slow_print("Starting sweep on Spectrum Analyzer...")
            sa_instr.write("INIT:IMM")
            sa_instr.write("*WAI")
            sa_instr.query("*OPC?")
            slow_print("Activating Marker at peak location on SA...")
            sa_instr.write("CALC:MARK1 ON")
            sa_instr.write("CALC:MARK1:MAX")

            # Query outputs
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
                'Marker Power (dBm)': peak_power,
                'Offset Frequency (Hz)': float(peak_freq) - float(sg_set_freq),
                'Offset Power (dBm)': float(peak_power) - float(sg_set_power)
            })

            slow_print(f"Signal Generator Set Frequency: {sg_set_freq} Hz")
            slow_print(f"Signal Generator Set Power: {sg_set_power} dBm")
            slow_print(f"Spectrum Analyzer Marker Frequency: {peak_freq} Hz")
            slow_print(f"Spectrum Analyzer Marker Power: {peak_power} dBm")
            slow_print(f"Offset Frequency: {float(peak_freq) - float(sg_set_freq)} Hz")
            slow_print(f"Offset Power: {float(peak_power) - float(sg_set_power)} dBm")
            # Screenshot Section
            save_to_instr = user_input("Do you want to save the screenshot to your Instrument? (y/n/q): ").lower()
            if save_to_instr == "q":
                break
            if save_to_instr == "y":
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                folder_on_instr = r"D:\GA monitor"
                filename = f"{sa_name}_{now}.png"
                full_instr_path = f"{folder_on_instr}\\{filename}"
                sa_instr.write(f':MMEM:STOR:SCR "{full_instr_path}"')
                slow_print(f"Screenshot saved as {full_instr_path} on instrument.")

                save_to_pc = user_input("Do you want to save the screenshot to your PC? (y/n/q): ").lower()
                if save_to_pc == "q":
                    break
                if save_to_pc == "y":
                    save_folder = r"D:\GA monitor"
                    os.makedirs(save_folder, exist_ok=True)
                    save_path = os.path.join(save_folder, filename)
                    slow_print("Transferring screenshot to PC...")
                    screenshot_data = sa_instr.query_binary_values(f':MMEM:DATA? "{full_instr_path}"', datatype='B')
                    with open(save_path, "wb") as f:
                        f.write(bytearray(screenshot_data))
                    slow_print(f"Screenshot saved as {save_path} on your PC.")

            sg_instr.write("OUTP OFF")

            # Ask if user wants to change SG parameters
            change_sg = user_input("Do you want to change the Signal Generator parameters? (y/n/q): ").lower()
            if change_sg == "q":
                break
            if change_sg == "y":
                freq, power = get_sg_params()
            # Ask if user wants to change SA parameters
            change_sa = user_input("Do you want to change the Spectrum Analyzer parameters? (y/n/q): ").lower()
            if change_sa == "q":
                break
            if change_sa == "y":
                start_freq, stop_freq, ref_level, RBW, VBW = get_sa_params()
            # If neither, break the loop
            if change_sg != "y" and change_sa != "y":
                break

    except KeyboardInterrupt:
        slow_print("Exited sequence by user request.")

    return results
