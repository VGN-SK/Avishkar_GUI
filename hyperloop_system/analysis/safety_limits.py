from typing import Dict, List



# SAFETY LIMIT COMPUTATION - COMBINING WEATHER AND TELEMETRY DATA HERE 

def compute_safety_limits(
    telemetry: Dict,
    weather: Dict
) -> Dict:
    """
    Combines telemetry and weather data
    to determine safety status.
    """

    alerts: List[str] = []
    severity = "normal"

    velocity = float(telemetry["velocity"])
    current = float(telemetry["current"])
    voltage = float(telemetry["voltage"])
    gap = float(telemetry["levitation_gap"])  # CURRENTLY USING ONLY ONE LEVITATION GAP INSTEAD OF 4 ON EACH CORNER ... WILL UPDATE IT IN FUTURE AND CHANGE CONDITIONS
    temperature = float(telemetry["temperature"])
    battery = float(telemetry["battery"])

    avg_wind = weather["avg_wind_speed"]
    rain = weather["rain_detected"]

    # SAFE VELOCITY BASELINE

    safe_velocity = 350  # base safe limit (m/s) - USED IN M/S ITSELF COZ MY ODOMETRY DATA IS ASSUMED TO BE IN METRES AND TRACK MODEL IS CODED ON THAT 

    # Reduce safe velocity if wind high
    if avg_wind > 15:
        safe_velocity -= 100

    if avg_wind > 25:
        safe_velocity -= 200

    # Rain reduces safe velocity slightly
    if rain:
        safe_velocity -= 50

 
    # CHECK ACTUAL VELOCITY AND PRODUCE NECESSARY ALARMS

    if velocity > safe_velocity:
        alerts.append("Velocity exceeds safe limit")
        severity = escalate(severity, "warning")

    # LEVITATION GAP CHECK

    if gap < 10:
        alerts.append("Levitation gap too low")
        severity = escalate(severity, "critical")

    if gap > 15:
        alerts.append("Levitation gap too high")
        severity = escalate(severity, "warning")

    # CURRENT OVERLOAD

    if current > 600:
        alerts.append("Electrical current overload")
        severity = escalate(severity, "critical")

    # TEMPERATURE CHECK

    if temperature > 60:
        alerts.append("Motor temperature high")
        severity = escalate(severity, "warning")

    # BATTERY CHECK

    if battery < 25:
        alerts.append("Battery level low")
        severity = escalate(severity, "warning")

    return {
        "safe_velocity": safe_velocity,
        "alerts": alerts,
        "severity": severity
    }



# SEVERITY ESCALATION FUNCTION

def escalate(current_level: str, new_level: str) -> str:
    """
    Escalates severity level.
    Levels: normal < warning < critical
    """

    order = ["normal", "warning", "critical"]

    return order[max(order.index(current_level), order.index(new_level))]

