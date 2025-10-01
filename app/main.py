import os
import sys
from typing import Any, Dict

import requests

BASE_URL = "http://api.weatherapi.com/v1"
ENDPOINT = "/current.json"
CITY = "Paris"
REQUEST_TIMEOUT = 10  # seconds


def get_api_key() -> str:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing API_KEY environment variable. "
            "Set API_KEY with your WeatherAPI key."
        )
    return api_key


def fetch_current_weather(api_key: str) -> Dict[str, Any]:
    url = f"{BASE_URL}{ENDPOINT}"
    params = {"key": api_key, "q": CITY}
    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def print_paris_weather(payload: Dict[str, Any]) -> None:
    location = payload.get("location", {})
    current = payload.get("current", {})
    condition = (current.get("condition") or {}).get("text", "n/a")

    line = (
        f"{location.get('name', 'Paris')}, {location.get('country', '')}: "
        f"{current.get('temp_c', 'n/a')}°C "
        f"(feels {current.get('feelslike_c', 'n/a')}°C), "
        f"{condition}. Humidity {current.get('humidity', 'n/a')}%, "
        f"wind {current.get('wind_kph', 'n/a')} kph."
    )
    print(line)


def main() -> int:
    try:
        api_key = get_api_key()
        data = fetch_current_weather(api_key)
        print_paris_weather(data)
        return 0
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response else "N/A"
        print(f"HTTP error: {status} {exc}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
