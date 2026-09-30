# spots_webview.py — Pythonista
# iSH: python3 ish_spots.py
# this loads http://127.0.0.1:8000/

import ui

URL = "http://127.0.0.1:8000/"

v = ui.WebView()
v.flex = "WH"
v.scales_page_to_fit = False
v.load_url(URL)
v.present("fullscreen")
