# spots_webview.py — Pythonista
# iSH first: python3 ish_spots.py
# Then run this.

import json
import socket
import threading
import time
import ui

HOST = "127.0.0.1"
PORT = 8000
URL = "http://%s:%d/" % (HOST, PORT)


def http_get(path, timeout=2.0):
    s = socket.create_connection((HOST, PORT), timeout=timeout)
    s.settimeout(timeout)
    try:
        req = "GET {} HTTP/1.0\r\nHost: {}:{}\r\nConnection: close\r\n\r\n".format(
            path, HOST, PORT
        )
        s.sendall(req.encode())
        buf = bytearray()
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
    finally:
        s.close()
    sep = bytes(buf).find(b"\r\n\r\n")
    if sep < 0:
        return None
    return bytes(buf[sep + 4:])


class SpotsApp(ui.View):
    def __init__(self):
        ui.View.__init__(self)
        self.flex = "WH"
        self.bg_color = "#111111"
        self._run = True
        self._ok = False

        self.hdr = ui.Label()
        self.hdr.text = "waiting for iSH :8000"
        self.hdr.text_color = "#e0b44a"
        self.hdr.font = ("Menlo", 12)
        self.hdr.number_of_lines = 2
        self.add_subview(self.hdr)

        self.reload_btn = ui.Button()
        self.reload_btn.title = "reload"
        self.reload_btn.font = ("Menlo", 12)
        self.reload_btn.tint_color = "#7dce82"
        self.reload_btn.action = self._reload
        self.add_subview(self.reload_btn)

        self.web = ui.WebView()
        self.web.scales_page_to_fit = False
        self.add_subview(self.web)

        threading.Thread(target=self._pump, daemon=True).start()

    def layout(self):
        w, h = self.width, self.height
        self.hdr.frame = (8, 8, w - 88, 36)
        self.reload_btn.frame = (w - 76, 8, 68, 36)
        self.web.frame = (0, 48, w, h - 48)

    def will_close(self):
        self._run = False

    def _reload(self, _sender=None):
        self.web.load_url(URL)

    def _set_hdr(self, text, ok):
        def paint():
            self.hdr.text = text
            self.hdr.text_color = "#7dce82" if ok else "#e0b44a"

        ui.delay(paint, 0)

    def _pump(self):
        while self._run:
            try:
                raw = http_get("/meta")
                meta = json.loads(raw.decode()) if raw else {}
                line = "spots:{spots}  coord:{with_coord}  gate:{gate}  {stage}".format(
                    spots=meta.get("spots", 0),
                    with_coord=meta.get("with_coord", 0),
                    gate=meta.get("gate", "-"),
                    stage=meta.get("stage", "-"),
                )
                self._set_hdr(line, True)
                if not self._ok:
                    self._ok = True
                    ui.delay(self._reload, 0)
            except Exception as e:
                self._ok = False
                self._set_hdr("iSH down  " + type(e).__name__, False)
            time.sleep(2)


if __name__ == "__main__":
    SpotsApp().present("fullscreen")
