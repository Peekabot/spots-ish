# spots-ish

iSH HTTP server for the spots wire.

```
GET  /meta
GET  /spots?since=<ts>
POST /tune
POST /ack
```

## iSH

```
git clone https://github.com/Peekabot/spots-ish.git
cd spots-ish
python3 ish_spots.py
```

Listens on `0.0.0.0:8000`. Pythonista client hits `127.0.0.1:8000`.

See `spots_proto.md`.
