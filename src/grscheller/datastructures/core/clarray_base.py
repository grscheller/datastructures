# Copyright 2023 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module grscheller.datastructure.clarray_base - constant length array.

Module implementing a base class for fixed length O(1) array data structures.
    
None values are not allowed in this data structures. A default iterator is used
to swap out None values .ssigned or mapped to these data structures.
"""

from __future__ import annotations

__all__ = ['CLArrayBase']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Never, Union, Iterator
from itertools import chain, cycle
from .circular_array import CircularArray

class CLArrayBase():
    """Constant Length Array

    Base class for fixed length array data structure. None
    values
    are not permitted to be stored to these data structure. A default iterator
    can be defined to swap out None values if stored to the CLArray. If no such
    iterator is defined, or is exhausted, the data structure defaults back to an
    infinite iterator which supplies an infinite stream of empty tuples ().

    Unless specifically resized, this data structure is guaranteed to remain
    a fixed length.

    TODO: Elaborate on constructor values here, or figure out how to get pdoc
          to generate documentation from a constructor docstring.
    """
    def __init__(self, *ds,
                 size: int|None=None,
                 noneIter: Iterator|None=None,
                 noneSwap: Any|None=tuple()):

        match (noneIter, noneSwap):
            case (None, None):
                raise ValueError("noneIter & noneSwap both cannot be None")
            case (None, swap):
                self._none = cycle((swap,))
            case (none, None):
                self._none = none  # could throw StopIteration exception
            case (none, swap):
                self._none = chain(none, cycle((swap,)))

        ca = CircularArray()
        none = self._none

        for d in ds:
            if d is not None:
                ca.pushR(d)

        ds_size = len(ca)

        if size is None:
            abs_size = size = ds_size
        else:
            abs_size = abs(size)

        if abs_size > ds_size:
            if size > 0:
                # pad higher indexes (on "right")
                for _ in range(size-ds_size):
                    ca.pushR(next(none))
            else:
                # pad lower indexes (on "left")
                for _ in range(-size - ds_size):
                    ca.pushL(next(none))
        elif abs_size < ds_size:
            if size > 0:
                # ignore extra data at end
                for _ in range(size - ds_size):
                    ca.popR()
            else:
                # ignore extra data at beginning
                for _ in range(ds_size + size):
                    ca.popL()

        self._ca = ca

    def __iter__(self):
        """Iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in self._ca.copy():
            yield data

    def __reversed__(self):
        """Reverse iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in reversed(self._ca.copy()):
            yield data

    def __repr__(self):
        # TODO: rethink this one?
        repr1 = f'{self.__class__.__name__}('
        repr2 = ', '.join(map(repr, self))
        if repr2 == '':
            repr3 = f'noneIter={self._none})'
        else:
            repr3 = f', noneIter={self._none})'
        return repr1 + repr2 + repr3

    def __str__(self):
        return '[[[' + ', '.join(map(repr, self)) + ']]]'

    def __bool__(self):
        """Return true only if there exists an array value not equal to the
        empty tuple (). Empty arrays always return false.

        TODO: Default this to noneSwap value & noneSwap to ()
        """
        for value in self:
            if value != ():
                return True
        return False

    def __len__(self) -> int:
        """Returns the size of the CLArray"""
        return len(self._ca)

    def __getitem__(self, index: int) -> Union[Any,Never]:
        return self._ca[index]

    def __setitem__(self, index: int, value: Any) -> Union[None,Never]:
        if value is None:
            self._ca[index] = next(self._none)
        else:
            self._ca[index] = value

    def __eq__(self, other: Any):
        """Returns True if all the data stored in both compare as equal. Worst
        case is O(n) behavior for the true case. The default value play no role
        in determining equality.
        """
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

    def reverse(self) -> None:
        """Reverse the elements of the CLArray. Mutates the CLArray."""
        self._ca = self._ca.reverse()

if __name__ == "__main__":
    pass