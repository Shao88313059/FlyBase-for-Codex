#!/usr/bin/env python3
"""Small helper for checking FlyBase API endpoints.

This script intentionally does not guess endpoint paths. Pass a path copied
from the official OpenAPI document or Swagger UI.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = "https://api.flybase.org/api/v1.0/"


def build_url(path: str, params: list[str]) -> str:
    path = path.strip()
    if path.startswith("http://") or path.startswith("https://"):
        url = path
    else:
        url = urllib.parse.urljoin(BASE_URL, path.lstrip("/"))

    query: dict[str, str] = {}
    for item in params:
        if "=" not in item:
            raise SystemExit(f"Bad parameter {item!r}; use key=value.")
        key, value = item.split("=", 1)
        query[key] = value
    if query:
        separator = "&" if urllib.parse.urlparse(url).query else "?"
        url = url + separator + urllib.parse.urlencode(query)
    return url


def fetch_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"HTTP {exc.code} for {url}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not reach {url}: {exc.reason}") from exc

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Response from {url} was not JSON: {exc}") from exc


def compact(value: object, max_items: int = 8) -> object:
    if isinstance(value, dict):
        return {key: compact(val, max_items) for key, val in list(value.items())[:max_items]}
    if isinstance(value, list):
        return [compact(item, max_items) for item in value[:max_items]]
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a confirmed FlyBase API endpoint.")
    parser.add_argument("mode", choices=["get", "raw"], help="Use get for compact JSON or raw for full JSON.")
    parser.add_argument("path", help="Endpoint path such as /species or a full URL.")
    parser.add_argument("--param", action="append", default=[], help="Query parameter as key=value.")
    args = parser.parse_args()

    url = build_url(args.path, args.param)
    data = fetch_json(url)
    output = data if args.mode == "raw" else compact(data)
    print(json.dumps({"url": url, "data": output}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
