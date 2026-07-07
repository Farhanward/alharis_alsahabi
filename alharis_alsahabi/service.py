"""Alharis Alsahabi SRE advisor as a local HTTP service.

``POST /api/scan`` accepts a service event
(``{"service", "error_rate", "latency_p95_ms", "cpu_percent", ...}``) and
returns OK/WARN/INCIDENT with Arabic findings — ready for monitoring hooks.
"""

from __future__ import annotations

from http.server import ThreadingHTTPServer
from typing import Any

from .engine import analyze_event
from .http_base import BaseServiceHandler, build_server


def _scan_route(data: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    event = data.get("event") if isinstance(data.get("event"), dict) else data
    if not event:
        return 400, {"ok": False, "error": "missing event payload"}
    return 200, {"ok": True, **analyze_event(event)}


class Handler(BaseServiceHandler):
    post_routes = {"/api/scan": staticmethod(_scan_route)}


def create_server(host: str | None = None, port: int | None = None) -> ThreadingHTTPServer:
    return build_server(Handler, host=host, port=port)


def run_server(host: str | None = None, port: int | None = None) -> None:
    from .version import __version__

    server = create_server(host=host, port=port)
    print(f"alharis service v{__version__}: http://{server.server_address[0]}:{server.server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
