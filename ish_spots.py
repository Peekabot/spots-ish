# ish_spots.py — run in iSH: python3 ish_spots.py
# GET /meta  GET /spots?since=  POST /tune  POST /ack

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

HOST, PORT = "0.0.0.0", 8000

ROWS = [
    {"ts": time.time() - 4, "src": "seed", "freq": 144390000, "mode": "APRS",
     "stage": "frame", "decoder": "direwolf", "crc_ok": True,
     "call_or_id": "N0CALL-9", "lat": 42.65, "lon": -73.76, "raw": "seed pos"},
    {"ts": time.time() - 20, "src": "seed", "freq": 144390000, "mode": "APRS",
     "stage": "frame", "decoder": "direwolf", "crc_ok": True,
     "call_or_id": "K1ABC-7", "lat": None, "lon": None, "raw": "no pos"},
    {"ts": time.time() - 30, "src": "seed", "freq": 144390000, "mode": "APRS",
     "stage": "demod", "decoder": "direwolf", "crc_ok": False,
     "call_or_id": None, "lat": None, "lon": None, "raw": "crc"},
]


def meta():
    last = max((r["ts"] for r in ROWS), default=0)
    stage = "—"
    for r in ROWS:
        if r["ts"] == last:
            stage = r.get("stage") or "—"
    coords = sum(1 for r in ROWS if r.get("crc_ok") and r.get("lat") is not None and r.get("lon") is not None)
    if not ROWS:
        gate = 3
    elif not coords:
        gate = 4
    else:
        gate = 5
    return {"spots": len(ROWS), "with_coord": coords, "last": last, "stage": stage, "gate": gate}


class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/meta":
            self._send(200, json.dumps(meta()))
            return
        if u.path == "/spots":
            q = parse_qs(u.query)
            since = float(q.get("since", ["0"])[0] or 0)
            lines = [json.dumps(r) for r in ROWS if r["ts"] > since]
            self._send(200, "\n".join(lines) + ("\n" if lines else ""), "application/jsonl")
            return
        self._send(404, json.dumps({"err": "nope"}))

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b"{}"
        u = urlparse(self.path)
        if u.path in ("/tune", "/ack"):
            self._send(200, json.dumps({"ok": True, "echo": raw.decode()[:200]}))
            return
        self._send(404, json.dumps({"err": "nope"}))


if __name__ == "__main__":
    print("spots on http://127.0.0.1:%d  GET /meta  GET /spots" % PORT)
    HTTPServer((HOST, PORT), H).serve_forever()
