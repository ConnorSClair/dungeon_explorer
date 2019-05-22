from typing import *
from enum import *
import logging
from random import randrange
from collections import deque


class Move(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)


class Connected_Cells(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)
    DOWNRIGHT = (1, 1)
    DOWNLEFT = (1, -1)
    UPRIGHT = (-1, 1)
    UPLEFT = (-1, -1)


class Dungeon_Master:
    """ Has instance of dungeon, runs game, takes path from shortest path & send commands to move_explorer,
    """

    def __init__(self, n: int, m: int):
        print("Dungeon Explorer")
        while True:
            self.dungeon = self.game_options()
            self.run_game()
            self.quit_game()
            

    def quit_game(self):
        response = input("Play again? {y/n}\n")
        if response != "y":
            print("See you next time!")
            exit(0)


    def game_options(self):
        difficulty = input("How difficult do you want the game to be? {easy, medium, hard}\n")
        if difficulty == "easy":
            obstacles = 4
        elif difficulty == "medium":
            obstacles = 3
        elif difficulty == "hard":
            obstacles = 2
        else:
            print("Invalid difficulty")
            exit(1)
        
        cols = int(input("What would you like the width of your dungeon to be? {2-100}\n"))
        rows = int(input("What would you like the height of your dungeon to be? {2-100}\n"))
        if cols < 2 or cols > 100 or rows < 2 or rows > 100:
            print("Invalid map size")
            exit(2)
        
        goal_row = randrange(0,rows)
        goal_col = randrange(0,cols)
        start_row = randrange(0,rows)
        start_col = randrange(0,cols)

        return Dungeon(rows,cols,obstacles,(start_row,start_col),(goal_row,goal_col))


    def run_game(self):
        """ Handles user input including player movement and quiting
        """
        print("\n")
        print("Move the player (o) to the goal (*) in the least number of moves")
        count = 0
        paths = Traversal.search_goal(self.dungeon.explorer_loc,self.dungeon.map, self.dungeon.FLOOR)
        path_to_goal = paths[self.dungeon.goal_loc[0]][self.dungeon.goal_loc[1]]
        min_moves = len(path_to_goal)
        while not self.dungeon.is_game_over():
            print(self.dungeon)
            print(f"Movecount: {count} | Goal: {min_moves} moves")
            choice = input("move - {w,a,s,d} or get help - {help} or quit - {q}")
            if choice == "q":
                self.quit_game()
            else:
                moved = False
                if choice == "a":
                    moved = self.dungeon.move_explorer(Move.LEFT)
                if choice == "d":
                    moved = self.dungeon.move_explorer(Move.RIGHT)
                if choice == "w":
                    moved = self.dungeon.move_explorer(Move.UP)
                if choice == "s":
                    moved = self.dungeon.move_explorer(Move.DOWN)
                if choice == "help":
                    paths = Traversal.search_goal(self.dungeon.explorer_loc,self.dungeon.map, self.dungeon.FLOOR)
                    best_move = paths[self.dungeon.goal_loc[0]][self.dungeon.goal_loc[1]][0]
                    print(f"Best move is to row {best_move[0]} and column {best_move[1]}")
                if moved:
                    count += 1
        if self.dungeon.is_game_over():
            if count == min_moves:
                print(f"Well done, you reached the goal in the smallest number of steps - {count} steps!")
            elif count > min_moves:
                print(f"Try again, you took {count} steps but could have made it in {min_moves} steps!")
            else:
                print(f"Congratulations! You beat my shortest path algorithm. Somehow?!")
        

    def run_explorer_shortest_path(self):
        #
        return 0


class Dungeon:
    def __init__(self, rows: int, cols: int, obstacles: int, start_loc: Tuple[int, int], goal_loc: Tuple[int, int]):
        self.map: List[List[str]] = []
        self.entities: List[List[str]] = []
        self.rows = rows
        self.cols = cols
        self.explorer_loc = start_loc
        self.goal_loc = goal_loc
        self.obstacles = obstacles

        self.FLOOR = "."
        self.EXPLORER = "o"
        self.GOAL = "*"
        self.OBSTACLE = '/'

        # adjacency matrix
        self.build_boards()
        self.add_obstacles(self.rows*self.cols//self.obstacles)
        self.set_entity(self.explorer_loc[0],
                        self.explorer_loc[1], self.EXPLORER)
        self.set_entity(self.goal_loc[0], self.goal_loc[1], self.GOAL)

    def is_game_over(self) -> bool:
        return self.explorer_loc == self.goal_loc

    def __repr__(self) -> str:
        return self.game_view()

    def game_view(self) -> str:
        result: List[List[str]] = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if self.entities[i][j] == None:
                    row.append(self.map[i][j])
                else:
                    row.append(self.entities[i][j])
            result.append(row)
        lines = ""
        for i in range(self.rows):
            lines += "".join(result[i])
            if i < self.rows - 1:
                lines += "\n"
            # last row, don't print new line
        return lines

    def board_view(self, board: List[List[str]]) -> str:
        lines = ""
        for i in range(len(board)):
            lines += "".join(board[i])
            if i < self.rows - 1:
                lines += "\n"
            # last row, don't print new line
        return lines

    def build_boards(self):
        self.map = Dungeon.build_board(self.rows, self.cols, self.FLOOR)
        self.entities = Dungeon.build_board(self.rows, self.cols, None)

    @staticmethod
    def build_board(n: int, m: int, sym) -> List[List[str]]:
        result = []
        for i in range(n):
            row = [sym]*m
            result.append(row)
        return result

    def add_obstacles(self, obs: int):
        max_obs = self.rows*self.cols//2
        if obs > max_obs:
            obs_remaining = max_obs
        obs_remaining = obs
        while obs_remaining > 0:
            row: int = randrange(0, self.rows)
            col: int = randrange(0, self.cols)
            if (row, col) == self.explorer_loc \
                    or (row, col) == self.goal_loc:
                continue
            self.map[row][col] = self.OBSTACLE
            perimeter_touches = Traversal.search(
                row, col, self.rows, self.cols, self.map, self.OBSTACLE)
            logging.info(perimeter_touches)
            if perimeter_touches > 1:
                self.map[row][col] = self.FLOOR
            else:
                obs_remaining -= 1

    @staticmethod
    def valid_board_loc(row: int, col: int, rows: int, cols: int):
        if row < 0 or row >= rows:
            return False
        if col < 0 or col >= cols:
            return False
        return True

    def entity_collision(self, row: int, col: int):
        return self.get_cell(row, col, self.map) == "/"

    def get_cell(self, row: int, col: int, map: List[List[str]]):
        if Dungeon.valid_board_loc(row, col, self.rows, self.cols):
            result = map[row][col]
            logging.info("got {} with value {}".format((row, col), result))
            return result
        else:
            logging.warn(
                "invalid location - this should not happen {}".format((row, col)))
            return None

    def set_cell(self, row: int, col: int, value: str, map: List[List[str]]):
        if Dungeon.valid_board_loc(row, col, self.rows, self.cols):
            map[row][col] = value
            logging.info("set {} with value {}".format((row, col), value))
            return True
        else:
            logging.info("invalid location {}".format((row, col)))
            return False

    def set_entity(self, row: int, col: int, sym: str):
        if Dungeon.valid_board_loc(row, col, self.rows, self.cols) and not self.entity_collision(row, col):
            self.entities[row][col] = sym
            logging.info(self.entities)
        else:
            logging.warning("invalid location {}".format((row, col)))

    def move_explorer(self, move: Move) -> bool:
        end_row = self.explorer_loc[0]+move.value[0]
        end_col = self.explorer_loc[1]+move.value[1]
        if self.valid_board_loc(end_row, end_col, self.rows, self.cols) and self.get_cell(end_row, end_col, self.map) != self.OBSTACLE:
            self.set_cell(end_row, end_col, self.EXPLORER, self.entities)
            # explorer moves, so set previous explorer location to None
            self.set_cell(
                self.explorer_loc[0], self.explorer_loc[1], None, self.entities)
            self.explorer_loc = (end_row, end_col)
            logging.info("{} moved from {} to the {}".format(
                self.EXPLORER, self.explorer_loc, move))
            return True
        else:
            return False


class Traversal:
    # make traversal methods non static?
    # return Traversal object containing paths and perimeter touches

    @staticmethod
    def get_valid_obj_connections(row, col, rows, cols, explorer: bool):
        result = set()
        if explorer:
            connected_cells = Move
        else:
            connected_cells = Connected_Cells
        # connected cells depends if explorer or terrain
        for move in connected_cells:
            end_row = row + move.value[0]
            end_col = col + move.value[1]
            if Dungeon.valid_board_loc(end_row, end_col, rows, cols):
                result.add((end_row, end_col))
        return result

    @staticmethod
    def is_perimeter_cell(row, col, rows, cols):
        return row == 0 or row == rows - 1 or col == 0 or col == cols - 1

    @staticmethod
    def search(start_r, start_c, rows, cols, map, sym):
        visited = Dungeon.build_board(rows, cols, False)
        paths = Dungeon.build_board(rows, cols, [])
        to_explore_r = deque()
        to_explore_c = deque()
        # start at loc r c
        to_explore_r.append(start_r)
        to_explore_c.append(start_c)
        visited[start_r][start_c] = True
        paths[start_r][start_c] = [(start_r, start_c)]
        perimeter_touches = 0
        if Traversal.is_perimeter_cell(start_r, start_c, rows, cols):
            perimeter_touches += 1
        while len(to_explore_c) > 0:
            # explore node
            # add unvisited to explore
            r = to_explore_r.popleft()
            c = to_explore_c.popleft()
            for connection in Traversal.get_valid_obj_connections(r, c, rows, cols, False):
                if map[connection[0]][connection[1]] == '/' and not visited[connection[0]][connection[1]]:
                    to_explore_r.append(connection[0])
                    to_explore_c.append(connection[1])
                    visited[connection[0]][connection[1]] = True
                    paths[connection[0]][connection[1]] = paths[r][c].copy()
                    paths[connection[0]][connection[1]].append(
                        (connection[0], connection[1]))
                    logging.info(
                        f"visited {connection[0]} {connection[1]} from {r} {c}")
                    if Traversal.is_perimeter_cell(connection[0], connection[1], rows, cols):
                        perimeter_touches += 1
        return perimeter_touches

    @staticmethod
    def search_goal(start_loc, map, sym):
        row = start_loc[0]
        col = start_loc[1]
        rows = len(map)
        cols = len(map[0])
        visited = Dungeon.build_board(rows, cols, False)
        paths = Dungeon.build_board(rows, cols, [])
        to_explore_r = deque()
        to_explore_c = deque()
        # start at loc r c
        visited[row][col] = True
        to_explore_r.append(row)
        to_explore_c.append(col)
        paths[row][col] = []
        while len(to_explore_c) > 0:
            # explore node
            # add unvisited to explore
            r = to_explore_r.popleft()
            c = to_explore_c.popleft()
            for connection in Traversal.get_valid_obj_connections(r, c, rows, cols, True):
                if map[connection[0]][connection[1]] == '.' and not visited[connection[0]][connection[1]]:
                    to_explore_r.append(connection[0])
                    to_explore_c.append(connection[1])
                    visited[connection[0]][connection[1]] = True
                    paths[connection[0]][connection[1]] = paths[r][c].copy()
                    paths[connection[0]][connection[1]].append(
                        connection)
                    logging.info(
                        f"visited {connection[0]} {connection[1]} from {r} {c}")
        return paths


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.WARN,
                        datefmt="%H:%M:%S")

    dungeon_master = Dungeon_Master(20, 20)
