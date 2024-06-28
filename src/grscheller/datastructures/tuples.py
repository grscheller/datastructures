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

"""Extending Python's Immutable builtin Tuple data structure with
a functional interfaces.

Types of Tuples:

* class **FTuple**: extend builtin tuple with functional interface
"""

from __future__ import annotations

__all__ = ['FTuple']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Any, Callable, Iterator, Generic, Optional, TypeVar
from itertools import accumulate, chain
from .core.iterlib import exhaust, merge

_T = TypeVar('_T')
_S = TypeVar('_S')

class FTuple(Generic[_T]):
    """Class implementing a Tuple-like object with FP behaviors."""
    __slots__ = '_tuple'

    def __init__(self, *ds: _T):
        """Initialize a Tuple-like object with functional methods.

        * Null values are not permitted in this data structure

        """
        self._tuple = tuple(filter(lambda d: d is not None, ds))

    def __iter__(self) -> Iterator[_T]:
        return iter(self._tuple)

    def __repr__(self) -> str:
        return 'FTuple(' + ', '.join(map(repr, self)) + ')'

    def __bool__(self) -> bool:
        return bool(len(self._tuple))

    def __str__(self) -> str:
        """Display data in the `FTuple`."""
        return "((" + ", ".join(map(repr, self)) + "))"

    def __getitem__(self, sl: slice|int) -> FTuple[_T]|Optional[_T]:
        """Supports both indexing and slicing."""
        if isinstance(sl, slice):
            return FTuple(*self._tuple[sl])
        try:
            item = self._tuple[sl]
        except IndexError:
            item = None
        return item

    def foldL1(self, f: Callable[[_S, _T], _S], init: _S) -> _S:
        """Fold left with an initial value.

        * first argument of `f` is for the accumulated value
        * if empty, return the initial value

        """
        value = init
        for v in self:
            value = f(value, v)
        return value

    def foldR1(self, f: Callable[[_T, _S], _S], init: _S) -> _S:
        """Fold right with an initial value.

        * second argument of `f` is for the accumulated value
        * if empty, return the initial value

        """
        value = init
        for v in self:
            value = f(v, value)
        return value

    def copy(self) -> FTuple[_T]:
        """Return shallow copy of the `FTuple` in O(1) time & space complexity."""
        return FTuple(*self)

    def map(self, f: Callable[[_T], _S]) -> FTuple[_S]:
        return FTuple(*map(f, self))

    def __add__(self, other: FTuple[_T]) -> FTuple[_T]:
        """Concatenate two `FTuples`."""
        return FTuple(*chain(iter(self), other))

    def __mul__(self, num: int) -> FTuple[_T]:
        """Return an `FTuple` which repeats another `FTuple` `num` times."""
        return FTuple(*self._tuple.__mul__(num if num > 0 else 0))


    # def accummulate(self, f: Callable[[Any, Any], Any], initial: Any) -> FP[Any]:
    #     """Accumulate partial fold results in same type data structure.

    #     Works best for variable sized containers.

    #     """
    #     # Probably need a subtype of fp[_S]
    #     return type(self)(*accumulate(chain((initial,), self), f))

    # # Default implementations for FIFO data structures,
    # # see stacks module for LIFO examples.

    # def flatMap(self, f: Callable[[Any], FP[Any]]) -> FP[Any]:
    #     """Monadically bind `f` to the data structure sequentially."""
    #     return type(self)(*chain(*map(iter, map(f, self))))

    # def mergeMap(self, f: Callable[[Any], FP[Any]]) -> FP[Any]:
    #     """Monadically bind `f` to the data structure, merge until one exhausted."""
    #     return type(self)(*merge(*map(iter, map(f, self))))

    # def exhaustMap(self, f: Callable[[Any], FP[Any]]) -> FP[Any]:
    #     """Monadically bind `f` to the data structure, merge until all are exhausted."""
    #     return type(self)(*exhaust(*map(iter, map(f, self))))
