"""
dochat.utils.totp | 0依赖的TOTP实现
"""

import secrets
import base64
import hashlib
import hmac
import struct
import time
from typing import Any


def generate_key() -> str:
    """
    generate TOTP Secret Key

    随机生成一个TOTP共享密钥
    """
    return base64.b32encode(secrets.token_bytes(20)).decode('utf-8')

def generate_totp_code(
        secret_key:str|bytes,
        digits:int=6,
        step:int=30,
        for_time:float|None=None,
        algo:Any=hashlib.sha1
    ) -> str:
    r"""
    generate totp code based on a Secret Key

    基于TOTP共享密钥生成TOTP码

    secret_key:
        - str
            传入base32字符串,比如'4JYPLTFS6VJAID5FTDHMBTOJAICKU22V'(UTF-8)
        - bytes
            传入字节,比如由'secrets.token_bytes(20)'生成的"b'\xc8\xd3\xa7\xd4\n\xe3\x1b7\x08y\x04\xb0\x84\x88\xc9\xb4\x92\xefD\xa5'"
    digits:
        - int
            位数,比如 021083 就是6位
    step:
        - int
            间隔/时间间隔,也是这个TOTP-CODE的最大有效时间/每多少间隔需要用新的
    for_time:
        - float[TEST]
            指定时间,传入Unix秒时间戳(float)
        - None
            使用此刻时间
    algo:
        - Any
            使用的Hash算法
            传给 hmac.new 的 digestmod,可以写比如 hashlib.sha1 / hashlib.sha256 / hashlib.md5 / ...
            只要hmac.new 的 digestmod可用且允许即可
            比如传入'hashlib.sha1'就是使用sha1算法,一般情况下使用'hashlib.sha1'
            (这里之所以类型是Any因为'hashlib.sha1'不好写类型注解)
    """
    if isinstance(secret_key, str):
        key_bytes: bytes = base64.b32decode(secret_key)
    else:
        key_bytes = secret_key
    
    t: float = time.time() if for_time is None else for_time
    msg: bytes = struct.pack(">Q",int(t//step))
    digest: bytes = hmac.new(
        key_bytes,
        msg,
        algo
    ).digest()
    offset: int = digest[-1] & 0x0F
    code_int: int = struct.unpack(">I", digest[offset:offset+4])[0] & 0x7FFFFFFF
    code: str = str(code_int % (10 ** digits)).zfill(digits)
    return code

if __name__ == "__main__":
    key = generate_key()
    code = generate_totp_code(key)
    print(key,code,code==generate_totp_code(key))
    # DeepSeek NB