from utils import parse_frequency, slow_print,SLOW_MODE

def run_test_sequence(instr):
    results = []

    slow_print("Resetting instrument to known state...")
    instr.write("*RST")

    # -------- Get Frequency Sweep Inputs --------
    while True:
        try:
            start_freq_str = input("Enter Start Frequency (e.g., 2GHz): ")
            start_freq = parse_frequency(start_freq_str)

            stop_freq_str = input("Enter Stop Frequency (e.g., 3GHz): ")
            stop_freq = parse_frequency(stop_freq_str)

            step_freq_str = input("Enter Frequency Step (e.g., 100MHz): ")
            step_freq = parse_frequency(step_freq_str)

            if stop_freq <= start_freq:
                slow_print("Stop frequency must be greater than start frequency.")
                continue

            break
        except ValueError as e:
            slow_print(f"Error: {e}. Please try again.")

    # -------- Get Power Input --------
    while True:
        try:
            power = float(input("Enter Power (in dBm, between -50 and 0): "))
            if -50 <= power <= 0:
                break
            else:
                slow_print("Power out of range! Please enter a value between -50 and 0 dBm.")
        except ValueError:
            slow_print("Invalid input! Please enter a numeric value.")

    slow_print(f"Beginning frequency sweep from {start_freq} Hz to {stop_freq} Hz...")

    # -------- Frequency Sweep Loop --------
    current_freq = start_freq
    while current_freq <= stop_freq:
        slow_print(f"Setting Frequency: {current_freq} Hz")
        instr.write(f"FREQ {current_freq}")

        slow_print(f"Setting Power: {power} dBm")
        instr.write(f"POW {power}")

        instr.write("OUTP ON")

        # Query values
        set_freq = instr.query("FREQ?").strip()
        set_power = instr.query("POW?").strip()

        results.append({
            'Frequency (Hz)': set_freq,
            'Power (dBm)': set_power
        })

        #save screenshot to device
        save_to_pc = input("Do you want to save a screenshot to the PC? (yes/no): ").strip().lower()
        if save_to_pc == 'yes':
            import datetime, os
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_on_instr = r"D:\GA monitor"
            filename = f"SG_screen_{now}.png"
            full_instr_path = f"{folder_on_instr}\\{filename}"

            # Save screenshot to instrument memory
            instr.write(f"MMEM:NAME '{full_instr_path}'")
            # Transfer screenshot to PC
            os.makedirs(folder_on_instr, exist_ok=True)
            screenshot_data = instr.query_binary_values(f"MMEM:DATA? '{full_instr_path}'", datatype='B')
            save_path = os.path.join(folder_on_instr, filename)
            with open(save_path, "wb") as f:
                f.write(bytearray(screenshot_data))
            slow_print(f"Screenshot saved as {save_path} on your PC.")

        
            
            

        instr.write("OUTP OFF")
        current_freq += step_freq

    return results