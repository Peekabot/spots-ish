# spots-ish

iSH serves the map page and the spots wire. Pythonista WebView is the window. Remote WebSDR is the iframe waterfall.

```
GET  /
GET  /meta
GET  /spots?since=<ts>
POST /tune
POST /ack
```

## iSH

```
git pull
python3 ish_spots.py
```

## Pythonista

Run `spots_webview.py` — loads `http://127.0.0.1:8000/`
