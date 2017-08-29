'''
Created on Oct 8, 2012

@author: gsrinivasaraghavan
'''
import unittest
from random import randrange
from testgen_decorator import for_examples
from classheap import Heap

CMP_FUNCTION = lambda x, y : (1 if (x > y) else (-1 if (x < y) else 0))

class TestHeap(unittest.TestCase):

    def nlist(self, heapsize):
        '''
        Generate a random list of n numbers, each number is at most 2n
        '''
        lst = []
        randmax = 2*heapsize
        for _ in range(heapsize):
            lst.append(randrange(randmax))
        return lst


    def check_subtree_heap(self, heap, i):
        '''
        Check if the subtree rooted at index i is a heap
        '''
        leftmost = heap.get_leftmostchild_index(i)
        rightmost = heap.get_rightmostchild_index(i)
        isheap = True
        if (leftmost != None):
            for j in range(leftmost, rightmost):
                if (not heap.is_favoured(i, j)):
                    isheap = False
                    break
                else:
                    isheap = self.check_subtree_heap(heap, j)
                    if not isheap:
                        break
        return isheap

    @for_examples((True, 10, 1), (True, 20, 2), (True, 30, 3))
    @for_examples((False, 10, 1), (False, 15, 2), (False, 40, 3))
    def test_restore_subtree(self, ismin, heapsize, aexp):
        '''
        Test if the heap property for a subtree rooted at a node can be restored, assuming the node was corrupted
        in an existing heap
        '''
        heap = Heap(ismin, aexp, CMP_FUNCTION)
        rlist = self.nlist(heapsize)
        heap.import_list(rlist)
        heap.heapify()
        i = randrange(len(rlist))
        heap.set_item_at(i, (min(rlist) - 1) if (ismin) else (max(rlist) + 1))
        heap.restore_subtree(i)
        self.assertTrue(self.check_subtree_heap(heap, i))
        

    @for_examples((True, 10, 1), (True, 20, 2), (True, 30, 3))
    @for_examples((False, 10, 1), (False, 15, 2), (False, 40, 3))
    def test_heapify(self, ismin, heapsize, aexp):
        '''
        Test Heapification
        '''
        heap = Heap(ismin, aexp, CMP_FUNCTION)
        heap.import_list(self.nlist(heapsize))
        heap.heapify()
        self.assertTrue(self.check_subtree_heap(heap, 0))


    @for_examples((True, 10, 1), (True, 20, 2), (True, 30, 3))
    @for_examples((False, 10, 1), (False, 15, 2), (False, 40, 3))
    def test_restore_heap(self, ismin, heapsize, aexp):
        '''
        Test if the heap is restored correctly after a single-node gets corrupted
        '''
        heap = Heap(ismin, aexp, CMP_FUNCTION)
        rlist = self.nlist(heapsize)
        heap.import_list(rlist)
        heap.heapify()
        i = randrange(len(rlist))
        heap.set_item_at(i, (min(rlist) - 1) if (ismin) else (max(rlist) + 1))
        heap.restore_heap(i)
        self.assertTrue(self.check_subtree_heap(heap, i))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()