import functools
from typing import Any
import time
# from tinty import colored as c, RED, GREEN, BLUE, CYAN, DIM
from loguru import logger

def time_consuming(func:Any) -> Any:
    """
    用于测试代码执行耗时
    """
    @functools.wraps(func)
    def wrapper(*args:Any, **kwargs:Any) -> Any:
        time_a = time.perf_counter()
        result = func(*args, **kwargs)
        time_b = time.perf_counter()
        # print(f"time_consuming[{func.__name__}]: {round((time_b-time_a)*1000,5)}ms | result:{result}")
        # print(
        #     "\n"
        #     + (c("[TEST]") | BLUE)
        #     + " "
        #     + (c("time_consuming") | RED)
        #     + "[ "
        #     + (c(func.__name__) | CYAN)
        #     + " ]"
        #     + "\n   - "
        #     + (c(f"{round((time_b-time_a)*1000,5)}ms") | GREEN)
        #     + " | "
        #     + (c("result:") | DIM)
        #     + (c(f"{result}") | DIM | BLUE)
        # )
        logger.opt(colors=True).info(
            (
                "<blue>[TEST]</blue> <red>time_consuming</red>[ <cyan>{}</cyan> ]\n"
                "   - <green>{}ms</green> | <dim>result:</dim> <dim><blue>{}</blue></dim>"
            ),
            func.__name__,
            round((time_b - time_a) * 1000, 5),
            result,
        )
        return result
    return wrapper

if __name__ == "__main__":
    @time_consuming
    def test():
        return None
    test()
    