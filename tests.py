# -*- coding: utf-8 -*-

import unittest
from subset import *

class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assertIsSubset(self, a, b):
        self.assertTrue(is_subset(a, b))

    def assertIsNotSubset(self, a, b):
        self.assertFalse(is_subset(a, b))

    def test_false_if_names_are_different(self):
        self.assertIsNotSubset('a=1', 'b=1')
        self.assertIsNotSubset('a=1', 'b=1 or c=1')

#
#
#
    def test_simple_combined(self):
        self.assertIsNotSubset('a>10', 'a>10 and b>10')
        self.assertIsSubset('a>10', 'a>10 or b>10')
        self.assertIsSubset('a>10', 'a>5 or a>15')
        self.assertIsNotSubset('a>10', 'a>5 and a>15')

    def test_combined_simple(self):
        self.assertIsSubset('a>10 and b>10', 'a>10')
        self.assertIsNotSubset('a>10 or b>10', 'a>10')
        self.assertIsNotSubset('a>5 or a>15', 'a>10')
        self.assertIsSubset('a>5 and a>15', 'a>10')

    def test_combined(self):
        self.assertIsSubset('a>10 or b>10', 'a>5 or b>5')
        self.assertIsNotSubset('a>10 or b>10', 'a>15 or b>15')
        self.assertIsSubset('a>10 and b>10', 'a>5 and b>5')
        self.assertIsNotSubset('a>10 or b>10', 'a>5 and b>5')
        self.assertIsSubset('a>10 and b>10', 'a>5 or b>5')
        self.assertIsSubset('a>10 and b>10 and c>10', 'a>5 and b>5 and c>5')
        self.assertIsNotSubset('a>10 and b>10 and c>10', 'a>5 and b>5 and c<5')
        self.assertIsSubset('(a>10 or b>10) and (c>10 or d>10)', '(a>5 or b>5) and (c>5 or d>5)');
        self.assertIsSubset('a>10 and b>10 or c>10 and d>10', 'a>5 and b>5 or c>5 and d>5');
        self.assertIsSubset('(a>10 or b>10) and c>10', '(a>10 or b>10) and c>5');
        self.assertIsNotSubset('(a>10 or b>10) and c>10', '(a>10 or b>10) and c>15');
        self.assertIsSubset('a>10 and a<20', 'a>5 and a<25');

#
# Test factor
#
    def test_factor_eq(self):
        cases = [
            (True,  'a=10', 'a=10'),
            (False, 'a=10', 'a>10'),
            (False, 'a=10', 'a<10'),
            (True,  'a=10', 'a>=10'),
            (True,  'a=10', 'a<=10'),
            (False, 'a=10', 'a!=10'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a=10', 'a=5'),
            (True,  'a=10', 'a>5'),
            (False, 'a=10', 'a<5'),
            (True,  'a=10', 'a>=5'),
            (False, 'a=10', 'a<=5'),
            (True,  'a=10', 'a!=5'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a=10', 'a=15'),
            (False, 'a=10', 'a>15'),
            (True,  'a=10', 'a<15'),
            (False, 'a=10', 'a>=15'),
            (True,  'a=10', 'a<=15'),
            (True,  'a=10', 'a!=15'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))            

    def test_factor_gt(self):
        cases = [
            (False, 'a>10', 'a=10'),
            (True,  'a>10', 'a>10'),
            (False, 'a>10', 'a<10'),
            (True,  'a>10', 'a>=10'),
            (False, 'a>10', 'a<=10'),
            (True,  'a>10', 'a!=10'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a>10', 'a=5'),
            (True,  'a>10', 'a>5'),
            (False, 'a>10', 'a<5'),
            (True,  'a>10', 'a>=5'),
            (False, 'a>10', 'a<=5'),
            (True,  'a>10', 'a!=5'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a>10', 'a=15'),
            (False, 'a>10', 'a>15'),
            (False, 'a>10', 'a<15'),
            (False, 'a>10', 'a>=15'),
            (False, 'a>10', 'a<=15'),
            (False, 'a>10', 'a!=15'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))  

    def test_factor_lt(self):
        cases = [
            (False, 'a<10', 'a=10'),
            (False, 'a<10', 'a>10'),
            (True,  'a<10', 'a<10'),
            (False, 'a<10', 'a>=10'),
            (True,  'a<10', 'a<=10'),
            (True,  'a<10', 'a!=10'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a<10', 'a=5'),
            (False, 'a<10', 'a>5'),
            (False, 'a<10', 'a<5'),
            (False, 'a<10', 'a>=5'),
            (False, 'a<10', 'a<=5'),
            (False, 'a<10', 'a!=5'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a<10', 'a=15'),
            (False, 'a<10', 'a>15'),
            (True,  'a<10', 'a<15'),
            (False, 'a<10', 'a>=15'),
            (True,  'a<10', 'a<=15'),
            (True,  'a<10', 'a!=15'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))  

    def test_factor_gte(self):
        cases = [
            (False, 'a>=10', 'a=10'),
            (False, 'a>=10', 'a>10'),
            (False, 'a>=10', 'a<10'),
            (True,  'a>=10', 'a>=10'),
            (False, 'a>=10', 'a<=10'),
            (False, 'a>=10', 'a!=10'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a>=10', 'a=5'),
            (True,  'a>=10', 'a>5'),
            (False, 'a>=10', 'a<5'),
            (True,  'a>=10', 'a>=5'),
            (False, 'a>=10', 'a<=5'),
            (True,  'a>=10', 'a!=5'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a>=10', 'a=15'),
            (False, 'a>=10', 'a>15'),
            (False, 'a>=10', 'a<15'),
            (False, 'a>=10', 'a>=15'),
            (False, 'a>=10', 'a<=15'),
            (False, 'a>=10', 'a!=15'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))  

    def test_factor_lte(self):
        cases = [
            (False, 'a<=10', 'a=10'),
            (False, 'a<=10', 'a>10'),
            (False, 'a<=10', 'a<10'),
            (False, 'a<=10', 'a>=10'),
            (True,  'a<=10', 'a<=10'),
            (False, 'a<=10', 'a!=10'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a<=10', 'a=5'),
            (False, 'a<=10', 'a>5'),
            (False, 'a<=10', 'a<5'),
            (False, 'a<=10', 'a>=5'),
            (False, 'a<=10', 'a<=5'),
            (False, 'a<=10', 'a!=5'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a<=10', 'a=15'),
            (False, 'a<=10', 'a>15'),
            (True,  'a<=10', 'a<15'),
            (False, 'a<=10', 'a>=15'),
            (True,  'a<=10', 'a<=15'),
            (True,  'a<=10', 'a!=15'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))  

    def test_factor_ne(self):
        cases = [
            (False, 'a!=10', 'a=10'),
            (False, 'a!=10', 'a>10'),
            (False, 'a!=10', 'a<10'),
            (False, 'a!=10', 'a>=10'),
            (False, 'a!=10', 'a<=10'),
            (True,  'a!=10', 'a!=10'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a!=10', 'a=5'),
            (False, 'a!=10', 'a>5'),
            (False, 'a!=10', 'a<5'),
            (False, 'a!=10', 'a>=5'),
            (False, 'a!=10', 'a<=5'),
            (False, 'a!=10', 'a!=5'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))

        cases = [
            (False, 'a!=10', 'a=15'),
            (False, 'a!=10', 'a>15'),
            (False, 'a!=10', 'a<15'),
            (False, 'a!=10', 'a>=15'),
            (False, 'a!=10', 'a<=15'),
            (False, 'a!=10', 'a!=15'),
        ]
        for expect, a, b in cases:
            self.assertEqual(is_subset(a, b), expect, (expect, a, b))             

if __name__ == '__main__':
    unittest.main()

