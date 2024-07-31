from itertools import islice, repeat
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *


class IPL:
    """
    In Place List

    If you have a list which is constantly getting populated with about the same number of
    elements instead of creating & deleting a bunch of lists all the time use this which will
    scale up to the max number of entries & then never shrink again. It is more memory friendly.
    """
    __slots__ = ('_idx', '_list', '_len_list', '_init_len')

    def __init__(self, init_len: int = 8) -> None:
        # It can be -ve though if you need an empty list that resizes by a custom amount at first
        assert init_len != 0, 'Length cannot be 0 bc *2 for resize'

        self._list: 'List[Any]' = [None] * init_len  # Yes, composition faster than inheritance
        self._init_len = init_len
        self._len_list = init_len  # Yes, faster than len()
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
