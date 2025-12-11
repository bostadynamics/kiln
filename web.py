from fastapi import FastAPI

from delta import Delta

app = FastAPI()

SLAVE_ADDRESS = 1
ADDRESS_SETPOINT = 0x1001
TIMEOUT = 0.3  # seconds. At least 0.3 seconds required for 2400 bits/s ASCII mode.
DEFAULT_PORT_NAME = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 38400  # baud (pretty much bit/s). Use 2400 or 38400 bit/s.

kiln = Delta(DEFAULT_PORT_NAME, SLAVE_ADDRESS)
kiln.serial.timeout = TIMEOUT
kiln.serial.baudrate = DEFAULT_BAUDRATE


@app.get("/status")
async def status():
    return {
        "current_temp": kiln.get_pv(),
        "target_temp": kiln.get_setpoint(),
        "current_step": kiln.get_current_step(),
        "min_left_for_step": kiln.get_current_step_left_min(),
        "sec_left_for_step": kiln.get_current_step_left_sec(),
        "integral_time": kiln.get_integral_time(),
        "derivative_time": kiln.get_derivative_time(),
    }


@app.get("/patterns")
async def get_all_patterns():
    return kiln.get_all_patterns()


@app.get("/pattern/{id}")
async def get_pattern(id):
    if id == "current":
        return kiln.get_pattern(kiln.get_current_program())
    return kiln.get_pattern(int(id))
