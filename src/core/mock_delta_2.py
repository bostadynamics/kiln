import threading

from .delta_2 import Delta2, Register


class MockDelta2(Delta2):
    """
    Mock implementation of Delta2 for testing without hardware.

    This class inherits from Delta2 to ensure interface consistency,
    but overrides the low-level Modbus communication methods to use
    in-memory storage instead of a serial connection.

    It simulates the behavior of the Delta DTB Series Controller registers,
    storing values as raw integers (like the device does) and handling
    the decimal point conversion in read/write methods.
    """

    def __init__(self, portname="mock", slaveaddress=1):
        # Do not call super().__init__ to prevent serial connection attempt.
        # MinimalModbus Instrument init would try to open the port.
        self.portname = portname
        self.slaveaddress = slaveaddress
        self.lock = threading.Lock()

        # Dummy serial object to allow setting timeout/baudrate without error
        class DummySerial:
            timeout = 1
            baudrate = 9600

        self.serial = DummySerial()

        # Storage for registers and bits
        # Registers store raw integer values (as they appear in the device)
        self.registers = {}
        # Bits store 0 or 1
        self.bits = {}

        # Initialize default values
        # PV: 25.0 degrees (stored as 250 with decimal=1 implied by usage)
        self.registers[Register.PV] = 250
        # SV: 25.0 degrees
        self.registers[Register.SV] = 350
        self.registers[Register.OUTPUT_1_VALUE] = 555
        self.registers[Register.OUTPUT_2_VALUE] = 785
        # Upper limit temp range: default likely high, e.g., 400.0 -> 4000
        self.registers[Register.UPPER_LIMIT_TEMP_RANGE] = 4000
        # Lower limit temp range: default likely low, e.g. 0.0 -> 0
        self.registers[Register.LOWER_LIMIT_TEMP_RANGE] = 0

        # Control Method: PID (0)
        self.registers[Register.CONTROL_METHOD] = 0
        temps = [0, 25, 300, 400, 500, 600, 700, 800]
        times = [0, 10, 20, 30, 40, 50, 60, 700]
        for p_n in range(8):
            for s_n in range(8):
                self.set_pattern_step(p_n, s_n, temps[s_n], times[s_n])

    def read_register(
        self, registeraddress, number_of_decimals=0, functioncode=3, signed=False
    ):
        """
        Mock read_register.
        Returns the value from the internal register storage, processed for decimals.
        """
        raw_value = self.registers.get(registeraddress, 0)

        # If the value is stored as a negative/positive python int, we use it directly.
        # We assume the mocked application writes valid range values.

        if number_of_decimals > 0:
            return float(raw_value) / (10**number_of_decimals)

        return int(raw_value)

    def write_register(
        self, registeraddress, value, number_of_decimals=0, functioncode=6, signed=False
    ):
        """
        Mock write_register.
        Stores the value into the internal register storage, converted to raw integer.
        """
        if number_of_decimals > 0:
            raw_value = int(round(value * (10**number_of_decimals)))
        else:
            raw_value = int(value)

        self.registers[registeraddress] = raw_value

    def read_bit(self, registeraddress, functioncode=2):
        """
        Mock read_bit.
        Returns 0 or 1.
        """
        return self.bits.get(registeraddress, 0)

    def write_bit(self, registeraddress, value, functioncode=5):
        """
        Mock write_bit.
        Stores value (0 or 1).
        """
        self.bits[registeraddress] = int(value)
