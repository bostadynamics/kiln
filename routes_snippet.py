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

        return templates.TemplateResponse(
            "partials/dashboard.html",
            {
                "request": request,
                "pv": pv,
                "setpoint": setpoint,
                "output1": output1,
                "output2": output2,
                "pv_color": pv_color,
            },
        )
    except Exception as e:
        # Return error fragment or log
        print(f"Error fetching data: {e}")
        # Return a simple error div if fails
        return HTMLResponse(
            f"<div class='error-msg' style='display:block'>Error: {str(e)}</div>"
        )
