"""
dochat.errors | 自定错误

一些自定义的错误
"""


class DoChatError(Exception):
    """DoChatError(这个项目)所有的自定义报错的基类"""

# ---- Client
class ClientError(DoChatError):
    """因客户端(的行为)产生的报错"""

class FormatError(ClientError):
    """
    格式错误
    如客户端发送了字符串但不是可解析的JSON文本
    (服务器强制要求所有字符串都得是可被解析的JSON文本)
    """

class TimeoutError(ClientError):
    """
    超时 | 原: ArrogantClientError

    蔑视与拒绝在规定时间内向服务器发送如 登录注册 ... 信息
    总之...不登就滚
    """

class IdentityError(ClientError):
    """
    客户端登录时的信息是错误的
    """
#
class TOTPCodeError(IdentityError):
    """
    TOTPCode信息错误或过期
    """
class UserIDError(IdentityError):
    """
    不存在的UserUUID | 查无此人 :/
    """

class MaliciousClientError(ClientError):
    """
    恶意客户端 | 原: AssholeClientError

    包括不限于
        - 非人般的速度
        - 便秘般的庞大数据
        - ...
    """
