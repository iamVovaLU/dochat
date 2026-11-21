"""
dochat.plugin | 插件系统

插件化系统 注册/调用/管理/...
"""

from loguru import logger
from typing import Any, Callable, TypeVar
import importlib.util
from pathlib import Path

from dochat.con import Paths

# 插件与模块注册表
_plugins: dict[str, Callable[..., Any]] = {}
_modules: list[Any] = []

F = TypeVar("F", bound=Callable[..., Any])

def register(name: str | None = None) -> Callable[[F], F]:
    """注册插件"""
    def decorator(func: F) -> F:
        plugin_name = name or func.__name__
        _plugins[plugin_name] = func
        logger.opt(colors=True).info(
            "<blue>[@]</blue> register <green>+</green> : {}",
            f"{plugin_name}"
        )
        return func
    return decorator

def loads(
    path:Path|str=Paths.plugins
) -> None:
    """
    用于遍历plugins目录下所有.py并加载模块等使其所需部分注册为Plugin插件方法
    """
    for item in [item for item in Path(path).iterdir() if item.is_file() and item.suffix == ".py"]:
        spec = importlib.util.spec_from_file_location(item.name, item)
        if not spec is None and not spec.loader is None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            _modules.append([
                spec,module
            ])

def run_plugin(name: str, *args: Any, **kwargs: Any) -> Any:
    """调用已注册插件"""
    if name not in _plugins:
        raise KeyError(f"Plugin '{name}' does not exist")
    return _plugins[name](*args, **kwargs)

def list_plugins() -> list[str]:
    """列出已注册插件"""
    return list(_plugins.keys())
