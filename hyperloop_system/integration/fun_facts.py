import requests
import time

CACHE_DURATION = 600  # 10 minutes
_cache = {"fact": None, "timestamp": 0}


def get_fun_fact():

    global _cache

    if _cache["fact"] and time.time() - _cache["timestamp"] < CACHE_DURATION:
        return _cache["fact"]

    try:
        response = requests.get(
            "https://uselessfacts.jsph.pl/random.json?language=en",   # using a facts api
            timeout=5
        )
        response.raise_for_status()

        data = response.json()

        fact = data["text"]

        _cache["fact"] = fact
        _cache["timestamp"] = time.time()

        return fact

    except Exception:
        return "Hyperloop systems aim to reduce energy per passenger-km dramatically."

