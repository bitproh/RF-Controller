from utils import slow_print, SLOW_MODE

class MockGAInstrument:
    def __init__(self):
        # Signal Generator parameters
        self.sg_freq = "0.0"
        self.sg_power = "0.0"
        # Spectrum Analyzer parameters
        self.sa_center_freq = "0.0"
        self.sa_span = "0.0"
        self.sa_ref_level = "0.0"
        self.sa_marker_freq = "1.0e9"
        self.sa_marker_power = "-30.0"

    # Unified write method (auto routes to SG/SA)
    def write(self, command):
        if command.startswith("FREQ:CENT") or command.startswith("FREQ:SPAN") or \
           command.startswith("DISP") or command.startswith("CALC"):
            self.sa_write(command)
        else:
            self.sg_write(command)

    # Unified query method (auto routes to SG/SA)
    def query(self, command):
        if command.startswith("CALC") or command.startswith("FREQ:CENT") or command.startswith("FREQ:SPAN"):
            return self.sa_query(command)
        else:
            return self.sg_query(command)

    # ---------- Signal Generator Emulation ----------
    def sg_write(self, command):
        slow_print(f"[SG MOCK WRITE] {command}")
        if command.startswith("FREQ "):
            self.sg_freq = command.split(" ")[1]
        elif command.startswith("POW "):
            self.sg_power = command.split(" ")[1]
        elif command == "OUTP ON":
            slow_print("[SG MOCK] Output ON")
        elif command == "OUTP OFF":
            slow_print("[SG MOCK] Output OFF")

    def sg_query(self, command):
        slow_print(f"[SG MOCK QUERY] {command}")
        if command == "FREQ?":
            return f"{self.sg_freq}\n"
        elif command == "POW?":
            return f"{self.sg_power}\n"
        return "OK\n"

    # ---------- Spectrum Analyzer Emulation ----------
    def sa_write(self, command):
        slow_print(f"[SA MOCK WRITE] {command}")
        if command.startswith("FREQ:CENT "):
            self.sa_center_freq = command.split(" ")[1]
        elif command.startswith("FREQ:SPAN "):
            self.sa_span = command.split(" ")[1]
        elif command.startswith("DISP:WIND:TRAC:Y:RLEV "):
            self.sa_ref_level = command.split(" ")[1]
        elif command.startswith("CALC:MARK1:MAX"):
            self.sa_marker_freq = self.sa_center_freq
            self.sa_marker_power = "-25.0"

    def sa_query(self, command):
        slow_print(f"[SA MOCK QUERY] {command}")
        if command == "FREQ:CENT?":
            return f"{self.sa_center_freq}\n"
        elif command == "FREQ:SPAN?":
            return f"{self.sa_span}\n"
        elif command == "DISP:WIND:TRAC:Y:RLEV?":
            return f"{self.sa_ref_level}\n"
        elif command == "CALC:MARK1:X?":
            return f"{self.sa_marker_freq}\n"
        elif command == "CALC:MARK1:Y?":
            return f"{self.sa_marker_power}\n"
        return "OK\n"

    def close(self):
        slow_print("[MOCK] Closed GA Monitor instruments")