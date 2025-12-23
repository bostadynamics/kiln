# src/routers/hardware.py
import asyncio
from fastapi import APIRouter, HTTPException, Depends
from typing import Any
from .monitoring import get_kiln
from ..core.models import (
    SetpointRequest,
    ControlMethodRequest,
    HeatingCoolingRequest,
    TempUnitRequest,
    PIDRequest,
    OutputRequest,
    RunStopRequest,
    LockStatusRequest,
    PIDSelectionRequest,
    AnalogDecimalRequest,
    ValveFeedbackRequest,
    ATValveFeedbackRequest,
    DecimalPointRequest,
    ATSettingRequest,
    StopSettingPIDRequest,
    TempStopPIDRequest,
    SystemAlarmRequest,
    SensorTypeRequest,
    PatternStepRequest,
    IntValueRequest,
)

router = APIRouter(tags=["hardware"])


# Helper to execute sync methods in thread pool if kiln is not async (Delta2)
async def _eval(kiln: Any, func_name: str, *args, **kwargs):
    method = getattr(kiln, func_name)
    if asyncio.iscoroutinefunction(method):
        return await method(*args, **kwargs)
    return await asyncio.to_thread(method, *args, **kwargs)


# --- Core Values ---


@router.get("/pv")
async def get_process_value(kiln: Any = Depends(get_kiln)):
    pv = await _eval(kiln, "get_pv")
    return {"pv": pv}


@router.get("/setpoint")
async def get_setpoint(kiln: Any = Depends(get_kiln)):
    sp = await _eval(kiln, "get_setpoint")
    return {"setpoint": sp}


@router.post("/setpoint")
async def set_setpoint(req: SetpointRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_setpoint", req.value)
    return {"status": "ok", "setpoint": req.value}


@router.get("/temp-range")
async def get_temp_range(kiln: Any = Depends(get_kiln)):
    upper = await _eval(kiln, "get_upper_limit_temp_range")
    lower = await _eval(kiln, "get_lower_limit_temp_range")
    return {"upper_limit": upper, "lower_limit": lower}


# --- Configuration ---


@router.get("/setting/sensor-type")
async def get_sensor_type(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_sensor_type")
    return {"sensor_type": val}


@router.get("/setting/control-method")
async def get_control_method(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_control_method")
    return {"control_method": val}


@router.post("/setting/control-method")
async def set_control_method(req: ControlMethodRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_control_method", req.value)
    return {"status": "ok", "control_method": req.value}


@router.get("/setting/heating-cooling")
async def get_heating_cooling_selection(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_heating_cooling_selection")
    return {"heating_cooling": val}


@router.post("/setting/heating-cooling")
async def set_heating_cooling_selection(
    req: HeatingCoolingRequest, kiln: Any = Depends(get_kiln)
):
    await _eval(kiln, "set_heating_cooling_selection", req.value)
    return {"status": "ok", "heating_cooling": req.value}


@router.get("/setting/temp-unit")
async def get_temp_unit(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_temp_unit_display")
    return {"temp_unit": val}


@router.post("/setting/temp-unit")
async def set_temp_unit(req: TempUnitRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_temp_unit_display", req.value)
    return {"status": "ok", "temp_unit": req.value}


@router.get("/settings/all")
async def get_all_settings(kiln: Any = Depends(get_kiln)):
    # Specific implementation for all settings
    if hasattr(kiln, "get_all_settings") and asyncio.iscoroutinefunction(
        kiln.get_all_settings
    ):
        return await kiln.get_all_settings()

    # Fallback to individual calls
    return {
        "control_method": await _eval(kiln, "get_control_method"),
        "heating_cooling": await _eval(kiln, "get_heating_cooling_selection"),
        "temp_unit": await _eval(kiln, "get_temp_unit_display"),
        "sensor_type": await _eval(kiln, "get_sensor_type"),
        "lock_status": await _eval(kiln, "get_setting_lock_status"),
        "pid_selection": await _eval(kiln, "get_pid_parameter_selection"),
        "analog_decimal": await _eval(kiln, "get_analog_decimal_setting"),
        "valve_feedback": await _eval(kiln, "get_valve_feedback_setting"),
        "at_valve_feedback": await _eval(kiln, "get_auto_tuning_valve_feedback"),
        "decimal_point": await _eval(kiln, "get_decimal_point_position"),
        "at_setting": await _eval(kiln, "get_at_setting"),
        "run_stop": await _eval(kiln, "get_run_stop_setting"),
        "stop_pid": await _eval(kiln, "get_stop_setting_pid"),
        "temp_stop_pid": await _eval(kiln, "get_temporarily_stop_pid"),
        "system_alarm": await _eval(kiln, "get_system_alarm_setting"),
    }


@router.get("/setting/lock-status")
async def get_lock_status(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_setting_lock_status")
    return {"lock_status": val}


@router.post("/setting/lock-status")
async def set_lock_status(req: LockStatusRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_setting_lock_status", req.value)
    return {"status": "ok", "lock_status": req.value}


@router.get("/setting/pid-selection")
async def get_pid_selection(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_pid_parameter_selection")
    return {"pid_selection": val}


@router.post("/setting/pid-selection")
async def set_pid_selection(req: PIDSelectionRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_pid_parameter_selection", req.value)
    return {"status": "ok", "pid_selection": req.value}


@router.get("/setting/analog-decimal")
async def get_analog_decimal(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_analog_decimal_setting")
    return {"analog_decimal": val}


@router.post("/setting/analog-decimal")
async def set_analog_decimal(req: AnalogDecimalRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_analog_decimal_setting", req.value)
    return {"status": "ok", "analog_decimal": req.value}


@router.get("/setting/valve-feedback")
async def get_valve_feedback(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_valve_feedback_setting")
    return {"valve_feedback": val}


@router.post("/setting/valve-feedback")
async def set_valve_feedback(req: ValveFeedbackRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_valve_feedback_setting", req.value)
    return {"status": "ok", "valve_feedback": req.value}


@router.get("/setting/at-valve-feedback")
async def get_at_valve_feedback(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_auto_tuning_valve_feedback")
    return {"at_valve_feedback": val}


@router.post("/setting/at-valve-feedback")
async def set_at_valve_feedback(
    req: ATValveFeedbackRequest, kiln: Any = Depends(get_kiln)
):
    await _eval(kiln, "set_auto_tuning_valve_feedback", req.value)
    return {"status": "ok", "at_valve_feedback": req.value}


@router.get("/setting/decimal-point")
async def get_decimal_point(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_decimal_point_position")
    return {"decimal_point": val}


@router.post("/setting/decimal-point")
async def set_decimal_point(req: DecimalPointRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_decimal_point_position", req.value)
    return {"status": "ok", "decimal_point": req.value}


@router.get("/setting/at-setting")
async def get_at_setting(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_at_setting")
    return {"at_setting": val}


@router.post("/setting/at-setting")
async def set_at_setting(req: ATSettingRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_at_setting", req.value)
    return {"status": "ok", "at_setting": req.value}


@router.get("/setting/stop-pid")
async def get_stop_pid(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_stop_setting_pid")
    return {"stop_pid": val}


@router.post("/setting/stop-pid")
async def set_stop_pid(req: StopSettingPIDRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_stop_setting_pid", req.value)
    return {"status": "ok", "stop_pid": req.value}


@router.get("/setting/temp-stop-pid")
async def get_temp_stop_pid(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_temporarily_stop_pid")
    return {"temp_stop_pid": val}


@router.post("/setting/temp-stop-pid")
async def set_temp_stop_pid(req: TempStopPIDRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_temporarily_stop_pid", req.value)
    return {"status": "ok", "temp_stop_pid": req.value}


@router.post("/sensor-type")
async def set_sensor_type(req: SensorTypeRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_sensor_type", req.value)
    return {"status": "ok", "sensor_type": req.value}


# --- PID Parameters ---


@router.get("/pid/p")
async def get_proportional_band(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_proportional_band")
    return {"proportional_band": val}


@router.post("/pid/p")
async def set_proportional_band(req: PIDRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_proportional_band", req.value)
    return {"status": "ok", "proportional_band": req.value}


@router.get("/pid/i")
async def get_integral_time(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_integral_time")
    return {"integral_time": val}


@router.post("/pid/i")
async def set_integral_time(req: PIDRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_integral_time", req.value)
    return {"status": "ok", "integral_time": req.value}


@router.get("/pid/d")
async def get_derivative_time(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_derivative_time")
    return {"derivative_time": val}


@router.post("/pid/d")
async def set_derivative_time(req: PIDRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_derivative_time", req.value)
    return {"status": "ok", "derivative_time": req.value}


# --- Outputs & Alarms ---


@router.get("/output/{index}")
async def get_output_value(index: int, kiln: Any = Depends(get_kiln)):
    if index == 1:
        val = await _eval(kiln, "get_output_1_value")
        return {"output_1": val}
    elif index == 2:
        val = await _eval(kiln, "get_output_2_value")
        return {"output_2": val}
    else:
        raise HTTPException(status_code=404, detail="Output index must be 1 or 2")


@router.post("/output/{index}")
async def set_output_value(
    index: int, req: OutputRequest, kiln: Any = Depends(get_kiln)
):
    method_name = f"set_output_{index}_value"
    await _eval(kiln, method_name, req.value)
    return {"status": "ok", "output": index, "value": req.value}


@router.get("/alarm/system")
async def get_system_alarm(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_system_alarm_setting")
    return {"system_alarm": val}


@router.post("/alarm/system")
async def set_system_alarm(req: SystemAlarmRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_system_alarm_setting", req.value)
    return {"status": "ok", "system_alarm": req.value}


@router.get("/alarm/{index}/type")
async def get_alarm_type(index: int, kiln: Any = Depends(get_kiln)):
    method_name = f"get_alarm_{index}_type"
    val = await _eval(kiln, method_name)
    return {"alarm_index": index, "type": val}


@router.get("/alarm/{index}/limits")
async def get_alarm_limits(index: int, kiln: Any = Depends(get_kiln)):
    upper = await _eval(kiln, f"get_upper_limit_alarm_{index}")
    lower = await _eval(kiln, f"get_lower_limit_alarm_{index}")
    return {"alarm_index": index, "upper": upper, "lower": lower}


# --- Patterns ---


@router.get("/pattern/{id}")
async def get_pattern(id: int, kiln: Any = Depends(get_kiln)):
    if hasattr(kiln, "get_pattern") and asyncio.iscoroutinefunction(kiln.get_pattern):
        return await kiln.get_pattern(id)

    steps = []
    try:
        for step in range(8):
            temp, time_val = await asyncio.to_thread(kiln.get_pattern_step, id, step)
            steps.append({"step": step, "temp": temp, "time": time_val})
        return {"pattern_id": id, "steps": steps}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pattern/{id}/step/{step_id}")
async def set_pattern_step(
    id: int, step_id: int, req: PatternStepRequest, kiln: Any = Depends(get_kiln)
):
    try:
        if hasattr(kiln, "set_pattern_step") and asyncio.iscoroutinefunction(
            kiln.set_pattern_step
        ):
            await kiln.set_pattern_step(id, step_id, req.temp, req.time)
        else:
            await asyncio.to_thread(
                kiln.set_pattern_step, id, step_id, req.temp, req.time
            )
        return {"status": "ok", "pattern": id, "step": step_id, "data": req}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pattern_start")
async def get_start_pattern(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_start_pattern_number")
    return {"start_pattern": val}


@router.post("/pattern_start")
async def set_start_pattern(req: IntValueRequest, kiln: Any = Depends(get_kiln)):
    try:
        await _eval(kiln, "set_start_pattern_number", req.value)
        return {"status": "ok", "start_pattern": req.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pattern/{id}/actual-steps")
async def get_actual_steps(id: int, kiln: Any = Depends(get_kiln)):
    try:
        val = await _eval(kiln, "get_actual_step_number_setting", id)
        return {"pattern_id": id, "actual_steps": val}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pattern/{id}/actual-steps")
async def set_actual_steps(
    id: int, req: IntValueRequest, kiln: Any = Depends(get_kiln)
):
    try:
        await _eval(kiln, "set_actual_step_number_setting", id, req.value)
        return {"status": "ok", "pattern_id": id, "actual_steps": req.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/current/program")
async def get_current_program_status(kiln: Any = Depends(get_kiln)):
    if hasattr(kiln, "get_executing_program_status") and asyncio.iscoroutinefunction(
        kiln.get_executing_program_status
    ):
        return await kiln.get_executing_program_status()

    return {
        "pattern": await _eval(kiln, "get_executing_pattern_number"),
        "step": await _eval(kiln, "get_executing_step_number"),
        "time_left_min": await _eval(kiln, "get_step_time_left_min"),
        "time_left_sec": await _eval(kiln, "get_step_time_left_sec"),
    }


# --- Status & Run/Stop ---


@router.get("/status/leds")
async def get_led_status(kiln: Any = Depends(get_kiln)):
    status = await _eval(kiln, "get_led_status")
    return {
        "raw": status,
        "AT": await _eval(kiln, "get_led_at_status"),
        "OUT1": await _eval(kiln, "get_led_out1_status"),
        "OUT2": await _eval(kiln, "get_led_out2_status"),
        "ALM1": await _eval(kiln, "get_led_alarm1_status"),
        "ALM2": await _eval(kiln, "get_led_alarm2_status"),
        "ALM3": await _eval(kiln, "get_led_alarm3_status"),
        "degF": await _eval(kiln, "get_led_deg_f_status"),
        "degC": await _eval(kiln, "get_led_deg_c_status"),
    }


@router.get("/run")
async def get_run_status(kiln: Any = Depends(get_kiln)):
    val = await _eval(kiln, "get_run_stop_setting")
    return {"run_status": val}


@router.post("/run")
async def set_run_status(req: RunStopRequest, kiln: Any = Depends(get_kiln)):
    await _eval(kiln, "set_run_stop_setting", req.value)
    return {"status": "ok", "run_status": req.value}


@router.get("/status/keys")
async def get_key_status(kiln: Any = Depends(get_kiln)):
    return {
        "set": await _eval(kiln, "get_key_set_status"),
        "select": await _eval(kiln, "get_key_function_status"),
        "up": await _eval(kiln, "get_key_up_status"),
        "down": await _eval(kiln, "get_key_down_status"),
    }
