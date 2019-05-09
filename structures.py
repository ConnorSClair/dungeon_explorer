from typing import *
from enum import *
import logging

class Move(Enum):
    UP = (-1,0)
    DOWN = (1,0)
    RIGHT = (0,1)
    LEFT = (0,-1)

class Dungeon_Master:
    def __init__(self, n: int, m: int):
        self.dungeon = Dungeon(n,m,0,(0,0),(n-1,m-1)) 
        
    def move_explorer(self,move: Move):
        self.dungeon.move_explorer(move)
        print(self.dungeon)

class Dungeon:
    def __init__(self, n: int, m: int,obsticles: int, start_loc:Tuple[int,int], goal_loc:Tuple[int,int]):
        self.map: List[List[str]] = []
        self.entities: List[List[str]] = []
        self.n = n
        self.m = m
        self.explorer_loc = start_loc
        self.goal_loc = goal_loc
        # adjacency matrix 
        self.build_board(obsticles)
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

    def build_board(self, obsticles: int):
        # initialise with 0s, 1s for obsticles randomly placed 
        for i in range(self.n):
            row = ['.']*self.m
            logging.info(row)
            self.map.append(row)
        logging.info(self.map)
        for i in range(self.n):
            row = [None]*self.m
            logging.info(row)
            self.entities.append(row)
        logging.info(self.entities)
    
    def move_explorer(self, move: Move):
        sym: str = self.get_cell(self.explorer_loc,self.entities)
        # check if valid
        end_loc = (self.explorer_loc[0]+move.value[0],self.explorer_loc[1]+move.value[1])
        if self.set_cell(end_loc,sym,self.entities):
            self.set_cell(self.explorer_loc,None,self.entities)
            self.explorer_loc = end_loc
        logging.info("{} moved from {} to {}".format(sym,self.explorer_loc,end_loc))

    def set_entity(self, loc:Tuple[int,int],sym: str): 
        if self.valid_loc(loc):
            self.entities[loc[0]][loc[1]] = sym
            logging.info(self.entities)
        else:
            logging.warning("invalid location {}".format(loc))
    
    def valid_move(self, loc: Tuple[int,int], move: Move):
        potential_move = (loc[0] + move.value[0],loc[1] + move.value[1])
        return self.valid_loc(potential_move)
    
    def valid_loc(self,loc: Tuple[int,int]):
        if loc[0] < 0 or loc[0] >= self.n:
            return False
        if loc[1] < 0 or loc[1] >= self.m:
            return False
        return True
    
    def get_cell(self,loc: Tuple[int,int], map: List[List[str]]):
        if self.valid_loc(loc):
            result = map[loc[0]][loc[1]]
            logging.info("got {} with value {}".format(loc,result))
        else:
            logging.warning("invalid location {}".format(loc))
        return result

    def set_cell(self, loc: Tuple[int,int], value: str, map: List[List[str]]):
        if self.valid_loc(loc):
            map[loc[0]][loc[1]] = value
            logging.info("set {} with value {}".format(loc,value))
            return True
        else:
            logging.warning("invalid location {}".format(loc))
            return False

class Explorer:
    @staticmethod
    def find_shortest_path(board,start,end):
        return "todo"
    

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.WARNING,
                        datefmt="%H:%M:%S")
    
    dungeon_master = Dungeon_Master(14,8)
    
    while True:
        choice = input("move - {left,right,up,down} or quit - {quit}")
        if choice == "quit":
            break
        else:
            if choice == "left":
                dungeon_master.move_explorer(Move.LEFT)
            if choice == "right":
                dungeon_master.move_explorer(Move.RIGHT)
            if choice == "up":
                dungeon_master.move_explorer(Move.UP)
            if choice == "down":
                dungeon_master.move_explorer(Move.DOWN)
            



    
