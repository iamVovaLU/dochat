from tomlkit.toml_document import TOMLDocument
from tomlkit.exceptions import NonExistentKey
#
import tomlkit
#
from dochat.con import Paths


class Config:
    """
    Config | 配置
    基于同目录下的config.toml文件
    """
    class Server:
        host:None|str = None
        port:None|str = None

def load():
    while True:
        # if Paths.config.is_file():
        try:
            with open(Paths.config,"r",encoding='utf-8') as f:
                doc: TOMLDocument = tomlkit.load(f)
            Config.Server.host = doc["server"]["host"]
            Config.Server.port = doc["server"]["port"]
            break
        except (FileNotFoundError,NonExistentKey):
            with open(Paths.default / "config.toml","r",encoding='utf-8') as f:
                config: str = f.read()
            with open(Paths.config,"w",encoding='utf-8') as f:
                _ = f.write(config)

if __name__ == "__main__":
    load()