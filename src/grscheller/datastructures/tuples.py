# Copyright 2023-2024 Geoffrey R. Scheller
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

"""
### Tuple based datastructures:

Tuple-like object with FP behaviors.

##### Tuple Types

* **ftuple:** Tuple-like object with FP behaviors

"""

from __future__ import annotations

from typing import Callable, cast, Iterable, Iterator, Optional
from grscheller.fp.iterables import FM, accumulate, concat, exhaust, merge

__all__ = ['ftuple', 'FT']

class ftuple[D]():
    """
    #### Functional Tuple

    * immutable tuple-like data structure with a functional interface
    * supports both indexing and slicing
    * `ftuple` addition & `int` multiplication supported
      * addition concatenates results, types must agree
      * both left and right multiplication supported

    """
    __slots__ = '_ds'

    def __init__(self, *dss: Iterable[D]) -> None:
        if len(dss) < 2:
            self._ds: tuple[D, ...] = tuple(*dss)
        else:
            msg = f'ftuple expected at most 1 argument, got {len(dss)}'
            raise TypeError(msg)

    def __iter__(self) -> Iterator[D]:
        return iter(self._ds)

    def __reversed__(self) -> Iterator[D]:
        return reversed(self._ds)

    def __bool__(self) -> bool:
        return bool(len(self._ds))

    def __len__(self) -> int:
        return len(self._ds)

    def __repr__(self) -> str:
        return 'FT(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return "((" + ", ".join(map(repr, self)) + "))"

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self._ds == other._ds

    def __getitem__(self, sl: slice|int) -> ftuple[D]|Optional[D]:
        if isinstance(sl, slice):
            return ftuple(self._ds[sl])
        try:
            item = self._ds[sl]
        except IndexError:
            item = None
        return item

    def foldL[L](self,
              f: Callable[[L, D], L],
              start: Optional[L]=None,
              default: Optional[L]=None) -> Optional[L]:
        """
        **Fold Left**

        * fold left with an optional starting value
        * first argument of function `f` is for the accumulated value
        * throws `ValueError` when `ftuple` empty and a start value not given

        """
        it = iter(self._ds)
        if start is not None:
            acc = start
        elif self:
            acc = cast(L, next(it))  # L = D in this case
        else:
            if default is None:
                msg = 'Both start and default cannot be None for an empty ftuple'
                raise ValueError('ftuple.foldL - ' + msg)
            acc = default
        for v in it:
            acc = f(acc, v)
        return acc

    def foldR[R](self,
              f: Callable[[D, R], R],
              start: Optional[R]=None,
              default: Optional[R]=None) -> Optional[R]:
        """
        **Fold Right**

        * fold right with an optional starting value
        * second argument of function `f` is for the accumulated value
        * throws `ValueError` when `ftuple` empty and a start value not given

        """
        it = reversed(self._ds)
        if start is not None:
            acc = start
        elif self:
            acc = cast(R, next(it))  # R = D in this case
        else:
            if default is None:
                msg = 'Both start and default cannot be None for an empty ftuple'
                raise ValueError('ftuple.foldR - ' + msg)
            acc = default
        for v in it:
            acc = f(v, acc)
        return acc

    def copy(self) -> ftuple[D]:
        """
        **Copy**

        Return a shallow copy of the ftuple in O(1) time & space complexity.

        """
        return ftuple(self)

    def __add__(self, other: ftuple[D]) -> ftuple[D]:
        return ftuple(concat(iter(self), other))

    def __mul__(self, num: int) -> ftuple[D]:
        return ftuple(self._ds.__mul__(num if num > 0 else 0))

    def __rmul__(self, num: int) -> ftuple[D]:
        return ftuple(self._ds.__mul__(num if num > 0 else 0))

    def accummulate[L](self, f: Callable[[L, D], L], s: Optional[L]=None) -> ftuple[L]:
        """
        **Accumulate partial folds**

        Accumulate partial fold results in an ftuple with an optional starting value.

        """
        if s is None:
            return ftuple(accumulate(self, f))
        else:
            return ftuple(accumulate(self, f, s))

    def map[U](self, f: Callable[[D], U]) -> ftuple[U]:
        return ftuple(map(f, self))

    def flatMap[U](self, f: Callable[[D], ftuple[U]], type: FM=FM.CONCAT) -> ftuple[U]:
        """
        **Bind function to ftuple**

        Bind function `f` to the `ftuple`.

        * type = CONCAT: sequentially concatenate iterables one after the other
        * type = MERGE: merge iterables together until one is exhausted
        * type = Exhaust: merge iterables together until all are exhausted

        """
        match type:
            case FM.CONCAT:
                return ftuple(concat(*map(lambda x: iter(x), map(f, self))))
            case FM.MERGE:
                return ftuple(merge(*map(lambda x: iter(x), map(f, self))))
            case FM.EXHAUST:
                return ftuple(exhaust(*map(lambda x: iter(x), map(f, self))))
            case '*':
                raise ValueError('Unknown FM type')

def FT[U](*ds: U) -> ftuple[U]:
    return ftuple(ds)

