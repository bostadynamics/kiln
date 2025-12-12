import sys

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Ensure we can import delta_2
sys.path.append(".")
from delta_2 import (
    ControlMethod,
    Delta2,
    HeatingCoolingSelection,
    RunStopSetting,
    TempUnit,
)

app = FastAPI(title="Delta DTB Controller API")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SLAVE_ADDRESS = 1
DEFAULT_PORT_NAME = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 38400
TIMEOUT = 0.3

# Global Kiln Instance
kiln = Delta2(DEFAULT_PORT_NAME, SLAVE_ADDRESS)
kiln.serial.timeout = TIMEOUT
kiln.serial.baudrate = DEFAULT_BAUDRATE


# Pydantic Models for Requests
class SetpointRequest(BaseModel):
    value: float


class ControlMethodRequest(BaseModel):
    value: ControlMethod


class HeatingCoolingRequest(BaseModel):
    value: HeatingCoolingSelection


class TempUnitRequest(BaseModel):
    value: TempUnit


class PIDRequest(BaseModel):
    value: float


class OutputRequest(BaseModel):
    value: float


class AlarmTypeRequest(BaseModel):
    value: int


class AlarmLimitRequest(BaseModel):
    value: int


class PatternStepRequest(BaseModel):
    temp: float
    time: int


class RunStopRequest(BaseModel):
    value: RunStopSetting


# --- Core Values ---


@app.get("/pv")
def get_process_value():
    return {"pv": kiln.get_pv()}


@app.get("/setpoint")
def get_setpoint():
    return {"setpoint": kiln.get_setpoint()}


@app.post("/setpoint")
def set_setpoint(req: SetpointRequest):
    kiln.set_setpoint(req.value)
    return {"status": "ok", "setpoint": req.value}


@app.get("/temp-range")
def get_temp_range():
    return {
        "upper_limit": kiln.get_upper_limit_temp_range(),
        "lower_limit": kiln.get_lower_limit_temp_range(),
    }


# --- Configuration ---


@app.get("/sensor-type")
def get_sensor_type():
    return {"sensor_type": kiln.get_sensor_type()}


@app.get("/control-method")
def get_control_method():
    return {"control_method": kiln.get_control_method()}


@app.post("/control-method")
def set_control_method(req: ControlMethodRequest):
    kiln.set_control_method(req.value)
    return {"status": "ok", "control_method": req.value}


@app.get("/heating-cooling")
def get_heating_cooling_selection():
    return {"heating_cooling": kiln.get_heating_cooling_selection()}


@app.post("/heating-cooling")
def set_heating_cooling_selection(req: HeatingCoolingRequest):
    kiln.set_heating_cooling_selection(req.value)
    return {"status": "ok", "heating_cooling": req.value}


@app.get("/temp-unit")
def get_temp_unit():
    return {"temp_unit": kiln.get_temp_unit_display()}


@app.post("/temp-unit")
def set_temp_unit(req: TempUnitRequest):
    kiln.set_temp_unit_display(req.value)
    return {"status": "ok", "temp_unit": req.value}


# --- PID Parameters ---


@app.get("/pid/p")
def get_proportional_band():
    return {"proportional_band": kiln.get_proportional_band()}


@app.post("/pid/p")
def set_proportional_band(req: PIDRequest):
    kiln.set_proportional_band(req.value)
    return {"status": "ok", "proportional_band": req.value}


@app.get("/pid/i")
def get_integral_time():
    return {"integral_time": kiln.get_integral_time()}


@app.post("/pid/i")
def set_integral_time(req: PIDRequest):
    kiln.set_integral_time(req.value)
    return {"status": "ok", "integral_time": req.value}


@app.get("/pid/d")
def get_derivative_time():
    return {"derivative_time": kiln.get_derivative_time()}


@app.post("/pid/d")
def set_derivative_time(req: PIDRequest):
    kiln.set_derivative_time(req.value)
    return {"status": "ok", "derivative_time": req.value}


# --- Outputs & Alarms ---


@app.get("/output/{index}")
def get_output_value(index: int):
    if index == 1:
        return {"output_1": kiln.get_output_1_value()}
    elif index == 2:
        return {"output_2": kiln.get_output_2_value()}
    else:
        raise HTTPException(status_code=404, detail="Output index must be 1 or 2")


@app.post("/output/{index}")
def set_output_value(index: int, req: OutputRequest):
    if index == 1:
        kiln.set_output_1_value(req.value)
    elif index == 2:
        kiln.set_output_2_value(req.value)
    else:
        raise HTTPException(status_code=404, detail="Output index must be 1 or 2")
    return {"status": "ok", "output": index, "value": req.value}


@app.get("/alarm/system")
def get_system_alarm():
    return {"system_alarm": kiln.get_system_alarm_setting()}


@app.get("/alarm/{index}/type")
def get_alarm_type(index: int):
    if index == 1:
        val = kiln.get_alarm_1_type()
    elif index == 2:
        val = kiln.get_alarm_2_type()
    elif index == 3:
        val = kiln.get_alarm_3_type()
    else:
        raise HTTPException(status_code=404, detail="Alarm index must be 1, 2 or 3")
    return {"alarm_index": index, "type": val}


@app.get("/alarm/{index}/limits")
def get_alarm_limits(index: int):
    if index == 1:
        upper = kiln.get_upper_limit_alarm_1()
        lower = kiln.get_lower_limit_alarm_1()
    elif index == 2:
        upper = kiln.get_upper_limit_alarm_2()
        lower = kiln.get_lower_limit_alarm_2()
    elif index == 3:
        upper = kiln.get_upper_limit_alarm_3()
        lower = kiln.get_lower_limit_alarm_3()
    else:
        raise HTTPException(status_code=404, detail="Alarm index must be 1, 2 or 3")
    return {"alarm_index": index, "upper": upper, "lower": lower}


# --- Patterns ---


@app.get("/pattern/{id}")
def get_pattern(id: int):
    # Returns all steps for the pattern
    steps = []
    try:
        for step in range(8):
            temp, time_val = kiln.get_pattern_step(id, step)
            steps.append({"step": step, "temp": temp, "time": time_val})
        return {"pattern_id": id, "steps": steps}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/pattern/{id}/step/{step_id}")
def set_pattern_step(id: int, step_id: int, req: PatternStepRequest):
    try:
        kiln.set_pattern_step(id, step_id, req.temp, req.time)
        return {"status": "ok", "pattern": id, "step": step_id, "data": req}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/current/program")
def get_current_program_status():
    return {
        "pattern": kiln.get_executing_pattern_number(),
        "step": kiln.get_executing_step_number(),
        "time_left_min": kiln.get_step_time_left_min(),
        "time_left_sec": kiln.get_step_time_left_sec(),
    }


# --- Status & Run/Stop ---


@app.get("/status/leds")
def get_led_status():
    status = kiln.get_led_status()
    # Decode bits if needed, or return raw. The user requested fully expose functionality.
    # Helper methods in Delta2 exist for individual check, but simple status is raw.
    # Let's use the individual getters for a richer response?
    # Or just return the raw register and let client decode.
    # Let's return a detailed object using the bit getters.
    return {
        "raw": status,
        "AT": kiln.get_led_at_status(),
        "OUT1": kiln.get_led_out1_status(),
        "OUT2": kiln.get_led_out2_status(),
        "ALM1": kiln.get_led_alarm1_status(),
        "ALM2": kiln.get_led_alarm2_status(),
        "ALM3": kiln.get_led_alarm3_status(),
        "degF": kiln.get_led_deg_f_status(),
        "degC": kiln.get_led_deg_c_status(),
    }


@app.get("/run")
def get_run_status():
    return {"run_status": kiln.get_run_stop_setting()}


@app.post("/run")
def set_run_status(req: RunStopRequest):
    kiln.set_run_stop_setting(req.value)
    return {"status": "ok", "run_status": req.value}


@app.get("/patterns/{id}/edit", response_class=HTMLResponse)
async def pattern_editor(id: int, request: Request):
    return templates.TemplateResponse(
        "pattern_editor.html", {"request": request, "pattern_id": id}
    )


@app.get("/status/keys")
def get_key_status():
    return {
        "set": kiln.get_key_set_status(),
        "select": kiln.get_key_function_status(),
        "up": kiln.get_key_up_status(),
        "down": kiln.get_key_down_status(),
    }


from fastapi import Request
from fastapi.responses import HTMLResponse


def calculate_color(pv, sv):
    """Calculates color transitioning from Red to Green based on distance."""
    diff = abs(pv - sv)
    range_val = 50.0  # Range for transition

    # 0.0 (far) to 1.0 (close)
    t = 1.0 - (min(diff, range_val) / range_val)

    # Red: 239, 68, 68 (#ef4444)
    # Green: 34, 197, 94 (#22c55e)

    start_r, start_g, start_b = 239, 68, 68
    end_r, end_g, end_b = 34, 197, 94

    r = int(start_r + (end_r - start_r) * t)
    g = int(start_g + (end_g - start_g) * t)
    b = int(start_b + (end_b - start_b) * t)

    return f"rgb({r}, {g}, {b})"


@app.get("/", response_class=HTMLResponse)
async def main_view(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/patterns", response_class=HTMLResponse)
async def patterns_view(request: Request):
    return templates.TemplateResponse("patterns.html", {"request": request})


@app.get("/partials/dashboard", response_class=HTMLResponse)
async def get_dashboard_partial(request: Request):
    # Fetch values
    try:
        pv = kiln.get_pv()
        setpoint = kiln.get_setpoint()
        output1 = kiln.get_output_1_value()
        output2 = kiln.get_output_2_value()

        pv_color = calculate_color(pv, setpoint)

        # Fetch status
        current_pattern = kiln.get_executing_pattern_number()
        current_step = kiln.get_executing_step_number()
        time_left = f"{kiln.get_step_time_left_min()}m {kiln.get_step_time_left_sec()}s"

        return templates.TemplateResponse(
            "partials/dashboard.html",
            {
                "request": request,
                "pv": pv,
                "setpoint": setpoint,
                "output1": output1,
                "output2": output2,
                "pv_color": pv_color,
                "pattern": current_pattern,
                "step": current_step,
                "time_left": time_left,
            },
        )
    except Exception as e:
        # Return error fragment or log
        print(f"Error fetching data: {e}")
        # Return a simple error div if fails
        return HTMLResponse(
            f"<div class='error-msg' style='display:block'>Error: {str(e)}</div>"
        )
