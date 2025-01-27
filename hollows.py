from __future__ import annotations
"""
Ensure you have read the introduction and task 1 and understand what 
is prohibited in this task.
This includes:
The ban on inbuilt sort methods .sort() or sorted() in this task.
And ensure your treasure data structure is not banned.

"""
from abc import ABC, abstractmethod
from typing import List
from data_structures.heap import MaxHeap
from data_structures.bst import BinarySearchTree
from betterbst import BetterBST
from config import Tiles
from treasure import Treasure, generate_treasures


class Hollow(ABC):
    """
    DO NOT MODIFY THIS CLASS
    Mystical troves of treasure that can be found in the maze
    There are two types of hollows that can be found in the maze:
    - Spooky Hollows: Each of these hollows contains unique treasures that can be found nowhere else in the maze.
    - Mystical Hollows: These hollows contain a random assortment of treasures like the spooky hollow however all mystical hollows are connected, so if you remove a treasure from one mystical hollow, it will be removed from all other mystical hollows.
    """

    # DO NOT MODIFY THIS ABSTRACT CLASS
    """
    Initialises the treasures in this hollow
    """

    def __init__(self) -> None:
        self.treasures = self.gen_treasures()
        self.restructure_hollow()

    @staticmethod
    def gen_treasures() -> List[Treasure]:
        """
        This is done here, so we can replace it later on in the auto marker.
        This method contains the logic to generate treasures for the hollows.

        Returns:
            List[Treasure]: A list of treasures that can be found in the maze
        """
        return generate_treasures()

    @abstractmethod
    def restructure_hollow(self):
        pass

    @abstractmethod
    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        pass

    def __len__(self) -> int:
        """
        After the restructure_hollow method is called, the treasures attribute should be updated
        don't create an additional attribute to store the number of treasures in the hollow.
        """
        return len(self.treasures)


class SpookyHollow(Hollow):

    def restructure_hollow(self) -> None:
        """
        Re-arranges the treasures in the hollow from a list to a new
        data structure that is better suited for the get_optimal_treasure method.

        The new treasures data structure can't be an ArrayR or list variant (LinkedList, python list, sorted list, ...).
        No lists! Breaching this will count as a major error and lose up to 100% of the marks of the task!

        Returns:
            None - This method should update the treasures attribute of the hollow

        Complexity:
            (This is the actual complexity of your code,
            remember to define all variables used.)
            Best Case Complexity: O(N * log N) - where N is the number of treasures. It will loop N times to add
                                the treasures into a list before constructing the BST. Then it takes O(N * log N) time
                                to construct the list into a BetterBST, where it uses mergesort to sort the treasures and
                                building a balance tree.
                                Please refer to "__build_balanced_tree" and "__sort_elements" in betterbst.py for detailed time complexity
            Worst Case Complexity: O(N * log N) - Same as best case. 

        Complexity requirements for full marks:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """
        treasure_tuples = []
        # O(N) - where N is the number of treasures in self.treasures. Best and worst case are same since each treasure
        # is iterated to calculate the ratio and appending it to the list.
        # Negative sign used here is to add the elements into the tree descendingly for future in-order traversal purpose
        for treasure in self.treasures:
            ratio = -treasure.value / treasure.weight
            treasure_tuples.append((ratio, treasure))

        # O(N*log N) - where N is the number of treasures. It will construct the better BST by first sorting all the
        # treasures according to the ratio with mergesort, which takes O(N*log N) time.
        # Please refer to __build_balanced_tree and __sort_elements for detailed time complexity
        self.treasures = BetterBST(treasure_tuples)

    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        """
        Removes the ideal treasure from the hollow
        Takes the treasure which has the greatest value / weight ratio
        that is less than or equal to the backpack_capacity of the player as
        we can't carry treasures that are heavier than our backpack capacity.

        Ensure there are only changes to the treasures contained in the hollow
        if there is a viable treasure to take. If there is a viable treasure
        only remove that treasure from the hollow, no other treasures should be removed.

        Returns:
            Treasure - the ideal treasure that the player should take.
            None - if all treasures are heavier than the backpack_capacity
            or the hollow is empty

        Complexity:
            (This is the actual complexity of your code,
            remember to define all variables used.)
            Best Case Complexity: O(log N) - where N is the number of treasures in the hollow. Best case occurs when
                                    the optimal treasure is found at the first retrieval which takes log N time, in a
                                    in-order traversal manner, which will be the leftmost element in this negated BST.
            Worst Case Complexity: O(N) - where N is the number of treasures in the hollow. Worst case occurs when
                                    the optimal treasure is found after several traversals in the BST in looking for
                                    the best treasure fitting within backpack capacity.

        Complexity requirements for full marks:
            Best Case Complexity: O(log(n))
            Worst Case Complexity: O(n)
            n is the number of treasures in the hollow
        """
        # Initialize variables for optimal treasure and its node
        optimal_treasure = None
        optimal_treasure_node = None

        # Iterate through treasures using in-order traversal
        # The first value onwards after multiplying (negative sign) again is in descending order,
        # hence it is checking the most optimal treasure with the greatest value/weight ratio.
        # Best case: O(log N) - where N is the number of treasures. The leftmost item in the in-order traversal is
        # retrieved in log N time, which is the highest ratio after negating it.
        # Worst case: O(N) - where N is the number of treasures to be iterated. Occurs if the first item is not optimal,
        # it will sequentially visit all the other nodes in-orderly (left subtree to current node to right subtree).
        for node in self.treasures:
            ratio, treasure = -node.key, node.item  # Convert back to positive ratio

            # Check if the treasure fits within the backpack capacity
            if treasure.weight <= backpack_capacity:
                optimal_treasure = treasure
                optimal_treasure_node = node
                break

        # If a suitable treasure is found, delete it and return
        # Delete here uses log N time to search for the node in a balanced BST and remove it.
        if optimal_treasure:
            del self.treasures[optimal_treasure_node.key]
            return optimal_treasure

        # Return None if no suitable treasure is found
        return None

    def __str__(self) -> str:
        return Tiles.SPOOKY_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)


class MysticalHollow(Hollow):

    def restructure_hollow(self):
        """
        Re-arranges the treasures in the hollow from a list to a new
        data structure that is better suited for the get_optimal_treasure method.

        The new treasures data structure can't be an ArrayR or list variant (LinkedList, python list, sorted list, ...).
        No lists! Breaching this will count as a major error and lose up to 100% of the marks of the task!

        Returns:
            None - This method should update the treasures attribute of the hollow

        Complexity:
            (This is the actual complexity of your code,
            remember to define all variables used.)
            Best Case Complexity: O(N) - where N is the number of treasures in the hollow. It iterates over all N
                                        number of treasures, calculating their ratio and adding them into the heap.
                                        Uses the time complexity mainly for adding the treasures into a list, and heapify method. 
            Worst Case Complexity: O(N) - Same as best case.

        Complexity requirements for full marks:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)
            Where n is the number of treasures in the hollow
        """
        # O(N) - where N is the number of treasures in self.treasures. Best and worst case are same since each treasure
        # is iterated to calculate the ratio and appending it to the list.
        treasure_tuples = []
        for treasure in self.treasures:
            ratio = treasure.value / treasure.weight
            treasure_tuples.append((ratio, treasure))

        # O(N) - where N is the number of treasures. It will construct a MaxHeap with the treasure tuples.
        # Overall time complexity occurs from heapify method from MaxHeap. 
        self.treasures = MaxHeap.heapify(treasure_tuples)

    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        """
        Removes the ideal treasure from the hollow
        Takes the treasure which has the greatest value / weight ratio
        that is less than or equal to the backpack_capacity of the player as
        we can't carry treasures that are heavier than our backpack capacity.

        Ensure there are only changes to the treasures contained in the hollow
        if there is a viable treasure to take. If there is a viable treasure
        only remove that treasure from the hollow, no other treasures should be removed.

        Returns:
            Treasure - the ideal treasure that the player should take.
            None - if all treasures are heavier than the backpack_capacity
            or the hollow is empty

        Complexity:
            (This is the actual complexity of your code,
            remember to define all variables used.)
            Best Case Complexity: O(log N) - where N is the number of treasures in the hollow. Best case occurs when the
                                    first get_max treasure's weight is within the backpack capacity, then it will break
                                    and return the treasure without checking temp_storage. Overall complexity depends on
                                    get_max() which is log N. Hence O(log N) in general.
            Worst Case Complexity: O(N * log N) - where N is the number of treasures in the hollow. Worst case occurs
                                    when the max ratio treasure is not within the backpack capacity, it will append it
                                    to a temporary storage for future usage (adding back to heap). Then it will continue
                                    iterating to get the next maximum ratio treasure, until it can fit into capacity.
                                    Overall, getting optimal treasure requires N number of times to iterate each treasure
                                    and log N time to get_max. Same goes to adding back the elements in the temporary storage
                                    into heap, it takes O(N * log N) time too, N number of elements in temp_storage and
                                    log N time to add.

        Complexity requirements for full marks:
            Best Case Complexity: O(log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """
        optimal_treasure = None
        temp_storage = []

        # Best case: O(log N) - where N is the number of treasures in the hollow. It immediately break and return the treasure
        # once the maximum ratio treasure's weight is within backpack capacity.
        # Worst case: O(N * log N) - where N is the number of treasures in the hollow. It will iterate N time getting the max 
        # and removing it until the weight is within backpack capacity, only when the treasure is retrieved or no more treasures
        # left it will break. 
        while optimal_treasure is None:
            if len(self.treasures) == 0:
                break
            # Extract the maximum ratio treasure
            ratio, treasure = self.treasures.get_max()

            if treasure.weight <= backpack_capacity:
                optimal_treasure = treasure
                break
            else:
                temp_storage.append((ratio, treasure))

        # Add back all treasures that were not suitable
        # Best case: O(1) if temp_storage is empty
        # Worst case: O(N * log N) where N is the number of treasures. If temp storage contain elements, it will iterate
        # each of them and add back into the heap.
        if temp_storage:
            for (ratio, treasure) in temp_storage:
                self.treasures.add((ratio, treasure))

        return optimal_treasure

    def __str__(self) -> str:
        return Tiles.MYSTICAL_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)
