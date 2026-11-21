"""
dochat.main | 入口
"""

def main() -> None:
    from dochat.plugin import loads
    loads()
    
    from dochat.websocket.server import run
    import uvloop
    uvloop.run(run(port=12130))
