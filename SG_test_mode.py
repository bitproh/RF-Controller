from utils import slow_print

class MockInstrument:
    def write(self, command):
        slow_print(f"[MOCK WRITE] {command}")

    def query(self, command):
        slow_print(f"[MOCK QUERY] {command}")
        if command == "*IDN?":
            return "MockInstrument,Model123,Serial0001,1.0\n"
        elif command == "FREQ?":
            return "2.0000000000E+09\n"
        elif command == "POW?":
            return "-10.0\n"
        else:
            return "OK\n"

    def close(self):
        slow_print("[MOCK] Closed instrument")
