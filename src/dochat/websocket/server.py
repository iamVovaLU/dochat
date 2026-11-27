"""
dochat.websocket.server | 处理客户端连接和业务处理
"""

from typing import (
    Any,
)
from loguru import logger
import json
import uuid
from picows.websockets import (
    Request,
    Response,
    ServerConnection,
    ServerHandshakeConnection,
    ConnectionClosedError,
    ConnectionClosedOK,
    serve,
)
#
from dochat.utils.judge import is_json
from dochat.errors import (
    ClientError,
    FormatError,
    UnknownError,
)
from dochat.plugin import run_plugin
from dochat.websocket.client import ClientsManager,ClientState,send_to



manager: ClientsManager = ClientsManager()

def process_request(
    conn: ServerHandshakeConnection,  # pyright: ignore[reportUnusedParameter]
    request: Request,  # pyright: ignore[reportUnusedParameter]
) -> Response | None:
    """
    用于处理 握手阶段
    (
        但是绝大多数身份和鉴定都得升级才能进行,
        所以握手阶段基本就是摆设,
        最多用来将封禁的IP踢出去,但只有运营过服务器的人才知道封IP屁用没有
    )
    """
    # conn.username = str(uuid.uuid4())
    return None


async def handler(ws: ServerConnection):
    """
    用于处理 握手连接后的处理/业务处理部分
    """
    # 连接后的注册
    id: str = uuid.uuid4().hex
    state: ClientState = ClientState(
        client_id=id,
        ws=ws,
        remote=str(ws.remote_address),
    )
    await manager.add(state)

    online = await manager.count()
    logger.opt(colors=True).info(
        "<green>[+]</green> Client-Connection({})\n    =| Online:{}",
        ws.username,
        online,
    )

    # 业务
    try:
        
        async for msg in ws:
            # if not (isinstance(msg, str) and is_json(text=msg)):
            #     raise FormatError("What the client sent is not a parsable JSON string.")
            # data = json.loads(msg)

            # return run_plugin(data[0], client, date[1])

            logger.info(  # [DEBUG] Print Message(在正式投入生产环境后不应PrintMessage)
                f"[↓] Client-Seed({len(msg)} Chars): [\n{msg[:50]}{'...' if len(msg) > 50 else ''}\n]"
            )
            ok: bool = await send_to(manager, state, msg)
            if not ok:
                break

    except ClientError as e:
        # 将因Client导致的错误发送给Client
        await ws.send(
            message=json.dumps(obj={"error": type(e).__name__, "message": str(e)})
        )
    except ConnectionClosedError as exc:  # 异常断开
        code = ws.close_code
        logger.warning(
            (
                f"[-][!] Client-abnormal-disconnect code={code} "
                f"rcvd={None if exc.rcvd is None else exc.rcvd.code} "
                f"sent={None if exc.sent is None else exc.sent.code}"
            )
        )
    except ConnectionClosedOK:  # 正常断开
        ...
        # 事实上到不到这里
        # 因为被'async for msg in ws'给吞掉了
        # 我也本不该写这个,我只是为了我日后看得懂
    except Exception:  # 兜底
        logger.exception("[X] Unexpected Error...")

    else:  # 正常结束/断开
        logger.opt(colors=True).info("<red>[-]</red> Expected-Client Reset")
    finally:  # 收尾工作
        _ = await manager.remove(id)
        logger.opt(colors=True).info("<red>[⌫]</red> Clear Client")


async def run(host: str = "localhost", port: int = 8765):
    async with serve(
        handler,
        host,
        port,
        process_request=process_request,
    ) as server:
        logger.opt(colors=True).info(
            "<yellow>[*]</yellow> ServerRunning <green>✔</green> : {}",
            f"\n    - {[sock.getsockname() for sock in server.sockets]}",
        )
        await server.serve_forever()

if __name__ == "__main__":
    import uvloop
    uvloop.run(run())
    # Glass Animals, IloveUSoFuckingMuch!