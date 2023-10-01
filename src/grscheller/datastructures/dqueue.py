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

from typing import Any, Callable
from .functional.maybe import Maybe, Nothing, Some
from .core import concatIters, mapIter

class Dqueue:
    """Double sided queue datastructure. Will resize itself as needed.

    Does not throw exceptions. The Dqueue class consistently uses None to
    represent the absence of a value. Therefore some care needs to be taken
    when Python None is pushed onto Dqueue objects.
    """
    def __init__(self, *data):
        """Construct a double sided queue"""
        size = len(data)
        capacity = size + 2
        self._capacity = capacity
        self._count = size
        self._front = 0
        self._rear = (size - 1) % capacity
        self._queue = list(data)
        self._queue.append(None)
        self._queue.append(None)

    def _isFull(self) -> bool:
        """Returns true if dqueue is full"""
        return self._count == self._capacity

    def _double(self):
        """Double capacity of dqueue"""
        if self._front > self._rear:
            frontPart = self._queue[self._front:]
            rearPart = self._queue[:self._rear+1]
        else:
            frontPart = self._queue
            rearPart = []
        self._queue = frontPart + rearPart + [None]*(self._capacity)
        self._capacity *= 2
        self._front = 0
        self._rear = self._count - 1

    def _compact(self):
        """Compact the datastructure as much as possible"""
        match self._count:
            case 0:
                self._queue = [None]*2
                self._capacity = 2
                self._front = 0
                self._rear = 1
            case 1:
                self._queue = [self._queue[self._front], None]
                self._capacity = 2
                self._front = 0
                self._rear = 0
            case _:
                if self._front > self._rear:
                    frontPart = self._queue[self._front:]
                    rearPart = self._queue[:self._rear+1]
                else:
                    frontPart = self._queue[self._front:self._rear+1]
                    rearPart = []
                self._queue = frontPart + rearPart
                self._capacity = self._count
                self._front = 0
                self._rear = self._capacity - 1

    def pushR(self, data: Any) -> Dqueue:
        """Push data on rear of dqueue, return the dqueue pushed to"""
        if self._isFull():
            self._double()
        self._rear = (self._rear + 1) % self._capacity
        self._queue[self._rear] = data
        self._count += 1
        return self

    def pushL(self, data: Any) -> Dqueue:
        """Push data on front of dqueue, return the dqueue pushed to"""
        if self._isFull():
            self._double()
        self._front = (self._front - 1) % self._capacity
        self._queue[self._front] = data
        self._count += 1
        return self

    def popR(self) -> Maybe:
        """Pop data off rear of dqueue"""
        if self._count == 0:
            return Nothing
        else:
            data = self._queue[self._rear]
            self._queue[self._rear] = None
            self._rear = (self._rear - 1) % self._capacity
            self._count -= 1
            return Some(data)

    def popL(self) -> Maybe:
        """Pop data off front of dqueue"""
        if self._count == 0:
            return Nothing
        else:
            data = self._queue[self._front]
            self._queue[self._front] = None
            self._front = (self._front + 1) % self._capacity
            self._count -= 1
            return Some(data)

    def headR(self) -> Maybe:
        """Return rear element of dqueue without consuming it"""
        if self._count == 0:
            return Nothing
        return Some(self._queue[self._rear])

    def headL(self) -> Maybe:
        """Return front element of dqueue without consuming it"""
        if self._count == 0:
            return Nothing
        return Some(self._queue[self._front])

    def __iter__(self):
        """Iterator yielding data stored in dequeue, does not consume data.

        To export contents of the Dqueue to a list, do
            myList = list(myDqueue)
        """
        if self._count > 0:
            cap = self._capacity
            rear = self._rear
            pos = self._front
            while pos != rear:
                yield self._queue[pos]
                pos = (pos + 1) % cap
            yield self._queue[pos]

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        cnt = self._count
        left = self
        frontL = self._front
        capL = self._capacity
        right = other
        frontR = other._front
        capR = other._capacity
        nn = 0
        while nn < cnt:
            if left._queue[(frontL+nn)%capL] != right._queue[(frontR+nn)%capR]:
                return False
            nn += 1
        return True

    def __repr__(self):
        """Display data in dqueue"""
        dataListStrs = []
        for data in self:
            dataListStrs.append(repr(data))
        return ">< " + " | ".join(dataListStrs) + " ><"

    def __len__(self) -> int:
        """Returns current number of values in dqueue"""
        return self._count

    def __bool__(self):
        """Returns true if dqueue is not empty"""
        return self._count > 0

    def __getitem__(self, ii: int) -> Any | None:
        """Together with __len__ method, allows the reversed() function to
        return a reverse iterator.

        Otherwise, the indexing of Dqueue objects should be considered private
        to the class.
        """
        if 0 <= ii < self._count:
            return self._queue[(self._front + ii) % self._capacity]
        else:
            return None

    def copy(self) -> Dqueue:
        """Return shallow copy of the dqueue in O(n) time & space complexity"""
        return Dqueue(*self)

    def capacity(self) -> int:
        """Returns current capacity of dqueue"""
        return self._capacity

    def fractionFilled(self) -> float:
        """Returns current capacity of dqueue"""
        return self._count/self._capacity

    def resize(self, addCapacity = 0):
        """Compact dqueue and add extra capacity"""
        self._compact()
        if addCapacity > 0:
            self._queue = self._queue + [None]*addCapacity
            self._capacity += addCapacity
            if self._count == 0:
                self._rear = self._capacity - 1

    def map1(self, f: Callable[[Any], Any]) -> Dqueue:
        """Apply function over dqueue contents, returns new instance"""
        newQueue = Dqueue()
        for nn in range(self._count):
            newQueue.pushR(f(self[nn]))
        return newQueue

    def map2(self, f: Callable[[Any], Any]) -> Dqueue:
        """Apply function over dqueue contents, returns new instance"""
        return Dqueue(*mapIter(iter(self), f))

    def flatMap(self, f: Callable[[Any], Dqueue]) -> Dqueue:
        """Apply function and flatten result, returns new instance"""
        return Dqueue(
            *concatIters(
                *mapIter(mapIter(iter(self), f), lambda x: iter(x))
            )
        )

if __name__ == "__main__":
    pass
