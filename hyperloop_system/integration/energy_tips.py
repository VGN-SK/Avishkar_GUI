import random
import time

CACHE_DURATION = 300  # 5 minutes
_cache = {"tip": None, "timestamp": 0}

ENERGY_TIPS = [   # Hardcoded as i wasnt able to find a suitable api
    "Optimize acceleration profiles to reduce peak power demand.",
    "Use regenerative braking to recover kinetic energy efficiently.",
    "Monitor levitation gap stability to prevent excess magnetic losses.",
    "Balance pod load distribution to improve propulsion efficiency.",
    "Reduce idle system components during docked states.",
    "Implement predictive battery management to extend lifecycle.",
    "Use adaptive speed control based on wind conditions.",
    "Schedule maintenance to avoid inefficient degraded components."
]


def get_energy_tip():

    global _cache

    if _cache["tip"] and time.time() - _cache["timestamp"] < CACHE_DURATION:
        return _cache["tip"]

    tip = random.choice(ENERGY_TIPS)

    _cache["tip"] = tip
    _cache["timestamp"] = time.time()

    return tip

