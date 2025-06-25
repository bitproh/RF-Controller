import pyvisa

known_instruments = [
    "TCPIP0::169.254.167.6::inst0::INSTR",
    "USB0::0x2A8D::0x1D0B::MY62282097::0::INSTR"
]

rm = pyvisa.ResourceManager()

<<<<<<< HEAD
# Replace with your actual VISA address
'''sig = rm.open_resource(rm.list_resources()[0])  # assumes first device is your sig-gen

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
'''
=======
for addr in known_instruments:
    try:
        instr = rm.open_resource(addr)
        idn = instr.query("*IDN?")
        print(f"✅ {addr} connected. IDN: {idn.strip()}")
        instr.close()
    except Exception as e:
        print(f"❌ {addr} NOT connected or unreachable. Error: {e}")
>>>>>>> 2baf7791e5ef6ac1faf5fa946b30c84d334f80ad
