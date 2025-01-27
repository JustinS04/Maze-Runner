from __future__ import annotations

from typing import List, Tuple, TypeVar

from data_structures.bst import BinarySearchTree
from algorithms.mergesort import mergesort

K = TypeVar('K')
I = TypeVar('I')


class BetterBST(BinarySearchTree[K, I]):
    def __init__(self, elements: List[Tuple[K, I]]) -> None:
        """
        Initialiser for the BetterBST class.
        We assume that the all the elements that will be inserted
        into the tree are contained within the elements list.

        As such you can assume the length of elements to be non-zero.
        The elements list will contain tuples of key, item pairs.

        First sort the elements list and then build a balanced tree from the sorted elements
        using the corresponding methods below.

        Args:
            elements(List[tuple[K, I]]): The elements to be inserted into the tree.

        Complexity:
            Best Case Complexity: O(N* log N) - where N is the number of elements in the input list. The time complexity of
                                    __sort_elements is O(N*logN) and __build_balanced_tree is O(N*logN). Hence overall
                                    O(N*log N + N*logN) --> O(N* logN)
            Worst Case Complexity: O(N* log N) - Same as best case.
        """
        super().__init__()
        # O(__sort_elements) -> O(N*logN)
        new_elements: List[Tuple[K, I]] = self.__sort_elements(elements)
        # O(__build_balanced_tree) -> O(N*logN)
        self.__build_balanced_tree(new_elements)

    def __sort_elements(self, elements: List[Tuple[K, I]]) -> List[Tuple[K, I]]:
        """
        Recall one of the drawbacks to using a binary search tree is that it can become unbalanced.
        If we know the elements ahead of time, we can sort them and then build a balanced tree.
        This will help us maintain the O(log n) complexity for searching, inserting, and deleting elements.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to sort.

        Returns:
            list(Tuple[K, I]]) - elements after being sorted.

        Complexity:
            Best Case Complexity: O(N * log N) - where N is the number of elements. It uses mergesort complexity
                                where it divides the list into smaller sublists until each list has one element,
                                then merges them back in a sorted order.
            Worst Case Complexity: O(N * log N) - Same as best case.
        """
        return mergesort(elements)

    def __build_balanced_tree(self, elements: List[Tuple[K, I]]) -> None:
        """
        This method will build a balanced binary search tree from the sorted elements.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to use to build our balanced tree.

        Returns:
            None

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(N * log N) - where N is the number of elements. It uses build_tree_aux complexity
                                                of halving the range of elements recursively, which takes O(log N) time.
                                                The __setitem__() magic method used to insert the element uses insertion,
                                                which also takes O(log N) time as the tree is maintained balanced. In total
                                                we perform N number of insertions for all elements. Hence overall O(N * log N).
            Worst Case Complexity: O(N * log N) - Same as best case.

        Justification:
            1. The code recursively divides the input list into smaller sublists by selecting the middle element. Hence,
            in each recursive call the range is halved resulting in a depth of log N.

            2. For each N elements, the insertion is done with '__setitem__()' magic method, which inserts the element into
            the BST. In a balanced tree where the height is maintained at log N, the overall insertion time is O(N * log N).

            As a result, the overall time complexity for building a balance tree is O(N * log N), where N is the number
            of elements in the input list.

        Complexity requirements for full marks:
            Best Case Complexity: O(n * log(n))
            Worst Case Complexity: O(n * log(n))
            where n is the number of elements in the list.
        """
        # Call the recursive auxiliary function to build the tree
        self.build_tree_aux(elements, 0, len(elements) - 1)

    def build_tree_aux(self, sorted_elements: List[Tuple[K, I]], start: int, end: int) -> None:
        """
        Recursively builds the balanced tree by inserting the middle element of the list.

        Args:
            sorted_elements (List[Tuple[K, I]]): The sorted elements from which to build the tree.
            start (int): The starting index of the current sublist.
            end (int): The ending index of the current sublist.

        Returns:
            None

        Complexity:
            Best Case Complexity: O(N * log N) - where N is the number of elements. It divides the range of elements recursively
                                                by taking the middle element and halving into left smaller sublists and right larger sublists.
                                                Hence this division process takes O(log N) time. The __setitem__() magic
                                                method from BST used to insert the element uses insertion, which also takes O(log N)
                                                time as the tree is maintained balanced. In total we perform N number of
                                                insertions for all elements. Hence overall O(N * log N)
            Worst Case Complexity: O(N * log N) - Same as best case.
        """
        # Base case: empty sublist
        if start > end:
            return

        else:
            # Find the middle index
            mid = (start + end) // 2

            # Insert the middle element into the BST
            key, value = sorted_elements[mid]
            self[key] = value

            # Recursively build the left and right subtrees
            self.build_tree_aux(sorted_elements, start, mid - 1)  # Left subtree
            self.build_tree_aux(sorted_elements, mid + 1, end)    # Right subtree

