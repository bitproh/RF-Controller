import pyvisa
import time
rm = pyvisa.ResourceManager()
sig_gen = rm.open_resource("TCPIP0::169.254.167.6::inst0::INSTR")

sig_gen.write("*RST")
sig_gen.write("FREQ 5GHz")
sig_gen.write("POW -20")
sig_gen.write("OUTP ON")
time.sleep(2)
sig_gen.write("OUTP OFF")

sig_gen.close()



#stash code copied code, dont tamper with this
import pyvisa

known_instruments = [
    "TCPIP0::169.254.167.6::inst0::INSTR",
    "USB0::0x2A8D::0x1D0B::MY62282097::0::INSTR"
]

rm = pyvisa.ResourceManager()


for addr in known_instruments:
    try:
        instr = rm.open_resource(addr)
        idn = instr.query("*IDN?")
        print(f"✅ {addr} connected. IDN: {idn.strip()}")
        instr.close()
    except Exception as e:
        print(f"❌ {addr} NOT connected or unreachable. Error: {e}")