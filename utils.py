import time
import sys
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os
from openpyxl.utils.exceptions import InvalidFileException

def export_results_to_excel(result_data, filename_prefix="Test_Result"):
    export_folder = "results"
    os.makedirs(export_folder, exist_ok=True)

    # File path (one file per day)
    today_str = datetime.now().strftime('%Y%m%d')
    filename = f"{filename_prefix}_{today_str}.xlsx"
    filepath = os.path.join(export_folder, filename)

    # Try to load existing workbook, or create new one
    try:
        if os.path.exists(filepath):
            wb = load_workbook(filepath)
            ws = wb.active
        else:
            wb = Workbook()
            ws = wb.active
            ws.title = "Results"
    except InvalidFileException:
        wb = Workbook()
        ws = wb.active
        ws.title = "Results"

    # Add timestamp section
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append([])  # empty row for spacing
    ws.append(["Timestamp", timestamp])
    ws.append([])

    # Case 1: Dictionary
    if isinstance(result_data, dict):
        ws.append(["Parameter", "Value"])
        for key, value in result_data.items():
            ws.append([key, value])

    # Case 2: List of dictionaries
    elif isinstance(result_data, list):
        if all(isinstance(item, dict) for item in result_data):
            headers = list(result_data[0].keys())
            ws.append(headers)
            for item in result_data:
                ws.append([item.get(h, "") for h in headers])
        else:
            ws.append(["Index", "Value"])
            for idx, item in enumerate(result_data, start=1):
                ws.append([idx, str(item)])

    # Fallback case
    else:
        ws.append(["Raw Output"])
        ws.append([str(result_data)])

    # Save the updated file
    wb.save(filepath)
    print(f"✅ Results appended to Excel: {filepath}")


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

SLOW_MODE = True # 🔁 Toggle this to False for instant printing

def slow_print(text, delay=0.05, char_delay=0.05):
    if not SLOW_MODE:
        print(text)
        return

    for char in text:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    print()
    time.sleep(delay)