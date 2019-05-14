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
class Connected_Obj(Enum):
    UP = (-1,0)
    DOWN = (1,0)
    RIGHT = (0,1)
    LEFT = (0,-1)
    DOWNRIGHT = (1,1)
    DOWNLEFT = (1,-1)
    UPRIGHT = (-1,1)
    UPLEFT = (-1,-1)

class Dungeon_Master:
    def __init__(self, n: int, m: int):
        self.dungeon = Dungeon(n,m,0,(0,0),(n-1,m-1)) 
        while True:
            choice = input("move - {w,a,s,d} or quit - {q}")
            if choice == "q":
                break
            else:
                if choice == "a":
                    self.move_explorer(Move.LEFT)
                if choice == "d":
                    self.move_explorer(Move.RIGHT)
                if choice == "w":
                    self.move_explorer(Move.UP)
                if choice == "s":
                    self.move_explorer(Move.DOWN)
        
    def move_explorer(self,move: Move):
        dungeon = self.dungeon
        sym: str = "o"
        end_loc = (dungeon.explorer_loc[0]+move.value[0],dungeon.explorer_loc[1]+move.value[1])
        if dungeon.set_cell(end_loc,sym,dungeon.entities):
            dungeon.set_cell(dungeon.explorer_loc,None,dungeon.entities)
            dungeon.explorer_loc = end_loc
        logging.info("{} moved from {} to {}".format(sym,dungeon.explorer_loc,end_loc))
        print(dungeon)

class Dungeon:
    def __init__(self, n: int, m: int,obsticles: int, start_loc:Tuple[int,int], goal_loc:Tuple[int,int]):
        self.map: List[List[str]] = []
        self.entities: List[List[str]] = []
        self.n = n
        self.m = m
        self.explorer_loc = start_loc
        self.goal_loc = goal_loc
        # adjacency matrix 
        self.build_boards()
        self.set_entity(start_loc,'o')
        self.set_entity(goal_loc,'*')
        print(self)

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
            lines += "\n"
        return lines

    def build_boards(self):
        self.map = Dungeon.build_board(self.n,self.m,".")
        self.entities = Dungeon.build_board(self.n,self.m,None)
        self.add_obstacles()

    @staticmethod
    def build_board(n: int, m: int,sym) -> List[List[str]]:
        result = []
        for i in range(n):
            row = [sym]*m
            result.append(row)
        return result

    def add_obstacles(self):
        obs_remaining: int = self.n*self.m//3
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


        



    def set_entity(self, loc:Tuple[int,int],sym: str): 
        if Dungeon.valid_loc(loc,self.n,self.m):
            self.entities[loc[0]][loc[1]] = sym
            logging.info(self.entities)
        else:
            logging.warning("invalid location {}".format(loc))
    
    @staticmethod
    def valid_loc(loc: Tuple[int,int],n: int, m: int):
        if loc[0] < 0 or loc[0] >= n:
            return False
        if loc[1] < 0 or loc[1] >= m:
            return False
        return True
    
    def get_cell(self,loc: Tuple[int,int], map: List[List[str]]):
        if Dungeon.valid_loc(loc,self.n,self.m):
            result = map[loc[0]][loc[1]]
            logging.info("got {} with value {}".format(loc,result))
            return result
        else:
            logging.warning("invalid location {}".format(loc))
            return None
        

    def set_cell(self, loc: Tuple[int,int], value: str, map: List[List[str]]):
        if Dungeon.valid_loc(loc,self.n,self.m):
            map[loc[0]][loc[1]] = value
            logging.info("set {} with value {}".format(loc,value))
            return True
        else:
            logging.warning("invalid location {}".format(loc))
            return False

class Traversal:
    @staticmethod
    def get_valid_obj_connections(r,c,n,m):
        result = set()
        for move in Connected_Obj:
            end_loc = (r+move.value[0],c+move.value[1])
            if Dungeon.valid_loc(end_loc,n,m):
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
                    logging.warning(f"visited {connection[0]} {connection[1]} from {r} {c}")
                    if Traversal.is_perimeter_cell(connection[0],connection[1],n,m):
                        perimeter_touches += 1
        return perimeter_touches
        

        

    

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    dungeon_master = Dungeon_Master(5,5)