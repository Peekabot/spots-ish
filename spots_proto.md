# spots wire — CRT pattern, SDR payload

iSH or Orin is the server. Pythonista is the display.
Same as /frame + /joy. Slower. Text body.

    GET  /spots?since=<ts>   → JSONL (only rows with ts > since)
    GET  /meta               → one JSON object, header bar
    POST /tune               → {"src","freq","mode"}   optional
    POST /ack                → {"ts": <last seen>}     optional

## /meta
```json
{"spots": 5, "with_coord": 2, "last": 1730000000.1, "stage": "frame", "gate": 5}
```
gate: 3 = no rows, 4 = rows but no coords, 5 = at least one pin.

## /spots line
```json
{"ts": 1730000000.1, "src": "rtl", "freq": 144390000, "mode": "APRS",
 "stage": "frame", "decoder": "direwolf", "crc_ok": true,
 "call_or_id": "N0CALL-9", "lat": 42.65, "lon": -73.76, "raw": "..."}
```
stage: energy | demod | frame | coord
pin on client: crc_ok == true AND lat != null AND lon != null

## cadence
Poll /meta every 2s. If last changed, GET /spots?since=last_drawn.
Do not PNG-encode. Do not 15Hz.

## bind
HOST 127.0.0.1:8000  (same as CRT stub)
If iSH is the server, Pythonista uses that. Orin later: same paths, other host.
