"""
dochat.utils.judge | 判断与检查
"""

import json
from typing import Any

def is_json(text:str,re:bool=False) -> bool|dict[str,Any]:
    """
    Check whether a string is a parsable JSON
    检查一个字符串是否为可解析的JSON

    当re为True时如果成功就返回解析成功的字典
    否则只会返回bool值
    """
    s: str = text.strip()
    if not s or s[0] not in "{[" or s[-1] not in "}]":
        return False
    try:
        adict=json.loads(s)
        if re:
            return adict
        else:
            return True
    except json.JSONDecodeError:
        return False

# def is_legal(text:str) -> bool:
#     ...