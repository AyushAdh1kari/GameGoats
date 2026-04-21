import os

import requests


API_BASE = os.getenv("GAMEGOATS_API_BASE", "http://web-api:4000")


def _build_url(path):
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{API_BASE}{path}"


def api_request(method, path, payload=None, timeout=10):
    try:
        response = requests.request(
            method=method,
            url=_build_url(path),
            json=payload,
            timeout=timeout,
        )
    except requests.exceptions.RequestException as exc:
        return None, f"API request failed: {exc}", None

    data = None
    if response.content:
        try:
            data = response.json()
        except ValueError:
            data = response.text

    if response.ok:
        return data, None, response.status_code

    if isinstance(data, dict) and data.get("error"):
        error_message = data["error"]
    else:
        error_message = f"Request failed with status {response.status_code}"

    return data, error_message, response.status_code


def get_json(path, timeout=10):
    return api_request("GET", path, timeout=timeout)


def post_json(path, payload, timeout=10):
    return api_request("POST", path, payload=payload, timeout=timeout)


def put_json(path, payload, timeout=10):
    return api_request("PUT", path, payload=payload, timeout=timeout)


def delete_json(path, payload=None, timeout=10):
    return api_request("DELETE", path, payload=payload, timeout=timeout)
