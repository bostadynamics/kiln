# src/core/kiln.py
from .delta_2 import Delta2
from .config import SLAVE_ADDRESS, DEFAULT_PORT_NAME, DEFAULT_BAUDRATE, TIMEOUT

# Global Kiln Instance
kiln = Delta2(DEFAULT_PORT_NAME, SLAVE_ADDRESS)
kiln.serial.timeout = TIMEOUT
kiln.serial.baudrate = DEFAULT_BAUDRATE
