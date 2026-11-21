import json

def is_json(text:str) -> bool:
    """
    Check whether a string is a parsable JSON
    检查一个字符串是否为可解析的JSON
    """
    s: str = text.strip()
    if not s or s[0] not in "{[" or s[-1] not in "}]":
        return False
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False