# src/routers/ui.py
import asyncio
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from typing import Any

# from ..core.kiln import kiln # Remove direct import
from ..core.utils import calculate_color
from ..core.config import TEMPLATES_DIR
from ..core.models import PatternStepRequest
from .monitoring import get_kiln
from ..core.delta_2 import (
    ControlMethod,
    HeatingCoolingSelection,
    SystemAlarmSetting,
    SettingLockStatus,
    PIDParameterSelection,
    AnalogDecimalSetting,
    ValveFeedbackSetting,
    AutoTuningValveFeedback,
    TempUnit,
    DecimalPointPosition,
    ATSetting,
    RunStopSetting,
    StopSettingPID,
    TemporarilyStopPID,
)
from . import monitoring

router = APIRouter(tags=["ui"])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def main_view(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/patterns", response_class=HTMLResponse)
async def patterns_view(request: Request):
    return templates.TemplateResponse("patterns.html", {"request": request})


@router.get("/settings", response_class=HTMLResponse)
async def settings_view(request: Request, kiln: Any = Depends(get_kiln)):
    # Fetch all current values
    try:
        # Check if kiln is KilnClient (async) or direct (sync)
        if hasattr(kiln, "get_all_settings") and asyncio.iscoroutinefunction(
            kiln.get_all_settings
        ):
            current_settings = await kiln.get_all_settings()
        else:
            current_settings = await asyncio.to_thread(
                lambda: {
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
            )
    except Exception as e:
        print(f"Error fetching settings: {e}")
        current_settings = {}

    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "settings": current_settings,
            "enums": {
                "ControlMethod": ControlMethod,
                "HeatingCoolingSelection": HeatingCoolingSelection,
                "SystemAlarmSetting": SystemAlarmSetting,
                "SettingLockStatus": SettingLockStatus,
                "PIDParameterSelection": PIDParameterSelection,
                "AnalogDecimalSetting": AnalogDecimalSetting,
                "ValveFeedbackSetting": ValveFeedbackSetting,
                "AutoTuningValveFeedback": AutoTuningValveFeedback,
                "TempUnit": TempUnit,
                "DecimalPointPosition": DecimalPointPosition,
                "ATSetting": ATSetting,
                "RunStopSetting": RunStopSetting,
                "StopSettingPID": StopSettingPID,
                "TemporarilyStopPID": TemporarilyStopPID,
            },
        },
    )


@router.post("/settings/update/{name}")
async def update_setting(name: str, request: Request, kiln: Any = Depends(get_kiln)):
    form_data = await request.form()
    value = form_data.get("value")
    if value is None:
        return {"status": "error", "message": "No value provided"}

    try:
        val_int = int(value)

        # Check if KilnClient (has generic set_setting)
        if hasattr(kiln, "set_setting") and asyncio.iscoroutinefunction(
            kiln.set_setting
        ):
            if name == "system_alarm":
                await kiln.set_system_alarm(val_int)
            elif name == "sensor_type":
                await kiln.set_sensor_type(val_int)
            else:
                await kiln.set_setting(name.replace("_", "-"), val_int)
            return {"status": "ok"}

        # Direct access (sync)
        if name == "system_alarm":
            await asyncio.to_thread(kiln.set_system_alarm_setting, val_int)
        elif name == "sensor_type":
            await asyncio.to_thread(kiln.set_sensor_type, val_int)
        else:
            method_name = f"set_{name}_setting"
            if hasattr(kiln, method_name):
                await asyncio.to_thread(getattr(kiln, method_name), val_int)
            else:
                fallback_name = name.replace("-", "_")
                method_name = (
                    f"set_{fallback_name}_display"
                    if "temp_unit" in name
                    else f"set_{fallback_name}"
                )
                if hasattr(kiln, method_name):
                    await asyncio.to_thread(getattr(kiln, method_name), val_int)
                else:
                    raise AttributeError(f"Kiln has no setter for {name}")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/partials/dashboard", response_class=HTMLResponse)
async def get_dashboard_partial(request: Request, kiln: Any = Depends(get_kiln)):
    try:
        # Fetch values
        if hasattr(kiln, "get_pv") and asyncio.iscoroutinefunction(kiln.get_pv):
            pv = await kiln.get_pv()
            setpoint = await kiln.get_setpoint()
            output1 = await kiln.get_output1()
            output2 = await kiln.get_output2()
            status = await kiln.get_executing_program_status()
            current_pattern = status.get("pattern")
            current_step = status.get("step")
            time_left_min = status.get("time_left_min")
            time_left_sec = status.get("time_left_sec")
            actual_steps = await kiln.get_actual_steps(current_pattern)
        else:
            data = await asyncio.to_thread(
                lambda: {
                    "pv": kiln.get_pv(),
                    "setpoint": kiln.get_setpoint(),
                    "output1": kiln.get_output_1_value(),
                    "output2": kiln.get_output_2_value(),
                    "pattern": kiln.get_executing_pattern_number(),
                    "step": kiln.get_executing_step_number(),
                    "time_left_min": kiln.get_step_time_left_min(),
                    "time_left_sec": kiln.get_step_time_left_sec(),
                }
            )
            pv = data["pv"]
            setpoint = data["setpoint"]
            output1 = data["output1"]
            output2 = data["output2"]
            current_pattern = data["pattern"]
            current_step = data["step"]
            time_left_min = data["time_left_min"]
            time_left_sec = data["time_left_sec"]
            actual_steps = await asyncio.to_thread(
                kiln.get_actual_step_number_setting, current_pattern
            )

        pv_color = calculate_color(pv, setpoint)
        time_left = f"{time_left_min}m {time_left_sec}s"

        # Recording status (imported from monitoring)
        is_recording = (
            monitoring.recording_task is not None
            and not monitoring.recording_task.done()
        )

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
                "actual_steps": actual_steps,
                "is_recording": is_recording,
            },
        )
    except Exception as e:
        print(f"Error fetching dashboard data: {e}")
        return HTMLResponse(
            f"<div class='error-msg' style='display:block'>Error: {str(e)}</div>"
        )


@router.get("/patterns/{id}/edit", response_class=HTMLResponse)
async def pattern_editor(id: int, request: Request):
    return templates.TemplateResponse(
        "pattern_editor.html", {"request": request, "pattern_id": id}
    )


@router.get("/pattern/{id}")
async def get_pattern_api(id: int, kiln: Any = Depends(get_kiln)):
    try:
        if hasattr(kiln, "get_pattern") and asyncio.iscoroutinefunction(
            kiln.get_pattern
        ):
            return await kiln.get_pattern(id)

        steps = []

        def fetch_steps():
            for step in range(8):
                temp, time_val = kiln.get_pattern_step(id, step)
                steps.append({"step": step, "temp": temp, "time": time_val})
            return steps

        await asyncio.to_thread(fetch_steps)
        return {"pattern_id": id, "steps": steps}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pattern/{id}/step/{step_id}")
async def set_pattern_step_api(
    id: int, step_id: int, req: PatternStepRequest, kiln: Any = Depends(get_kiln)
):
    try:
        if hasattr(kiln, "set_pattern_step") and asyncio.iscoroutinefunction(
            kiln.set_pattern_step
        ):
            return await kiln.set_pattern_step(id, step_id, req.temp, req.time)
        await asyncio.to_thread(kiln.set_pattern_step, id, step_id, req.temp, req.time)
        return {"status": "ok", "pattern": id, "step": step_id, "data": req}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pattern_start/update")
async def update_start_pattern(request: Request, kiln: Any = Depends(get_kiln)):
    form_data = await request.form()
    value = form_data.get("value")
    if value is not None:
        if hasattr(kiln, "set_start_pattern") and asyncio.iscoroutinefunction(
            kiln.set_start_pattern
        ):
            await kiln.set_start_pattern(int(value))
        else:
            await asyncio.to_thread(kiln.set_start_pattern_number, int(value))
    return await get_dashboard_partial(request, kiln=kiln)


@router.post("/pattern/{id}/actual-steps/update")
async def update_actual_steps(id: int, request: Request, kiln: Any = Depends(get_kiln)):
    form_data = await request.form()
    value = form_data.get("value")
    if value is not None:
        if hasattr(kiln, "set_actual_steps") and asyncio.iscoroutinefunction(
            kiln.set_actual_steps
        ):
            await kiln.set_actual_steps(id, int(value))
        else:
            await asyncio.to_thread(kiln.set_actual_step_number_setting, id, int(value))
    return await get_dashboard_partial(request, kiln=kiln)


@router.get("/api/recording")
async def get_recording_api():
    return await monitoring.get_current_recording()


@router.post("/recording/start")
async def start_recording_api(kiln: Any = Depends(get_kiln)):
    return await monitoring.start_recording(kiln=kiln)


@router.post("/recording/stop")
async def stop_recording_api():
    return await monitoring.stop_recording()
