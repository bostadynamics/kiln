# src/core/kiln.py
import os

from .config import DEFAULT_BAUDRATE, DEFAULT_PORT_NAME, SLAVE_ADDRESS, TIMEOUT
from .delta_2 import Delta2
from .mock_delta_2 import MockDelta2

# Global Kiln Instance
if os.environ.get("USE_MOCK_DELTA", "false").lower() == "true":
    print("USING MOCK DELTA 2 CONTROLLER")
    kiln = MockDelta2(DEFAULT_PORT_NAME, SLAVE_ADDRESS)
else:
    kiln = Delta2(DEFAULT_PORT_NAME, SLAVE_ADDRESS)
kiln.serial.timeout = TIMEOUT
kiln.serial.baudrate = DEFAULT_BAUDRATE
