import time
import sys
from openpyxl import Workbook
from datetime import datetime
import os

def export_results_to_excel(result_data, filename_prefix="Test_Result"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append(["Timestamp", timestamp])
    ws.append([])

    # Case 1: If result is a dictionary
    if isinstance(result_data, dict):
        ws.append(["Parameter", "Value"])
        for key, value in result_data.items():
            ws.append([key, value])

    # Case 2: If result is a list
    elif isinstance(result_data, list):
        if all(isinstance(item, dict) for item in result_data):
            # Write headers from keys of first item
            headers = list(result_data[0].keys())  
            ws.append(headers)


            # Write all rows
            for item in result_data:
                ws.append([item.get(h, "") for h in headers])
        else:
            ws.append(["Index", "Value"])
            for idx, item in enumerate(result_data, start=1):
                ws.append([idx, str(item)])  # convert anything else to string

    else:
        ws.append(["Raw Output"])
        ws.append([str(result_data)])

    # Save the file
    filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    export_folder = "results"
    os.makedirs(export_folder, exist_ok=True)
    filepath = os.path.join(export_folder, filename)

    wb.save(filepath)
    print(f"✅ Results exported to Excel: {filepath}")


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

def slow_print(text, delay=0.05, char_delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    print()  # Move to next line after full string
    time.sleep(delay)