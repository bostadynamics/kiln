import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Modbus Configuration
SLAVE_ADDRESS = 1
DEFAULT_PORT_NAME = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 38400
TIMEOUT = 0.3

# Monitoring Configuration
RECORDING_FILE = "recording.txt"

# For separate service mode (client-server communication)
KILN_SERVER_URL = "http://localhost:8000"
MONITOR_SERVER_URL = "http://localhost:8001"
