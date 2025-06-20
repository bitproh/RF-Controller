from utils import slow_print

class MockInstrument:
    def __init__(self):
        self.freq = "0.0"
        self.power = "0.0"

    def write(self, command):
        slow_print(f"[MOCK WRITE] {command}")

        # Parse SCPI commands like "FREQ 2e9" or "POW -10"
        if command.startswith("FREQ "):
            try:
                self.freq = command.split(" ")[1]
            except IndexError:
                self.freq = "0.0"

        elif command.startswith("POW "):
            try:
                self.power = command.split(" ")[1]
            except IndexError:
                self.power = "0.0"

    def query(self, command):
        slow_print(f"[MOCK QUERY] {command}")
        if command == "FREQ?":
            return f"{self.freq}\n"
        elif command == "POW?":
            return f"{self.power}\n"
        else:
            return "OK\n"

    def close(self):
        slow_print("[MOCK] Closed instrument")
