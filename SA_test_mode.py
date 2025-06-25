from utils import slow_print

class MockInstrument:
    def __init__(self):
        self.center_freq = "0.0"
        self.span = "0.0"
        self.ref_level = "0.0"
        self.marker_freq = "1.0e9"
        self.marker_power = "-30.0"

    def write(self, command):
        slow_print(f"[MOCK WRITE] {command}")

        # Parse SCPI commands for spectrum analyzer
        if command.startswith("FREQ:CENT "):
            try:
                self.center_freq = command.split(" ")[1]
            except IndexError:
                self.center_freq = "0.0"
        elif command.startswith("FREQ:SPAN "):
            try:
                self.span = command.split(" ")[1]
            except IndexError:
                self.span = "0.0"
        elif command.startswith("DISP:WIND:TRAC:Y:RLEV "):
            try:
                self.ref_level = command.split(" ")[1]
            except IndexError:
                self.ref_level = "0.0"
        elif command.startswith("CALC:MARK1:MAX"):
            # Simulate marker peak search
            self.marker_freq = self.center_freq
            self.marker_power = "-25.0"

    def query(self, command):
        slow_print(f"[MOCK QUERY] {command}")
        if command == "FREQ:CENT?":
            return f"{self.center_freq}\n"
        elif command == "FREQ:SPAN?":
            return f"{self.span}\n"
        elif command == "DISP:WIND:TRAC:Y:RLEV?":
            return f"{self.ref_level}\n"
        elif command == "CALC:MARK1:X?":
            return f"{self.marker_freq}\n"
        elif command == "CALC:MARK1:Y?":
            return f"{self.marker_power}\n"
        else:
            return "OK\n"

    def close(self):
        slow_print("[MOCK] Closed instrument")