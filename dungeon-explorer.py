from typing import *
from enum import *
import logging
from random import randrange
from collections import deque

class Move(Enum):
    UP = (-1,0)
    DOWN = (1,0)
    RIGHT = (0,1)
    LEFT = (0,-1)

class Connected_Cells(Enum):
    UP = (-1,0)
    DOWN = (1,0)
    RIGHT = (0,1)
    LEFT = (0,-1)
    DOWNRIGHT = (1,1)
    DOWNLEFT = (1,-1)
    UPRIGHT = (-1,1)
    UPLEFT = (-1,-1)

class Loc():
    def __init__(self, r: int, c: int):
        self.r = r
        self.c = c


class Dungeon_Master:
    """ Has instance of dungeon, runs game, takes path from shortest path & send commands to move_explorer,
    """
    def __init__(self, n: int, m: int):
        self.dungeon = Dungeon(n,m,0,(0,0),(n-1,m-1)) 
        self.run_game()

    def run_game(self):
        print("\n")
        print("Move the player (o) to the goal (*) in the least number of moves")
        count = 0
        while not self.dungeon.is_game_over():
            print(self.dungeon)
            print(f"Movecount: {count}")
            choice = input("move - {w,a,s,d} or quit - {q}")
            if choice == "q":
                print("quit game")
                break
            else:
                moved = False
                if choice == "a":
                    moved = self.move_explorer(Move.LEFT)
                if choice == "d":
                    moved = self.move_explorer(Move.RIGHT)
                if choice == "w":
                    moved = self.move_explorer(Move.UP)
                if choice == "s":
                    moved = self.move_explorer(Move.DOWN)
                if moved:
                    count += 1
        print(self.dungeon)
        print(f"Well done, you reached the goal in {count} moves")
        
    def run_explorer_shortest_path(self):
        # 
        return 0

    def move_explorer(self,move: Move) -> bool:
        dungeon = self.dungeon
        sym: str = "o"
        end_loc = (dungeon.explorer_loc[0]+move.value[0],dungeon.explorer_loc[1]+move.value[1])
        if dungeon.valid_board_loc(end_loc,dungeon.n,dungeon.m) and dungeon.get_cell(end_loc[0],end_loc[1],dungeon.map) != "/":
            dungeon.set_cell(end_loc,sym,dungeon.entities)
            dungeon.set_cell(dungeon.explorer_loc,None,dungeon.entities)
            dungeon.explorer_loc = end_loc
            logging.info("{} moved from {} to {}".format(sym,dungeon.explorer_loc,end_loc))
            return True
        else:
            return False
        

class Dungeon:
    def __init__(self, n: int, m: int,obsticles: int, start_loc:Tuple[int,int], goal_loc:Tuple[int,int]):
        self.map: List[List[str]] = []
        self.entities: List[List[str]] = []
        self.n = n
        self.m = m
        self.explorer_loc = start_loc
        self.goal_loc = goal_loc

        self.EXPLORER = "o"
        self.GOAL = "*"
        self.obstacle = '/'

        # adjacency matrix 
        self.build_boards()
        self.add_obstacles(self.n*self.m//2)
        self.set_entity(self.explorer_loc[0],self.explorer_loc[1],self.EXPLORER)
        self.set_entity(self.goal_loc[0],self.goal_loc[1],self.GOAL)

    def is_game_over(self) -> bool:
        return self.explorer_loc == self.goal_loc


    def __repr__(self):
        result: List[List[str]] = []
        for i in range(self.n):
            row = []
            for j in range(self.m):
                if self.entities[i][j] == None:
                    row.append(self.map[i][j])
                else:
                    row.append(self.entities[i][j])
            result.append(row)
        lines = ""
        for i in range(self.n):
            lines += "".join(result[i])
            if i < self.n - 1:
                lines += "\n"
            # last row, don't print new line
        return lines

    def build_boards(self):
        self.map = Dungeon.build_board(self.n,self.m,".")
        self.entities = Dungeon.build_board(self.n,self.m,None)
        
    @staticmethod
    def build_board(n: int, m: int,sym) -> List[List[str]]:
        result = []
        for i in range(n):
            row = [sym]*m
            result.append(row)
        return result

    def add_obstacles(self, obs: int):
        max_obs = self.n*self.m//3
        if obs > max_obs:
            obs_remaining = max_obs
        obs_remaining = obs
        while obs_remaining > 0:
            row: int= randrange(0,self.n)
            col: int = randrange(0,self.m)
            if (row,col) == self.explorer_loc \
                or (row,col) == self.goal_loc:
                continue
            self.map[row][col] = "/"
            perimeter_touches = Traversal.search(row,col,self.n,self.m,self.map,"/")
            logging.info(perimeter_touches)
            if perimeter_touches > 1:
                self.map[row][col] = "."
            else:
                obs_remaining -= 1

    @staticmethod
    def valid_board_loc(loc: Tuple[int,int],n: int, m: int):
        if loc[0] < 0 or loc[0] >= n:
            return False
        if loc[1] < 0 or loc[1] >= m:
            return False
        return True
    
    def entity_collision(self, r: int, c: int):
        return self.get_cell(r,c,self.map) == "/"

    def get_cell(self,r: int, c: int, map: List[List[str]]):
        if Dungeon.valid_board_loc((r,c),self.n,self.m):
            result = map[r][c]
            logging.info("got {} with value {}".format((r,c),result))
            return result
        else:
            logging.warn("invalid location - this should not happen{}".format((r,c)))
            return None

    def set_cell(self, loc: Tuple[int,int], value: str, map: List[List[str]]):
        if Dungeon.valid_board_loc(loc,self.n,self.m):
            map[loc[0]][loc[1]] = value
            logging.info("set {} with value {}".format(loc,value))
            return True
        else:
            logging.info("invalid location {}".format(loc))
            return False

    def set_entity(self, r:int, c:int,sym: str): 
        if Dungeon.valid_board_loc((r,c),self.n,self.m) and not self.entity_collision(r,c):
            self.entities[r][c] = sym
            logging.info(self.entities)
        else:
            logging.warning("invalid location {}".format((r,c)))

    def move_explorer(self,move: Move):
        #todo
        end_loc = (dungeon.explorer_loc[0]+move.value[0],dungeon.explorer_loc[1]+move.value[1])
        if dungeon.valid_board_loc(end_loc,dungeon.n,dungeon.m) and dungeon.get_cell(end_loc,dungeon.map) != "/":
            dungeon.set_cell(end_loc,sym,dungeon.entities)
            dungeon.set_cell(dungeon.explorer_loc,None,dungeon.entities)
            dungeon.explorer_loc = end_loc
        logging.info("{} moved from {} to {}".format(sym,dungeon.explorer_loc,end_loc))
        print(dungeon)
    

class Traversal:
    # make traversal methods non static? 
    # return Traversal object containing paths and perimeter touches 

    @staticmethod
    def get_valid_obj_connections(r,c,n,m):
        result = set()
        for move in Connected_Cells:
            end_loc = (r+move.value[0],c+move.value[1])
            if Dungeon.valid_board_loc(end_loc,n,m):
                result.add(end_loc)
        return result
    
    @staticmethod
    def is_perimeter_cell(r,c,n,m):
        return r == 0 or r == n - 1 or c == 0 or c == m - 1
    
    @staticmethod
    def search(start_r,start_c,n,m,map,sym):
        visited = Dungeon.build_board(n,m,False)
        paths = Dungeon.build_board(n,m,[])
        to_explore_r = deque()
        to_explore_c = deque()
        # start at loc r c
        visited[start_r][start_c] = True
        to_explore_r.append(start_r)
        to_explore_c.append(start_c)
        paths[start_r][start_c] = [(start_r,start_c)]
        perimeter_touches = 0
        if Traversal.is_perimeter_cell(start_r,start_c,n,m):
            perimeter_touches += 1
        while len(to_explore_c) > 0:
            # explore node
            # add unvisited to explore
            r = to_explore_r.popleft()
            c = to_explore_c.popleft()
            for connection in Traversal.get_valid_obj_connections(r,c,n,m):
                if map[connection[0]][connection[1]] == '/' and not visited[connection[0]][connection[1]]:
                    to_explore_r.append(connection[0])
                    to_explore_c.append(connection[1])
                    visited[connection[0]][connection[1]] = True
                    paths[connection[0]][connection[1]] = paths[r][c].copy()
                    paths[connection[0]][connection[1]].append((connection[0],connection[1]))
                    logging.info(f"visited {connection[0]} {connection[1]} from {r} {c}")
                    if Traversal.is_perimeter_cell(connection[0],connection[1],n,m):
                        perimeter_touches += 1
        return perimeter_touches

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.WARN,
                        datefmt="%H:%M:%S")
    
    dungeon_master = Dungeon_Master(10,10)