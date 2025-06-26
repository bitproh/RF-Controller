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

    # Simulate SG write
    def sg_write(self, command):
        slow_print(f"[SG MOCK WRITE] {command}")
        if command.startswith("FREQ "):
            try:
                self.sg_freq = command.split(" ")[1]
            except IndexError:
                self.sg_freq = "0.0"
        elif command.startswith("POW "):
            try:
                self.sg_power = command.split(" ")[1]
            except IndexError:
                self.sg_power = "0.0"
        elif command == "OUTP ON":
            slow_print("[SG MOCK] Output ON")
        elif command == "OUTP OFF":
            slow_print("[SG MOCK] Output OFF")

    # Simulate SG query
    def sg_query(self, command):
        slow_print(f"[SG MOCK QUERY] {command}")
        if command == "FREQ?":
            return f"{self.sg_freq}\n"
        elif command == "POW?":
            return f"{self.sg_power}\n"
        else:
            return "OK\n"

    # Simulate SA write
    def sa_write(self, command):
        slow_print(f"[SA MOCK WRITE] {command}")
        if command.startswith("FREQ:CENT "):
            try:
                self.sa_center_freq = command.split(" ")[1]
            except IndexError:
                self.sa_center_freq = "0.0"
        elif command.startswith("FREQ:SPAN "):
            try:
                self.sa_span = command.split(" ")[1]
            except IndexError:
                self.sa_span = "0.0"
        elif command.startswith("DISP:WIND:TRAC:Y:RLEV "):
            try:
                self.sa_ref_level = command.split(" ")[1]
            except IndexError:
                self.sa_ref_level = "0.0"
        elif command.startswith("CALC:MARK1:MAX"):
            # Simulate marker peak search
            self.sa_marker_freq = self.sa_center_freq
            self.sa_marker_power = "-25.0"

    # Simulate SA query
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
        else:
            return "OK\n"

    def close(self):
        slow_print("[MOCK] Closed GA Monitor instruments")