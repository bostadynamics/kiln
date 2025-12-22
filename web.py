from delta_2 import (
    AnalogDecimalSetting,
    ATSetting,
    AutoTuningValveFeedback,
    ControlMethod,
    DecimalPointPosition,
    HeatingCoolingSelection,
    PIDParameterSelection,
    RunStopSetting,
    SettingLockStatus,
    StopSettingPID,
    SystemAlarmSetting,
    TemporarilyStopPID,
    TempUnit,
    ValveFeedbackSetting,
)
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from kiln_client import KilnClient

kiln = KilnClient("http://192.168.50.47:8000")
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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


@app.get("/settings", response_class=HTMLResponse)
async def settings_view(request: Request):
    # Fetch all current values
    try:
        current_settings = await kiln.get_all_settings()
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


@app.post("/settings/update/{name}")
async def update_setting(name: str, request: Request):
    form_data = await request.form()
    value = form_data.get("value")
    if value is None:
        return {"status": "error", "message": "No value provided"}

    # Special handling for names if needed, but client has generic `set_setting`
    # Our API has /setting/{name} for most, but some are different.
    # Let's map them.
    try:
        if name == "system_alarm":
            await kiln.set_system_alarm(int(value))
        elif name == "sensor_type":
            await kiln.set_sensor_type(int(value))
        else:
            await kiln.set_setting(name.replace("_", "-"), int(value))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/partials/dashboard", response_class=HTMLResponse)
async def get_dashboard_partial(request: Request):
    # Fetch values
    try:
        pv = await kiln.get_pv()
        setpoint = await kiln.get_setpoint()
        output1 = await kiln.get_output1()
        output2 = await kiln.get_output2()

        pv_color = calculate_color(pv, setpoint)

        # Fetch status
        # Note: KilnClient returns a dict with pattern, step, time_left_min, time_left_sec
        status = await kiln.get_executing_program_status()
        current_pattern = status.get("pattern")
        current_step = status.get("step")
        time_left = f"{status.get('time_left_min')}m {status.get('time_left_sec')}s"

        # Fetch settings for the UI to know what can be edited
        # start_pattern = await kiln.get_start_pattern()
        actual_steps = await kiln.get_actual_steps(current_pattern)

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
                # "start_pattern": start_pattern,
                "actual_steps": actual_steps,
            },
        )
    except Exception as e:
        # Return error fragment or log
        print(f"Error fetching data: {e}")
        # Return a simple error div if fails
        return HTMLResponse(
            f"<div class='error-msg' style='display:block'>Error: {str(e)}</div>"
        )


@app.get("/patterns/{id}/edit", response_class=HTMLResponse)
async def pattern_editor(id: int, request: Request):
    return templates.TemplateResponse(
        "pattern_editor.html", {"request": request, "pattern_id": id}
    )


@app.get("/pattern/{id}")
async def get_pattern_api(id: int):
    return await kiln.get_pattern(id)


from pydantic import BaseModel


class PatternStepRequest(BaseModel):
    temp: float
    time: int


@app.post("/pattern/{id}/step/{step_id}")
async def set_pattern_step_api(id: int, step_id: int, req: PatternStepRequest):
    return await kiln.set_pattern_step(id, step_id, req.temp, req.time)


@app.post("/pattern_start/update")
async def update_start_pattern(request: Request):
    form_data = await request.form()
    value = form_data.get("value")
    if value is not None:
        await kiln.set_start_pattern(int(value))
    return await get_dashboard_partial(request)


@app.post("/pattern/{id}/actual-steps/update")
async def update_actual_steps(id: int, request: Request):
    form_data = await request.form()
    value = form_data.get("value")
    if value is not None:
        await kiln.set_actual_steps(id, int(value))
    return await get_dashboard_partial(request)
