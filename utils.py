import time
import sys

def parse_frequency(freq_input):
    freq_input = freq_input.strip().lower().replace(" ", "")  # e.g., '1GHz' → '1ghz'

    multipliers = {
        'ghz': 1e9,
        'mhz': 1e6,
        'khz': 1e3,
        'hz': 1,
    }

    for unit in multipliers:
        if freq_input.endswith(unit):
            try:
                value = float(freq_input.replace(unit, ""))
                return value * multipliers[unit]
            except ValueError:
                raise ValueError("Invalid numeric value in frequency input.")

    # If no unit is provided, assume Hz
    try:
        return float(freq_input)
    except ValueError:
        raise ValueError("Frequency format not recognized.")

#fucntion for printing values with delay

def slow_print(text, delay=0.05, char_delay=0.06):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    print()  # Move to next line after full string
    time.sleep(delay)
