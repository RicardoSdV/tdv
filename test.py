from typing import Callable


def myFunc():
    return 1

ans: int = myFunc()

myfunc: Callable = myFunc

ans2 = myfunc()

print(ans, ans2)
