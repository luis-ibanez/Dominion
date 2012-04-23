'''
Created on 21/04/2012

@author: ender3
'''
import unittest
from app.dominion.util.circularList import CircularList


class CircularListTest(unittest.TestCase):

    def setUp(self):
        self.list=[1,2,3,4]
        self.circular_list = CircularList(self.list)

    def test_current(self):
        # make sure the shuffled sequence does not lose any elements
        self.current_index=self.circular_list.current()
        self.assertEqual(self.current_index, 1)

    def test_next(self):
        self.circular_list.next(1)
        self.assertEqual(self.circular_list.current(), 2)

    def test_circular_list(self):
        self.assertEqual(self.circular_list.current(),1)
        self.assertEqual(self.circular_list.next(1), 2)
        self.assertEqual(self.circular_list.next(1), 3)
        self.assertEqual(self.circular_list.next(1), 4)
        self.assertEqual(self.circular_list.next(1), 1)
        self.assertEqual(self.circular_list.next(1), 2)
        self.assertEqual(self.circular_list.next(1), 3)

if __name__ == "__main__":
    unittest.main()
