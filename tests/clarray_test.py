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

from typing import Any
from grscheller.datastructures.array import CLArray

class TestCLArray:
    def test_map1(self):
        cl1 = CLArray(0, 1, 2, 3, size=-6, default=-1)
        cl2 = cl1.map(lambda x: x+1, size=7, default=42)
        assert cl1[0] + 1 == cl2[0] == 0
        assert cl1[1] + 1 == cl2[1] == 0
        assert cl1[2] + 1 == cl2[2] == 1
        assert cl1[3] + 1 == cl2[3] == 2
        assert cl1[4] + 1 == cl2[4] == 3
        assert cl1[5] + 1 == cl2[5] == 4
        assert cl2[6] == 42

    def test_map2(self):
        cl1 = CLArray(0, 1, 2, 3, size=6, default=-1)
        cl2 = cl1.map(lambda x: x+1)
        assert cl1[0] + 1 == cl2[0] == 1
        assert cl1[1] + 1 == cl2[1] == 2
        assert cl1[2] + 1 == cl2[2] == 3
        assert cl1[3] + 1 == cl2[3] == 4
        assert cl1[4] + 1 == cl2[4] == 0
        assert cl1[5] + 1 == cl2[5] == 0

    def test_map3(self):
        cl1 = CLArray(1, 2, 3, 10)

        cl2 = cl1.map(lambda x: x*x-1)
        assert cl2 is not None
        assert cl1 is not cl2
        assert cl1 == CLArray(1, 2, 3, 10)
        assert cl2 == CLArray(0, 3, 8, 99)
        
    def test_default(self):
        cl1 = CLArray(size=1, default=1)
        cl2 = CLArray(size=1, default=2)
        assert cl1 != cl2
        assert cl1[0] == 1
        assert cl2[0] == 2
        assert not cl1
        assert not cl2
        assert len(cl1) == 1
        assert len(cl2) == 1

        foo = 42
        baz = 'hello world'

        try:
            foo = cl1[0]
        except IndexError as err:
            print(err)
            assert False
        else:
            assert True
        finally:
            assert True
            assert foo == 1

        try:
            baz = cl2[42]
        except IndexError as err:
            print(err)
            assert True
        else:
            assert False
        finally:
            assert True
            assert baz == 'hello world'

        cl1 = CLArray(size=1, default=12)
        cl2 = CLArray(size=1, default=30)
        assert cl1 != cl2
        assert not cl1
        assert not cl2
        assert len(cl1) == 1
        assert len(cl2) == 1

        cl0 = CLArray()
        cl1 = CLArray(default=())
        cl2 = CLArray(None, None, None, size=2)
        cl3 = CLArray(None, None, None, size=2, default=())
        assert len(cl0) == 0
        assert cl0.default() == ()
        assert len(cl1) == 0
        assert cl1.default() == ()
        assert len(cl2) == 2
        assert cl2.default() == ()
        assert len(cl3) == 2
        assert cl3.default() == ()
        assert cl2[0] == cl2[1] == ()
        assert cl3[0] == cl3[1] == ()
        assert not cl0
        assert not cl1
        assert not cl2
        assert not cl3

        cl1 = CLArray(1, 2, size=3, default=42)
        cl2 = CLArray(1, 2, None, size=3, default=42)
        assert cl1 == cl2
        assert cl1 is not cl2
        assert cl1
        assert cl2
        assert len(cl1) == 3
        assert len(cl2) == 3
        assert cl1[2] == cl2[2] == cl1[-1] == cl2[-1] == 42

        cl1 = CLArray(1, 2, size=-3)
        cl2 = CLArray((), 1, 2)
        assert cl1 == cl2
        assert cl1 is not cl2
        assert cl1
        assert cl2
        assert len(cl1) == 3
        assert len(cl2) == 3

        cl5 = CLArray(*range(1,4), size=-5, default=42)
        assert cl5 == CLArray(42, 42, 1, 2, 3)

    def test_set_then_get(self):
        cl = CLArray(size=5, default=0)
        assert cl[1] == 0
        cl[3] = set = 42
        got = cl[3]
        assert set == got

    def test_equality(self):
        cl1 = CLArray(1, 2, 'Forty-Two', (7, 11, 'foobar'))
        cl2 = CLArray(1, 3, 'Forty-Two', [1, 2, 3])
        assert cl1 != cl2
        cl2[1] = 2
        assert cl1 != cl2
        cl1[3] = cl2[3]
        assert cl1 == cl2

    def test_len_getting_indexing_padding_slicing(self):
        cl = CLArray(*range(2000))
        assert len(cl) == 2000

        cl = CLArray(*range(542), size=42)
        assert len(cl) == 42
        assert cl[0] == 0
        assert cl[41] == cl[-1] == 41
        assert cl[2] == cl[-40]

        cl = CLArray(*range(1042), size=-42)
        assert len(cl) == 42
        assert cl[0] == 1000
        assert cl[41] == 1041
        assert cl[-1] == 1041
        assert cl[41] == cl[-1] == 1041
        assert cl[1] == cl[-41] == 1001
        assert cl[0] == cl[-42]

        cl = CLArray(*[1, 'a', (1, 2)], size=5, default=42)
        assert cl[0] == 1
        assert cl[1] == 'a'
        assert cl[2] == (1, 2)
        assert cl[3] == 42
        assert cl[4] == 42
        assert cl[-1] == 42
        assert cl[-2] == 42
        assert cl[-3] == (1, 2)
        assert cl[-4] == 'a'
        assert cl[-5] == 1
        try:
            foo = cl[5] 
            print(f'should never print: {foo}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False
        try:
            bar = cl[-6] 
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False

        cl = CLArray(*[1, 'a', (1, 2)], size=-6, default=42)
        assert cl[0] == 42
        assert cl[1] == 42
        assert cl[2] == 42
        assert cl[3] == 1
        assert cl[4] == 'a'
        assert cl[5] == (1, 2)
        assert cl[-1] == (1, 2)
        assert cl[-2] == 'a'
        assert cl[-3] == 1
        assert cl[-4] == 42
        assert cl[-5] == 42
        assert cl[-6] == 42
        try:
            foo = cl[6] 
            print(f'should never print: {foo}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False
        try:
            bar = cl[-7] 
            print(f'should never print: {bar}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False

    def test_bool(self):
        cl_allNotNone = CLArray(True, 0, '')
        cl_allNone = CLArray(None, None, None, default=42)
        cl_firstNone = CLArray(None, False, [])
        cl_lastNone = CLArray(0.0, True, False, None)
        cl_someNone = CLArray(0, None, 42, None, False)
        cl_defaultNone = CLArray(default = None)
        cl_defaultNotNone = CLArray(default = False)
        assert cl_allNotNone
        assert not cl_allNone
        assert cl_firstNone
        assert cl_lastNone
        assert cl_someNone
        assert not cl_defaultNone
        assert not cl_defaultNotNone

        cl_Nones = CLArray(None, size=4321, default=())
        cl_0 = CLArray(0, 0, 0)
        cl_42s = CLArray(*([42]*42))
        cl_42s_d42 = CLArray(*([42]*42), default=42)
        cl_emptyStr = CLArray('')
        cl_hw = CLArray('hello', 'world')
        assert not cl_Nones
        assert cl_0
        assert cl_42s
        assert not cl_42s_d42
        assert cl_emptyStr
        assert cl_hw

    def test_reversed_iter(self):
        """Tests that prior state of cl is used, not current one"""
        cl = CLArray(1,2,3,4,5)
        clrevIter = reversed(cl)
        aa = next(clrevIter)
        assert cl[4] == aa == 5
        cl[2] = 42
        aa = next(clrevIter)
        assert cl[3] == aa == 4
        aa = next(clrevIter)
        assert cl[2] != aa == 3
        aa = next(clrevIter)
        assert cl[1] == aa == 2
        aa = next(clrevIter)
        assert cl[0] == aa == 1

    def test_reverse(self):
        cl1 = CLArray(1, 2, 3, 'foo', 'bar')
        cl2 = CLArray('bar', 'foo', 3, 2, 1)
        assert cl1 != cl2
        cl2.reverse()
        assert cl1 == cl2
        cl1.reverse()
        assert cl1 != cl2
        assert cl1[1] == cl2[-2]

        cl4 = cl2.copy()
        cl5 = cl2.copy()
        assert cl4 == cl5
        cl4.reverse()
        cl5.reverse()
        assert cl4 != cl2
        assert cl5 != cl2
        cl2.reverse()
        assert cl4 == cl2

    def test_copy_map(self):

        def ge3(n: int) -> int|None:
            if n < 3:
                return None
            return n

        cl4 = CLArray(*range(43), size = 5)
        cl5 = CLArray(*range(43), size = -5)
        cl4_copy = cl4.copy()
        cl5_copy = cl5.copy()
        assert cl4 == cl4_copy
        assert cl4 is not cl4_copy
        assert cl5 == cl5_copy
        assert cl5 is not cl5_copy
        assert cl4[0] == 0
        assert cl4[4] == cl4[-1] == 4
        assert cl5[0] == 38
        assert cl5[4] == cl5[-1] == 42

        cl0 = CLArray(None, *range(1, 6), size=7, default=0)
        cl0b = CLArray(*range(1, 6), size=-7, default=0)
        assert cl0 == CLArray(1, 2, 3, 4, 5, 0, 0)
        assert cl0b == CLArray(0, 0, 1, 2, 3, 4, 5)
        assert cl0.default() == 0
        assert cl0b.default() == 0
        cl1 = cl0.copy()
        cl2 = cl0.copy(default=4)
        assert cl1 == cl2 == cl0
        assert cl1.default() == 0
        assert cl2.default() == 4

        cl0 = cl0.map(ge3)
        cl3 = cl1.map(ge3)
        cl4 = cl2.map(ge3)
        assert cl0.default() == 0
        assert cl3.default() == 0
        assert cl4.default() == 4
        assert cl0 == CLArray(0, 0, 3, 4, 5, 0, 0)
        assert cl3 == CLArray(0, 0, 3, 4, 5, 0, 0)
        assert cl4 == CLArray(4, 4, 3, 4, 5, 4, 4)
        assert cl3.copy(size=6).copy(size=-3) == CLArray(4, 5, 0)
        assert cl3.copy(size=6).copy(size=3) == CLArray(0, 0, 3)
        assert cl4.copy(size=6).copy(size=-3) == CLArray(4, 5, 4)
        assert cl4.copy(size=6).copy(size=3) == CLArray(4, 4, 3)
        cl5 = cl3.copy(default=2)
        cl6 = cl4.copy(default=2)
        assert cl6 != cl5
        cl7 = cl5.copy(default=-1)
        cl8 = cl6.copy(default=-1)
        assert cl8 != cl7
        assert cl8.default() == cl7.default() == -1
        assert cl8.map(ge3) != cl7.map(ge3)
        assert cl8.default() == cl7.default() == -1
        assert cl7.map(ge3) == CLArray(-1, -1, 3, 4, 5, -1, -1, default = -1)

        cl0 = CLArray(5,4,3,2,1)
        assert cl0.copy(size=3) == CLArray(5, 4, 3)
        assert cl0.copy(size=-3) == CLArray(3, 2, 1)
        cl1 = cl0.map(ge3)
        assert (cl1[0], cl1[1], cl1[2], cl1[3], cl1[4]) == (5, 4, 3, (), ())
        cl2 = cl0.copy(default=0).map(ge3)
        assert (cl2[0], cl2[1], cl2[2], cl2[3], cl2[4]) == (5, 4, 3, 0, 0)
        cl2 = cl0.map(ge3, default=42)
        assert (cl2[0], cl2[1], cl2[2], cl2[3], cl2[4]) == (5, 4, 3, 42, 42)

    # tests not complete due to flatMap changes
    def test_flatMap(self):

        def ge1(n: Any) -> int|None:
            if n == ():
                return None
            if n >= 1:
                return n
            return None

        def lt2or42(n: Any) -> int|None:
            if n == ():
                return 42
            if n < 2:
                return n
            return None

        # Keep defaults all the same
        cl0 = CLArray(*range(10), default=6)
        cl1 = cl0.flatMap(lambda x: CLArray(*range(x%5)))
        cl2 = cl0.flatMap(lambda x: CLArray(*range(x%5), default=6))
        cl3 = cl0.flatMap(lambda x: CLArray(*range(x%5)), default=6)
        cl4 = cl0.flatMap(lambda x: CLArray(*range(x%5), default=7), default=6)
        assert cl1 == cl2 == cl3 == cl4
        assert cl1 == CLArray(0,0,1,0,1,2,0,1,2,3,0,0,1,0,1,2,0,1,2,3)
        assert cl0.default() == 6
        assert cl1.default() == 6
        assert cl2.default() == 6
        assert cl3.default() == 6
        assert cl4.default() == 6
        cl11 = cl1.map(ge1)
        cl12 = cl2.map(ge1)
        cl13 = cl3.map(ge1)
        cl14 = cl4.map(ge1)
        assert cl11 == cl12 == cl13 == cl14
        assert cl11 == CLArray(6,6,1,6,1,2,6,1,2,3,6,6,1,6,1,2,6,1,2,3)
        assert cl11.default() == cl12.default() == cl13.default()
        assert cl13.default() == cl14.default() == 6
        cl11 = cl1.map(lt2or42)
        cl12 = cl2.map(lt2or42)
        cl13 = cl3.map(lt2or42)
        cl14 = cl4.map(lt2or42)
        assert cl11 == cl12 == cl13 == cl14
        assert cl11 == CLArray(0,0,1,0,1,6,0,1,6,6,0,0,1,0,1,6,0,1,6,6)
        assert cl11.default() == 6
        assert cl12.default() == 6
        assert cl13.default() == 6
        assert cl14.default() == 6

        # Vary up the defaults
        cl0 = CLArray(*range(10), default=6)
        assert cl0.default() == 6
        cl1 = cl0.flatMap(lambda x: CLArray(*range(x%5)))
        cl2 = cl0.flatMap(lambda x: CLArray(*range(x%5), default=7))
        cl3 = cl0.flatMap(lambda x: CLArray(*range(x%5)), default=8)
        cl4 = cl0.flatMap(lambda x: CLArray(*range(x%5), default=-1), default=9)
        assert cl1.default() == 6
        assert cl2.default() == 6
        assert cl3.default() == 8
        assert cl4.default() == 9
        assert cl1 == cl2 == cl3 == cl4
        assert cl1 == CLArray(0,0,1,0,1,2,0,1,2,3,0,0,1,0,1,2,0,1,2,3)
        cl11 = cl1.map(lt2or42)
        cl12 = cl2.map(lt2or42)
        cl13 = cl3.map(lt2or42)
        cl14 = cl4.map(lt2or42)
        assert cl11 == CLArray(0,0,1,0,1,6,0,1,6,6,0,0,1,0,1,6,0,1,6,6)
        assert cl12 == CLArray(0,0,1,0,1,6,0,1,6,6,0,0,1,0,1,6,0,1,6,6)
        assert cl13 == CLArray(0,0,1,0,1,8,0,1,8,8,0,0,1,0,1,8,0,1,8,8)
        assert cl14 == CLArray(0,0,1,0,1,9,0,1,9,9,0,0,1,0,1,9,0,1,9,9)
        assert cl11.default() == 6
        assert cl12.default() == 6
        assert cl13.default() == 8
        assert cl14.default() == 9

        # Vary up the defaults, no default set on initial CLArray
        cl0 = CLArray(*range(10))
        assert cl0.default() == ()
        cl1 = cl0.flatMap(lambda x: CLArray(*range(x%5)))
        cl2 = cl0.flatMap(lambda x: CLArray(*range(x%5), default=7))
        cl3 = cl0.flatMap(lambda x: CLArray(*range(x%5)), default=8)
        cl4 = cl0.flatMap(lambda x: CLArray(*range(x%5), default=-1), default=9)
        assert cl1 == cl2 == cl3 == cl4
        assert cl1 == CLArray(0,0,1,0,1,2,0,1,2,3,0,0,1,0,1,2,0,1,2,3)
        assert cl1.default() == ()
        assert cl2.default() == ()
        assert cl3.default() == 8
        assert cl4.default() == 9
        cl11 = cl1.map(lt2or42)
        cl12 = cl2.map(lt2or42)
        cl13 = cl3.map(lt2or42)
        cl14 = cl4.map(lt2or42)
        assert cl11 == CLArray(0,0,1,0,1,(),0,1,(),(),0,0,1,0,1,(),0,1,(),())
        assert cl12 == CLArray(0,0,1,0,1,(),0,1,(),(),0,0,1,0,1,(),0,1,(),())
        assert cl13 == CLArray(0,0,1,0,1,8,0,1,8,8,0,0,1,0,1,8,0,1,8,8)
        assert cl14 == CLArray(0,0,1,0,1,9,0,1,9,9,0,0,1,0,1,9,0,1,9,9)
        assert cl11.default() == ()
        assert cl12.default() == ()
        assert cl13.default() == 8
        assert cl14.default() == 9

        # Let f change default, set default set on initial CLArray
        cl0 = CLArray(*range(3), default=6)
        assert cl0.default() == 6
        cl1 = cl0.flatMap(lambda x: CLArray(*range(x)))
        cl2 = cl0.flatMap(lambda x: CLArray(*range(x), default=x*x))
        cl3 = cl0.flatMap(lambda x: CLArray(*range(x)), default=8)
        cl4 = cl0.flatMap(lambda x: CLArray(*range(x), default=-1), default=9)
        fcl5 = cl0.flatMap(lambda x: CLArray(*range(x), default=cl0.default()))
        fcl6 = cl0.flatMap(lambda x: CLArray(*range(x), default=8), default=8)
        assert cl1 == CLArray(0, 0, 1)
        assert cl2 == CLArray(0, 0, 1)
        assert cl3 == CLArray(0, 0, 1)
        assert cl4 == CLArray(0, 0, 1)
        assert fcl5 == CLArray(0, 0, 1)
        assert fcl6 == CLArray(0, 0, 1)
        assert cl1.default() == 6
        assert cl2.default() == 6
        assert cl3.default() == 8
        assert cl4.default() == 9
        assert fcl5.default() == 6
        assert fcl6.default() == 8

        # Let f change default, no default set on initial CLArray
        cl0 = CLArray(*range(5), default=-1)
        assert cl0.default() == -1
        cl1 = cl0.flatMap(lambda x: CLArray(*range(x+1), default=x+1))
        cl2 = cl0.flatMap(lambda x: CLArray(*range(x), default=x*x))
        cl3 = cl0.flatMap(lambda x: CLArray(*range(x)), default=8)
        cl4 = cl0.flatMap(lambda x: CLArray(*range(x), default=-1), default=9)
        assert cl1 == CLArray(0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 4)
        assert cl2 == CLArray(0, 0, 1, 0, 1, 2, 0, 1, 2, 3)
        assert cl3 == CLArray(0, 0, 1, 0, 1, 2, 0, 1, 2, 3)
        assert cl4 == CLArray(0, 0, 1, 0, 1, 2, 0, 1, 2, 3)
        assert cl1.default() == -1
        assert cl2.default() == -1
        assert cl3.default() == 8
        assert cl4.default() == 9
        cl11 = cl1.map(lt2or42)
        cl12 = cl2.map(lt2or42)
        cl13 = cl3.map(lt2or42)
        cl14 = cl4.map(lt2or42)
        assert cl11 == CLArray(0, 0, 1, 0, 1, -1, 0, 1, -1, -1, 0, 1, -1, -1, -1)
        assert cl12 == CLArray(0, 0, 1, 0, 1, -1, 0, 1, -1, -1)
        assert cl13 == CLArray(0, 0, 1, 0, 1, 8, 0, 1, 8, 8)
        assert cl14 == CLArray(0, 0, 1, 0, 1, 9, 0, 1, 9, 9)
        assert cl11.default() == -1
        assert cl12.default() == -1
        assert cl13.default() == 8
        assert cl14.default() == 9

        def bar(x):
            return CLArray(2, x, 3*x, size=4, default=7*x)

        cl0 = CLArray(1, 2, size=3, default=-1)
        cl1 = cl0.flatMap(bar, size=14)
        assert repr(cl1) == 'CLArray(2, 1, 3, 7, 2, 2, 6, 14, 2, -1, -3, -7, -1, -1, size=14, default=-1)'

#       cl0 = CLArray(1, 2, size=3, default=-1, backlog=(8, 9, 10))
#       cl1 = cl0.flatMap(bar, size=16)
#       assert repr(cl1) == 'CLArray(2, 1, 3, 7, 2, 2, 6, 14, 2, -1, -3, -7, 8, 9, 10, -1, size=16, default=-1)'

