"""
dochat.con | 上下文

用于存放一些一些比如根路径等东西`
需要被多个包引用但每个包不好算得东西
"""

from pathlib import Path


class Paths:
    config: Path = Path(__file__).resolve().parent / "config.toml"
    #
    default: Path = Path(__file__).resolve().parent / "default"
    plugins: Path = Path(__file__).resolve().parent / "plugins"


if __name__ == "__main__":
    print(Paths.config)

