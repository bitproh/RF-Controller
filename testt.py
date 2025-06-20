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

