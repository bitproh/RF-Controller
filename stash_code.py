#this code has no conection with the actual working og the device,
#this code is just for debugging and testing purposes.
#person on use: Asif Muhammmad
# first appproach testing
# still on use, dont change.

# simple_siggen.py

import pyvisa
import time

rm = pyvisa.ResourceManager()
print("Resources:", rm.list_resources())

# Replace with your actual VISA address
sig = rm.open_resource(rm.list_resources()[0])  # assumes first device is your sig-gen

print("IDN:", sig.query("*IDN?").strip())

def set_freq(freq_hz):
    sig.write(f"FREQ {freq_hz}")
    print("Frequency:", sig.query("FREQ?").strip())

def set_power(p_dbm):
    sig.write(f"POW {p_dbm}")
    print("Power:", sig.query("POW?").strip())

def output(on=True):
    sig.write(f"OUTP {'ON' if on else 'OFF'}")
    print("Output is", "ON" if on else "OFF")

def sweep(start_hz, stop_hz, step_hz=1e6):
    set_freq(start_hz)
    sig.write("SWE:TYPE STEP")
    sig.write(f"FREQ:START {start_hz}")
    sig.write(f"FREQ:STOP {stop_hz}")
    sig.write(f"FREQ:STEP {step_hz}")
    sig.write("SWE:STAT ON")
    sig.write("TRIG:SOUR IMM")
    sig.write("INIT:IMM")
    print(f"Sweeping {start_hz}→{stop_hz} Hz in steps of {step_hz} Hz")

# Example usage
set_freq(1e9)
set_power(-10)
output(True)
time.sleep(1)
sweep(1e9, 1.1e9, 10e6)
time.sleep(2)
output(False)
