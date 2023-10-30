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

"""Module grscheller.datastructure.dqueue - Double sided queue

Double sided queue with amortized O(1) insertions & deletions from either end.
Obtaining length (number of elements) of a Dqueue is also a O(1) operation.

Implemented with a Python List based circular array.
"""

from __future__ import annotations

__all__ = ['Dqueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Self
from itertools import chain
from .core.iterlib import mergeIters, exhaustIters
from .core.carray import Carray

class Dqueue():
    """Double sided queue datastructure. Will resize itself as needed.

    The Dqueue class consistently uses None to represent the absence of a value.
    None will not be pushed to this data structure. As an alternative, use Maybe
    objects of type Nothing, or the empty tuple () to represent a non-existent
    value. 
    """
    def __init__(self, *ds):
        """Construct a double sided queue data structure.

        Null values will be culled from the intial data from ds.
        """
        self._carray = Carray()
        for d in ds:
            if d is not None:
                self._carray.pushR(d)

    def __bool__(self) -> bool:
        """Returns true if dqueue is not empty."""
        return len(self._carray) != 0

    def __len__(self) -> int:
        """Returns current number of values in dqueue."""
        return len(self._carray)

    def __iter__(self):
        """Iterator yielding data currently stored in dqueue.

        Data yielded in left-to-right order.
        """
        currCarray = self._carray.copy()
        for pos in range(len(currCarray)):
            yield currCarray[pos]

    def __reversed__(self):
        """Reverse iterate over the current state of the dqueue.
        
        Data yielded in right-to-left order.
        """
        for data in reversed(self._carray.copy()):
            yield data

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False
        return self._carray == other._carray

    def __repr__(self):
        """Display data in dqueue."""
        dataListStrs = []
        for data in self._carray:
            dataListStrs.append(repr(data))
        return ">< " + " | ".join(dataListStrs) + " ><"

    def copy(self) -> Dqueue:
        """Return shallow copy of the dqueue in O(n) time & space complexity."""
        new_dqueue = Dqueue()
        new_dqueue._carray = self._carray.copy()
        return new_dqueue

    def pushR(self, *ds: Any) -> Dqueue:
        """Push data on rear of dqueue & return reference to self."""
        for d in ds:
            if d != None:
                self._carray.pushR(d)
        return self

    def pushL(self, *ds: Any) -> Dqueue:
        """Push data on front of dqueue, return reference to self."""
        for d in ds:
            if d != None:
                self._carray.pushL(d)
        return self

    def popR(self) -> Any|None:
        """Pop data off rear of dqueue"""
        if len(self._carray) > 0:
            return self._carray.popR()
        else:
            return None

    def popL(self) -> Any|None:
        """Pop data off front of dqueue"""
        if len(self._carray) > 0:
            return self._carray.popL()
        else:
            return None

    def peakR(self) -> Any|None:
        """Return righ-mostt element of dqueue without consuming it."""
        if len(self._carray) > 0:
            return self._carray[-1]
        else:
            return None

    def peakL(self) -> Any|None:
        """Return left-most element of dqueue without consuming it."""
        if len(self._carray) > 0:
            return self._carray[0]
        else:
            return None

    def capacity(self) -> int:
        """Returns current capacity of dqueue."""
        return self._carray.capacity()

    def fractionFilled(self) -> float:
        """Returns current capacity of dqueue."""
        return self._carray.fractionFilled()

    def resize(self, addCapacity = 0) -> Self:
        """Compact dqueue and add extra capacity."""
        self._carray.resize(addCapacity)
        return self

    def map(self, f: Callable[[Any], Any], mut: bool=False) -> Self|Dqueue:
        """Apply function over dqueue contents.

        Return new Dqueue if mut=False (the default)
        otherwise mutate the data structure and return self.
        """
        newDqueue  = Dqueue(*map(f, iter(self)))
        if mut:
            self._carray = newDqueue._carray
            return self
        return newDqueue

    def flatMap(self, f: Callable[[Any], Dqueue], mut: bool=False) -> Self|Dqueue:
        """Apply function and flatten result, surpress any None values.

        Merge the dqueues produced sequentially left-to-right.

        Return new Dqueue if mut=False (the default)
        otherwise mutate the data structure and return self.
        """
        newDqueue = Dqueue(*chain(*(iter(x) for x in map(f, iter(self)))))
        if mut:
            self._carray = newDqueue._carray
            return self
        return newDqueue

    def mergeMap(self, f: Callable[[Any], Dqueue], mut: bool=False) -> Self|Dqueue:
        """Apply function and flatten result, surpress any None values.

        Round Robin Merge the dqueues produced until first cached dqueue is
        exhausted.

        Return new Dqueue if mut=False (the default)
        otherwise mutate the data structure and return self.
        """
        newDqueue = Dqueue(*mergeIters(*(iter(x) for x in map(f, iter(self)))))
        if mut:
            self._carray = newDqueue._carray
            return self
        return newDqueue

    def exhaustMap(self, f: Callable[[Any], Dqueue], mut: bool=False) -> Self|Dqueue:
        """Apply function and flatten result, surpress any None values.

        Round Robin Merge the dqueues produced until all cached dqueues are exhausted.

        Return new Dqueue if mut=False (the default)
        otherwise mutate the data structure and return self.
        """
        newDqueue = Dqueue(*exhaustIters(*(iter(x) for x in map(f, iter(self)))))
        if mut:
            self._carray = newDqueue._carray
            return self
        return newDqueue

if __name__ == "__main__":
    pass
