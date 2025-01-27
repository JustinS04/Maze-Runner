from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
from config import Directions, Tiles
from hollows import Hollow, MysticalHollow, SpookyHollow
from treasure import Treasure


class Position:
    def __init__(self, row: int, col: int) -> None:
        """
        Args:
            row(int): Row number in this maze cell position
            col(int): Column number in this maze cell position
        """
        self.row: int = row
        self.col: int = col

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Position) and value.row == self.row and value.col == self.col

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"


@dataclass
class MazeCell:
    tile: str | Hollow
    position: Position
    visited: bool = False

    def __str__(self) -> str:
        return str(self.tile)

    def __repr__(self) -> str:
        return f"'{self.tile}'"


class Maze:
    directions: dict[Directions, Tuple[int, int]] = {
        Directions.UP: (-1, 0),
        Directions.DOWN: (1, 0),
        Directions.LEFT: (0, -1),
        Directions.RIGHT: (0, 1),
    }

    def __init__(self, start_position: Position, end_positions: List[Position], walls: List[Position], hollows: List[tuple[Hollow, Position]], rows: int, cols: int) -> None:
        """
        Constructs the maze you should never be interacting with this method.
        Please take a look at `load_maze_from_file` & `sample1`

        Args:
            start_position(Position): Starting position in the maze.
            end_positions(List[Position]): End positions in the maze.
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            rows(int): Number of rows in the maze.
            cols(int): Number of columns in the maze.

        Complexity:
            Best Case Complexity: O(_create_grid)
            Worst Case Complexity: O(_create_grid)
        """
        self.start_position: Position = start_position
        self.end_positions: List[Position] = end_positions
        self.rows: int = rows
        self.cols: int = cols
        self.grid: List[List[MazeCell]] = self._create_grid(walls, hollows, end_positions)

    def _create_grid(self, walls: List[Position], hollows: List[(Hollow, Position)], end_positions: List[Position]) -> List[List[MazeCell]]:
        """
        Args:
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            end_positions(List[Position]): End positions in the maze.

        Return:
            List[MazeCell]: The generated maze grid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.
        """
        grid: List[List[MazeCell]] = [[MazeCell(' ', Position(i, j))
                                       for j in range(self.cols)] for i in range(self.rows)]
        grid[self.start_position.row][self.start_position.col] = MazeCell(
            Tiles.START_POSITION.value, self.start_position)
        for wall in walls:
            grid[wall.row][wall.col].tile = Tiles.WALL.value
        for hollow, pos in hollows:
            grid[pos.row][pos.col].tile = hollow
        for end_position in end_positions:
            grid[end_position.row][end_position.col].tile = Tiles.EXIT.value
        return grid

    @staticmethod
    def validate_maze_file(maze_name: str) -> None:
        """
        Mazes must have the following:
        - A start position (P)
        - At least one exit (E)
        - All rows must have the same number of columns
        - Tiles are representations can be found in config.py
        - At least one treasure

        Args:
            maze_name(str): The name of the maze.

        Raises:
            ValueError: If maze_name is invalid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            Assuming dictionary operations can be done on O(1) time.
        """
        tile_count: dict[str, int] = {}
        with open(f"./mazes/{maze_name}", 'r') as f:
            lines: List[str] = f.readlines()
            cols: int = len(lines[0].strip())
            for line in lines:
                if len(line.strip()) != cols:
                    raise ValueError(f"Uneven columns in {maze_name} ensure all rows have the same number of columns")
                # Check tiles
                for tile in line.strip():
                    if tile not in tile_count:
                        tile_count[tile] = 1
                    else:
                        tile_count[tile] += 1
        if 'P' not in tile_count or 'E' not in tile_count:
            raise ValueError(f"Missing start or end position in {maze_name}")

        if tile_count['P'] > 1:
            raise ValueError(f"Multiple start positions found in {maze_name}")

        # Check we have at least one treasure
        if not (Tiles.SPOOKY_HOLLOW.value in tile_count or Tiles.MYSTICAL_HOLLOW.value in tile_count):
            raise ValueError(f"No treasures found in {maze_name}")

        valid_types: List[str] = [tile.value for tile in Tiles]
        invalid_tiles: List[str] = [tile for tile in tile_count if tile not in valid_types]
        if invalid_tiles:
            raise ValueError(f"Invalid tile(s) found in {maze_name} ({invalid_tiles})")

    @classmethod
    def load_maze_from_file(cls, maze_name: str) -> Maze:
        """
        Args:
            maze_name(str): The maze name to load the maze from.

        Return:
            Maze: The newly created maze instance.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            For small mazes we assume the lists we not need to resize.
        """
        cls.validate_maze_file(maze_name)
        end_positions, walls, hollows = [], [], []
        mystical_hollow: MysticalHollow = MysticalHollow()
        start_position: Position | None = None
        with open(f"./mazes/{maze_name}", 'r') as f:
            lines: List[str] = f.readlines()
            rows: int = len(lines)
            cols: int = len(lines[0].strip())
            for i, line in enumerate(lines):
                for j, tile in enumerate(line.strip()):
                    if tile == Tiles.START_POSITION.value:
                        start_position: Position = Position(i, j)
                    elif tile == Tiles.EXIT.value:
                        end_positions.append(Position(i, j))
                    elif tile == Tiles.WALL.value:
                        walls.append(Position(i, j))
                    elif tile == Tiles.SPOOKY_HOLLOW.value:
                        hollows.append((SpookyHollow(), Position(i, j)))
                    elif tile == Tiles.MYSTICAL_HOLLOW.value:
                        hollows.append((mystical_hollow, Position(i, j)))
        assert start_position is not None
        return Maze(start_position, end_positions, walls, hollows, rows, cols)

    def is_valid_position(self, position: Position) -> bool:
        """
        Checks if the position is within the maze and not blocked by a wall.

        Args:
            position (Position): The position to check.

        Returns:
            bool - True if the position is within the maze and not blocked by a wall / hollow.

        Complexity:
            Best Case Complexity: O(1) - Assignment operations and checking of bounds and tiles take constant time.
            Worst Case Complexity: O(1) - Assignment operations and checking of bounds and tiles take constant time.
        """
        row, col = position.row, position.col
        return (0 <= row < self.rows) and (0 <= col < self.cols) and (self.grid[row][col].tile != Tiles.WALL.value)

    def get_available_positions(self, current_position: Position) -> List[Position]:
        """
        Returns a list of all the new possible you can move to from your current position.

        Args:
            current_position (Position): Your current position.

        Returns:
            List[Position] - A list of all the new possible you can move to from your current position.

        Complexity:
            Best Case Complexity: O(1) - The loop iterates over a fixed number of directions (UP, DOWN, LEFT, RIGHT),
                                and each operation of assignment, addition, is_valid_position, append and return are
                                all constant time. It checks whether that particular position moved, is available, if
                                it is, then append to the available position list.
                                Since there are always 4 directions, the total time remains constant.
            Worst Case Complexity: O(1) - Same as best case
        """
        available_positions = []
        # Iterate through each direction and its corresponding row(dr) / column(dc) changes
        for direction, (dr, dc) in self.directions.items():
            new_position = Position(current_position.row + dr, current_position.col + dc)
            # Check if the new position is valid
            if self.is_valid_position(new_position):
                available_positions.append(new_position)
        return available_positions

    def find_way_out(self) -> List[Position] | None:
        """
        Finds a way out of the maze in some cases there may be multiple exits
        or no exits at all.

        Returns:
            List[Position]: If there is a way out of the maze, 
            the path will be made up of the coordinates starting at 
            your original starting point and ending at the exit.

            None: Unable to find a path to the exit, simply return None.

        Complexity:
            Best Case Complexity: O(N) - where N is the number of cells in the maze
                                    - Best case of "self.find_path_aux"
            Worst Case Complexity: O(N) - where N is the number of cells in the maze
                                    - Worst case of "self.find_path_aux"
        """
        start: Position = self.start_position
        path = []
        return self.find_path_aux(start, path)

    def find_path_aux(self, current_position: Position, path: list[Position]) -> list[Position] | None:
        """
        Recursive helper function to find a path to an exit in the maze.

        This function uses a depth-first search (DFS) starting from the current position
        and try to find a path to one of the exit positions. It uses recursion to explore
        possible paths and backtracks when a path is invalid or already visited.

        Args:
            current_position (Position): The current position in the maze during the search.
            path (list[Position]): The list of positions representing the current path that is explored.

        Returns:
            list[Position]: The path from the start position to an exit, if found.
            None: If no path to an exit is found.

        Complexity:
            Best Case Complexity: O(N) - where N is the number of cells in the maze. Best case occurs when the shortest
                                    path is found to reach the exit. While considering the DFS search, the best case
                                    could happen in the most minimal backtracking since the exit is found directly.
            Worst Case Complexity: O(N) - where N is the number of cells in the maze. Worst case occurs when every single
                                    cell in the maze are encountered. While considering the DFS search, it should account
                                    for all cells' visits if there is no path to an exit or exits are very far from start.
                                    Hence, we could analyze the time complexity such that it uses N time to enter during
                                    exploration, and N time to exit during backtracking, making the overall complexity
                                    O(N + N).
                                    For example, one of the worst case would be a maze contain 10 cells, with no exit,
                                    it will need to explore the 10 cells until all are visited, and backtrack the 10 cells
                                    to look for other path, which yet result in no exit.
        """
        # If current_position is on any of the end_positions, simply add the position to the path list and return it.
        if current_position in self.end_positions:
            path.append(current_position)
            return path

        else:
            cell = self.grid[current_position.row][current_position.col]
            if cell.visited:
                return None  # Skip if already visited

            # Mark the current cell as visited
            cell.visited = True
            path.append(current_position)

            # O(1) - Get available positions in the specified order: UP, DOWN, LEFT, RIGHT
            available_positions = self.get_available_positions(current_position)

            # Explore each available position recursively
            # O(N) - where N is the number of cells in the maze. The iteration of available positions is fixed at 4
            # hence it is always multiplying the cell with a range of 0-4. The main time complexity is analyzed where
            # the cell or positions are encountered, resulting in a path towards the exit.
            # Best case could be O(N), that it requires fewer steps reaching the end.
            # Worst case could also be O(N), where it requires all the cell in the maze to reach the end.
            for next_position in available_positions:
                result = self.find_path_aux(next_position, path)
                if result is not None:
                    return result

            # O(1) - Backtrack: remove current position from path
            path.remove(current_position)
            return None

    def take_treasures(self, path: List[MazeCell], backpack_capacity: int) -> List[Treasure] | None:
        """
        You must take the treasures in the order they appear in the path selecting treasures
        that have the highest value / weight ratio.
        Remember the total of treasures cannot exceed backpack_capacity, which means
        Individual treasures cannot exceed this value either.

        Should there be no treasures that are viable please return an empty list.

        You do not have to validate the path, it is guaranteed to be a valid path.

        Args:
            path (List[MazeCell]): The path you took to reach the exit.
            backpack_capacity (int): The maximum weight you can carry.

        Returns:
            List[Treasure] - List of the most optimal treasures.
            None - If there are no treasures to take.

        Complexity:
            Best Case Complexity: O(N * (log T)) - where N is the number of cells throughout the path and T is the number of
                                    treasures in the hollow. Best case occurs when a spooky hollow is encountered,
                                    and the best case of spooky_hollow.get_optimal_treasure when spooky hollow occurred.
                                    Please refer to "spooky_hollow.get_optimal_treasure" for more time complexity analysis.
            Worst Case Complexity: O(N * (T * log T)) - where N is the number of cells throughout the path, and T is
                                    the number of treasures in the hollow. Worst case when the hollow is mystical,
                                    mystical requires  O(T * log T) in the worst case for mystical_hollow.get_optimal_treasure().
                                    Please refer to "mystical_hollow.get_optimal_treasure" for more time complexity analysis.
            
                        - Overall, it will loop through each cell in the path to check if the tile is a hollow, if it is, the 
                        time complexity depends if its a spooky hollow or a mystical hollow. If both are met, it will still 
                        follow the worst case of O(N * (T * log T)).

        """
        treasures_taken = []

        # Best case: O(N * (log T)) - where N is the number of cells throughout the path. Occurs when spooky hollow encountered.
        # Worst case: O(N * (T * log T)) - where T is the number of treasures collected. Worst case occurs when mystical hollow encountered,
        for cell in path:
            if isinstance(cell.tile, Hollow):
                # Attempt to get the optimal treasure within capacity
                optimal_treasure = cell.tile.get_optimal_treasure(backpack_capacity)

                # If optimal treasure is found and weight within backpack capacity, the treasure is appended into a list
                # and subtraction on the backpack capacity is performed.
                if optimal_treasure and optimal_treasure.weight <= backpack_capacity:
                    treasures_taken.append(optimal_treasure)
                    backpack_capacity -= optimal_treasure.weight

        # If treasures taken contain elements, return the list.
        if treasures_taken:
            return treasures_taken

        return None

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """
        Returns the grid in a human-readable format.

        Complexity:
        Best Case Complexity: O(n) where n is the number of cells in the maze.
        Worst Case Complexity: O(n) where n is the number of cells in the maze.
        """
        my_grid: str = ""
        for row in self.grid:
            my_grid += "" if my_grid == "" else "\n"
            my_grid += str(row)

        return my_grid


def sample1() -> None:
    maze = Maze.load_maze_from_file("sample.txt")
    print(maze)


def sample2() -> None:
    maze = Maze.load_maze_from_file("sample2.txt")
    print(maze)
    # Samples as to how the grid / maze cells work
    r, c = 4, 0  # row 4, col 0
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))
    r, c = 2, 3  # row 2, col 3
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))


if __name__ == "__main__":
    sample1()
    directions: dict[Directions, Tuple[int, int]] = {
        Directions.UP: (-1, 0),
        Directions.DOWN: (1, 0),
        Directions.LEFT: (0, -1),
        Directions.RIGHT: (0, 1),
    }
