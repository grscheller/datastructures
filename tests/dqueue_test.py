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

from grscheller.datastructures.dqueue import DQueue

class TestDqueue:
    def test_push_then_pop(self):
        dq = DQueue()
        pushed = 42; dq.pushL(pushed)
        popped = dq.popL()
        assert pushed == popped
        assert len(dq) == 0
        pushed = 0; dq.pushL(pushed)
        popped = dq.popR()
        assert pushed == popped == 0
        assert not dq
        pushed = 0; dq.pushR(pushed)
        popped = dq.popL()
        assert popped is not None
        assert pushed == popped
        assert len(dq) == 0
        pushed = ''; dq.pushR(pushed)
        popped = dq.popR()
        assert pushed == popped
        assert len(dq) == 0
        dq.pushR('first').pushR('second').pushR('last')
        assert dq.popL() == 'first'
        assert dq.popR() == 'last'
        assert dq
        dq.popL()
        assert len(dq) == 0

    def test_pushing_None(self):
        dq0 = DQueue()
        dq1 = DQueue()
        dq2 = DQueue()
        dq1.pushR(None)
        dq2.pushL(None)
        assert dq0 == dq1 == dq2

        barNone = (1, 2, None, 3, None, 4)
        bar = (1, 2, 3, 4)
        dq0 = DQueue(*barNone)
        dq1 = DQueue(*bar)
        assert dq0 == dq1
        for d in iter(dq0):
            assert d is not None
        for d in dq1:
            assert d is not None

    def test_bool_len_peak(self):
        dq = DQueue()
        assert not dq
        dq.pushL(2,1)
        dq.pushR(3)
        assert dq
        assert len(dq) == 3
        assert dq.popL() == 1
        assert len(dq) == 2
        assert dq
        assert dq.peakL() == 2
        assert dq.peakR() == 3
        assert dq.popR() == 3
        assert len(dq) == 1
        assert dq
        assert dq.popL() == 2
        assert len(dq) == 0
        assert not dq
        assert not dq.popL()
        assert not dq.popR()
        assert dq.popL() == None
        assert dq.popR() == None
        assert len(dq) == 0
        assert not dq
        assert dq.pushR(42)
        assert len(dq) == 1
        assert dq
        assert dq.peakL() == 42
        assert dq.peakR() == 42
        assert dq.popR() == 42
        assert not dq
        assert dq.peakL() == None
        assert dq.peakR() == None

    def test_iterators(self):
        data = [1, 2, 3, 4]
        dq = DQueue(*data)
        ii = 0
        for item in dq:
            assert data[ii] == item
            ii += 1
        assert ii == 4

        data.append(5)
        dq = DQueue(*data)
        data.reverse()
        ii = 0
        for item in reversed(dq):
            assert data[ii] == item
            ii += 1
        assert ii == 5

        dq0 = DQueue()
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

        data = ()
        dq0 = DQueue(*data)
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

    def test_capacity(self):
        dq = DQueue(1, 2)
        assert dq.fractionFilled() == 2/2
        dq.pushL(0)
        assert dq.fractionFilled() == 3/4
        dq.pushR(3)
        assert dq.fractionFilled() == 4/4
        dq.pushR(4)
        assert dq.fractionFilled() == 5/8
        assert len(dq) == 5
        assert dq.capacity() == 8
        dq.resize()
        assert dq.fractionFilled() == 5/5
        dq.resize(20)
        assert dq.fractionFilled() == 5/25

    def test_copy_reversed(self):
        dq1 = DQueue(*range(20))
        dq2 = dq1.copy()
        assert dq1 == dq2
        assert dq1 is not dq2
        jj = 19
        for ii in reversed(dq1):
            assert jj == ii
            jj -= 1
        jj = 0
        for ii in iter(dq1):
            assert jj == ii
            jj += 1

    def test_equality(self):
        dq1 = DQueue(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        dq2 = DQueue(2, 3, 'Forty-Two').pushL(1).pushR((7, 11, 'foobar'))
        assert dq1 == dq2

        tup2 = dq2.popR()
        assert dq1 != dq2

        dq2.pushR((42, 'foofoo'))
        assert dq1 != dq2

        dq1.popR()
        dq1.pushR((42, 'foofoo')).pushR(tup2)
        dq2.pushR(tup2)
        assert dq1 == dq2

        holdA = dq1.popL()
        dq1.resize(42)
        holdB = dq1.popL()
        holdC = dq1.popR()
        dq1.pushL(holdB).pushR(holdC).pushL(holdA).pushL(200)
        dq2.pushL(200)
        assert dq1 == dq2

    def test_maps(self):
        # TODO: more edge cases
        # TODO: change up from queue_twst.py version
        q0 = DQueue(1,2,3,5)
        f1 = lambda x: x*x - 1
        f2 = lambda x: DQueue(1, x, x*x+1)
        f3 = lambda x: DQueue(*range(2*x, 4*x))
        f4 = lambda x: DQueue(*range(2*x, 3*x))

        q1 = q0.copy()
        q2 = q1.map(f1)
        assert q1 == q0
        q1.map(f1, mut=True)
        assert q1 == q2 == DQueue(0,3,8,24)
        assert q1 != q0

        q3 = q0.copy()
        q4 = q3.flatMap(f2)
        assert q3 == q0
        q3.flatMap(f2, mut=True)
        assert q3 == q4 == DQueue(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 5, 26)
        assert q3 != q0

        q3 = q0.copy()
        q4 = q3.mergeMap(f3)
        assert q3 == q0
        q3.mergeMap(f3, mut=True)
        assert q3 == q4 == DQueue(2, 4, 6, 10, 3, 5, 7, 11)
        assert q3 != q0

        q5 = q0.copy()
        q6 = q5.exhaustMap(f4)
        assert q5 == q0
        q5.exhaustMap(f4, mut=True)
        assert q5 == q6 == DQueue(2, 4, 6, 10, 5, 7, 11, 8, 12, 13, 14)
        assert q5 != q0
