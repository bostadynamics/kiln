import sys

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Ensure we can import delta_2
sys.path.append(".")
from delta_2 import (
    AnalogDecimalSetting,
    ATSetting,
    ControlMethod,
    DecimalPointPosition,
    Delta2,
    HeatingCoolingSelection,
    PIDParameterSelection,
    RunStopSetting,
    SettingLockStatus,
    StopSettingPID,
    SystemAlarmSetting,
    TemporarilyStopPID,
    TempUnit,
    ValveFeedbackSetting,
    AutoTuningValveFeedback,
)

app = FastAPI(title="Delta DTB Controller API")
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


class LockStatusRequest(BaseModel):
    value: SettingLockStatus


class PIDSelectionRequest(BaseModel):
    value: PIDParameterSelection


class AnalogDecimalRequest(BaseModel):
    value: AnalogDecimalSetting


class ValveFeedbackRequest(BaseModel):
    value: ValveFeedbackSetting


class ATValveFeedbackRequest(BaseModel):
    value: AutoTuningValveFeedback


class DecimalPointRequest(BaseModel):
    value: DecimalPointPosition


class ATSettingRequest(BaseModel):
    value: ATSetting


class StopSettingPIDRequest(BaseModel):
    value: StopSettingPID


class TempStopPIDRequest(BaseModel):
    value: TemporarilyStopPID


class SystemAlarmRequest(BaseModel):
    value: SystemAlarmSetting


class SensorTypeRequest(BaseModel):
    value: int


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


@app.get("/settings/all")
def get_all_settings():
    return {
        "control_method": kiln.get_control_method(),
        "heating_cooling": kiln.get_heating_cooling_selection(),
        "temp_unit": kiln.get_temp_unit_display(),
        "sensor_type": kiln.get_sensor_type(),
        "lock_status": kiln.get_setting_lock_status(),
        "pid_selection": kiln.get_pid_parameter_selection(),
        "analog_decimal": kiln.get_analog_decimal_setting(),
        "valve_feedback": kiln.get_valve_feedback_setting(),
        "at_valve_feedback": kiln.get_auto_tuning_valve_feedback(),
        "decimal_point": kiln.get_decimal_point_position(),
        "at_setting": kiln.get_at_setting(),
        "run_stop": kiln.get_run_stop_setting(),
        "stop_pid": kiln.get_stop_setting_pid(),
        "temp_stop_pid": kiln.get_temporarily_stop_pid(),
        "system_alarm": kiln.get_system_alarm_setting(),
    }


@app.get("/setting/lock-status")
def get_lock_status():
    return {"lock_status": kiln.get_setting_lock_status()}


@app.post("/setting/lock-status")
def set_lock_status(req: LockStatusRequest):
    kiln.set_setting_lock_status(req.value)
    return {"status": "ok", "lock_status": req.value}


@app.get("/setting/pid-selection")
def get_pid_selection():
    return {"pid_selection": kiln.get_pid_parameter_selection()}


@app.post("/setting/pid-selection")
def set_pid_selection(req: PIDSelectionRequest):
    kiln.set_pid_parameter_selection(req.value)
    return {"status": "ok", "pid_selection": req.value}


@app.get("/setting/analog-decimal")
def get_analog_decimal():
    return {"analog_decimal": kiln.get_analog_decimal_setting()}


@app.post("/setting/analog-decimal")
def set_analog_decimal(req: AnalogDecimalRequest):
    kiln.set_analog_decimal_setting(req.value)
    return {"status": "ok", "analog_decimal": req.value}


@app.get("/setting/valve-feedback")
def get_valve_feedback():
    return {"valve_feedback": kiln.get_valve_feedback_setting()}


@app.post("/setting/valve-feedback")
def set_valve_feedback(req: ValveFeedbackRequest):
    kiln.set_valve_feedback_setting(req.value)
    return {"status": "ok", "valve_feedback": req.value}


@app.get("/setting/at-valve-feedback")
def get_at_valve_feedback():
    return {"at_valve_feedback": kiln.get_auto_tuning_valve_feedback()}


@app.post("/setting/at-valve-feedback")
def set_at_valve_feedback(req: ATValveFeedbackRequest):
    kiln.set_auto_tuning_valve_feedback(req.value)
    return {"status": "ok", "at_valve_feedback": req.value}


@app.get("/setting/decimal-point")
def get_decimal_point():
    return {"decimal_point": kiln.get_decimal_point_position()}


@app.post("/setting/decimal-point")
def set_decimal_point(req: DecimalPointRequest):
    kiln.set_decimal_point_position(req.value)
    return {"status": "ok", "decimal_point": req.value}


@app.get("/setting/at-setting")
def get_at_setting():
    return {"at_setting": kiln.get_at_setting()}


@app.post("/setting/at-setting")
def set_at_setting(req: ATSettingRequest):
    kiln.set_at_setting(req.value)
    return {"status": "ok", "at_setting": req.value}


@app.get("/setting/stop-pid")
def get_stop_pid():
    return {"stop_pid": kiln.get_stop_setting_pid()}


@app.post("/setting/stop-pid")
def set_stop_pid(req: StopSettingPIDRequest):
    kiln.set_stop_setting_pid(req.value)
    return {"status": "ok", "stop_pid": req.value}


@app.get("/setting/temp-stop-pid")
def get_temp_stop_pid():
    return {"temp_stop_pid": kiln.get_temporarily_stop_pid()}


@app.post("/setting/temp-stop-pid")
def set_temp_stop_pid(req: TempStopPIDRequest):
    kiln.set_temporarily_stop_pid(req.value)
    return {"status": "ok", "temp_stop_pid": req.value}


@app.post("/sensor-type")
def set_sensor_type(req: SensorTypeRequest):
    kiln.set_sensor_type(req.value)
    return {"status": "ok", "sensor_type": req.value}


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


@app.post("/alarm/system")
def set_system_alarm(req: SystemAlarmRequest):
    kiln.set_system_alarm_setting(req.value)
    return {"status": "ok", "system_alarm": req.value}


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


@app.get("/status/keys")
def get_key_status():
    return {
        "set": kiln.get_key_set_status(),
        "select": kiln.get_key_function_status(),
        "up": kiln.get_key_up_status(),
        "down": kiln.get_key_down_status(),
    }
