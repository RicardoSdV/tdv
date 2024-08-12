from itertools import islice, repeat
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *


class IPL:
    """ In Place List. Inits a list of Nones. To add, overwrites elements. When full, doubles.
    On reset, yields added elements. On clear, creates new list of Nones. """

    __slots__ = ('_list', '_len_list', '_init_len', '_idx')

    def __init__(self, init_len: int = 8) -> None:
        assert init_len < 1, 'Length cannot be < 0 bc *2 for resize'

        self._list: 'List[Any]' = [None] * init_len  # Yes, composition faster than inheritance
        self._len_list = init_len  # Yes, faster than len()
        self._init_len = init_len
        self._idx = -1

    def append(self, element: 'Any') -> None:
        self._idx += 1
        try:
            self._list[self._idx] = element
        except IndexError:
            self._len_list *= 2
            self._list.extend(repeat(None, self._len_list))
            self._list[self._idx] = element

    def reset(self) -> 'Iterator[Any]':
        yield from islice(self._list, self._idx+1)
        self._idx = -1

    def clear(self) -> None:
        self._list = [None] * self._init_len
        self._len_list = self._init_len
        self._idx = -1
