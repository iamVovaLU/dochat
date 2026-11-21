def main() -> None:
    from dochat.websocket.server import run
    import uvloop
    uvloop.run(run(port=12130))
