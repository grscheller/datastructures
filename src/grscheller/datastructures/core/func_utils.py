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

"""Module grscheller.datastructures.core.func_utils

Class Maybe: Implements the Maybe Monad, also called Option or Optional Monad.
Class Either: Implements a left biased Either Monad.
"""
from __future__ import annotations
from typing import Any, Callable

__all__ = [
    'Either', 'Left', 'Right',
    'Maybe', 'Some', 'Nothing',
    'maybeToEither', 'eitherToMaybe'
]
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class Maybe():
    """Class representing a potentially missing value.

    - Implements the Option Monad
    - Maybe(value) constructs "Some(value)" 
    - Both Maybe() or Maybe(None) constructs a "Nothing"
    - immutable semantics - map & flatMap return modified copies
    - None is always treated as a non-existance value
      - cannot be stored in an object of type Maybe
      - semantically None does not exist
      - None only has any real existance as an implementration detail
    """
    def __init__(self, value: Any=None):
        self._value = value

    def __bool__(self) -> bool:
        """Return false if a Nothing, otherwise true."""
        return self._value != None

    def __len__(self) -> int:
        """A Maybe either contains something or not.
        Return 1 if a Some, 0 if a Nothing.
        """
        if self:
            return 1
        return 0

    def __iter__(self):
        """Yields its value if not a Nothing"""
        if self:
            yield self._value

    def __repr__(self) -> str:
        if self:
            return 'Some(' + repr(self._value) + ')'
        else:
            return 'Nothing'

    def __eq__(self, other: Maybe) -> bool:
        """Returns true if both sides are Nothings, or if both sides are Somes
        contining values which compare as equal.
        """
        if not isinstance(other, type(self)):
            return False
        return self._value == other._value

    def map(self, f: Callable[[Any], Any]) -> Maybe:
        if self:
            return Maybe(f(self._value))
        else:
            return Maybe()

    def flatMap(self, f: Callable[[Any], Maybe]) -> Maybe:
        if self:
            return f(self._value)
        else:
            return Maybe()

    def get(self, default: Any=None) -> Any:
        """Get contents if they exist, otherwise return None. Caller is
        responsible with dealing with a None return value.
        """
        if self:
            return self._value
        else:
            return default

# Maybe convenience functions/objects.

def maybeToEither(m: Maybe, right: Any=None) -> Either:
    """Convert a Maybe to an Either"""
    return Either(m.get(), right)

def Some(value=None):
    """Function for creating a Maybe from a value. If value is None or missing,
    returns a Nothing.
    """
    return Maybe(value)

#: Maybe object representing a missing value,
#: Nothing is not a singleton. Test via equality not identity.
Nothing = Some()


class Either():
    """Class that either contains a Left value or Right value, but not both.

    This version is biased to the Left, which is intended as the "happy path."
    """
    def __init__(self, left: Any, right: Any=None):
        if left == None:
            self._isLeft = False
            self._value = right
        else:
            self._isLeft = True
            self._value = left

    def __bool__(self) -> bool:
        """Return true if a Left, false if a Right"""
        return self._isLeft

    def __len__(self) -> int:
        """An Either always contains just one thing, even if it is None"""
        return 1

    def __iter__(self):
        """Yields its value if a Left"""
        if self:
            yield self._value

    def __repr__(self) -> str:
        if self:
            return 'Left(' + repr(self._value) + ')'
        else:
            return 'Right(' + repr(self._value) + ')'

    def __eq__(self, other: Either) -> bool:
        """True if both sides are same "type" and values compare as equal"""
        if not isinstance(other, type(self)):
            return False

        if (self and other) or (not self and not other):
            return self._value == other._value
        return False

    def copy(self) -> Either:
        if self:
            return Either(self._value)
        return Either(None, self._value)

    def map(self, f: Callable[[Any], Any], right=None) -> Either:
        if self:
            return Either(f(self._value), right)
        return self.copy()

    def mapRight(self, g: Callable[[Any], Any]) -> Either:
        """Map over if a Right."""
        if self:
            return self.copy()
        return Either(None, g(self._value))

    def flatMap(self, f: Callable[[Any], Either], right=None) -> Either:
        """flatMap with a Right default."""
        if self:
            return f(self._value).mapRight(lambda _: right)
        return self.copy()

    def get(self, default: Any=None) -> Any:
        """get value if a Left, otherwise return default value."""
        if self:
            return self._value
        return default

# Either convenience functions, act like subtype constructors.

def eitherToMaybe(e: Either) -> Maybe:
    """Convert an Either to a Maybe"""
    return Maybe(e.get())

def Left(left: Any, right: Any=None) -> Either:
    """Function returns Left Either if left != None, otherwise Right Either."""
    return Either(left, right)

def Right(right: Any) -> Either:
    """Function to construct a Right Either."""
    return Either(None, right)

if __name__ == "__main__":
    pass