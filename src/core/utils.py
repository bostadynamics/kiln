# src/core/utils.py


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
