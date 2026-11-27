from typing import Any
from asyncio.locks import Lock
from dataclasses import dataclass
from picows.websockets import ServerConnection
from rstypes import RMap
import asyncio

@dataclass
class ClientState:
    client_id: str
    ws: ServerConnection
    remote: str

class ClientsManager:
    def __init__(self) -> None:
        self._clients: dict[str, ClientState] = {}
        self._lock: Lock = asyncio.Lock()
        self._send_locks: RMap = RMap(factory=asyncio.Lock)

    async def add(self, state: ClientState) -> None:
        """
        添加客户端
        """
        async with self._lock:
            self._clients[state.client_id] = state

    async def remove(self, client_id: str) -> ClientState | None:
        """
        注销客户端
        """
        async with self._lock:
            state: ClientState | None = self._clients.pop(client_id, None)
        if state:
            await self._send_locks.pop(key=client_id)
        return state

    async def snapshot(self) -> list[ClientState]:
        """
        返回当前所有客户端状态的快照副本
        """
        async with self._lock:
            return list[ClientState](self._clients.values())

    async def count(self) -> int:
        """
        返回当前在线客户端数量
        """
        async with self._lock:
            return len(self._clients)
    
    async def get_send_lock(self, client_id: str) -> Lock:
        """
        获取指定客户端的发送锁
        不存在则创建
        """
        lock: Any | None = await self._send_locks.get(key=client_id)
        if lock is None:
            lock = asyncio.Lock()
            await self._send_locks.set(key=client_id, value=lock)
        return lock

async def send_to(manager: ClientsManager, state: ClientState, data: str | bytes) -> bool:
    """
    向指定客户端发送数据
    同一连接的发送操作串行执行
    """
    lock: Lock = await manager.get_send_lock(state.client_id)
    try:
        async with lock:
            await state.ws.send(data)
        return True
    except Exception:
        return False