from typing import *
from enum import *
import logging

class Move(Enum):
    LEFT = (-1,0)
    RIGHT = (1,0)
    DOWN = (0,1)
    UP = (0,-1)

class Dungeon_Master:
    def __init__(self, n: int, m: int):
        self.dungeon = Dungeon(n,m,0,(0,0),(n-1,m-1))   
        
    def move_explorer(self,move: Move):

    



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
        self.set_entities((0,0),(n-1,m-1))

    def __repr__(self):
        lines = ""
        for i in range(self.n):
            lines += "".join(self.map[i])
            lines += "\n"
        
        return lines

    def build_board(self, obsticles: int):
        # initialise with 0s, 1s for obsticles randomly placed 
        for i in range(self.n):
            row = ['.']*self.m
            logging.info(row)
            self.map.append(row)
        logging.info(self.map)
    
    def set_entities(self, start_loc:Tuple[int,int], goal_loc:Tuple[int,int]): 
        if self.valid_loc(start_loc):
            self.map[start_loc[0]][start_loc[1]] = 'o'
        else:
            logging.warn("invalid location {}".format(start_loc))
        if self.valid_loc(goal_loc):
            self.map[goal_loc[0]][goal_loc[1]] = '*'
        else:
            logging.warn("invalid location {}".format(goal_loc))
    
    def valid_move(self, loc: Tuple[int,int], move: Move):
        potential_move = (loc[0] + move[0],loc[1] + move[1])
        return self.valid_loc(potential_move)
    
    def valid_loc(self,loc: Tuple[int,int]):
        if loc[0] < 0 or loc[0] >= self.n:
            return False
        if loc[1] < 0 or loc[1] >= self.m:
            return False
        return True
    
    def get_cell(self,loc: Tuple[int,int]):
        if self.valid_loc(loc):
            result = self.map[loc[0]][loc[1]]
            logging.info("got {} with value {}".format(loc,result))
        else:
            logging.warn("invalid location {}".format(loc))
        return result

    def move_cell()
    
    def set_cell(self,loc: Tuple[int,int],value: str):
        if self.valid_loc(loc):
            self.map[loc[0]][loc[1]] = value
            logging.info("set {} with value {}".format(loc,value))
        else:
            logging.warn("invalid location {}".format(loc))

class Explorer:
    @staticmethod
    def find_shortest_path(board,start,end):
        return "todo"
    

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    dungeon_master = Dungeon_Master(14,8)
    print(dungeon_master.dungeon)



    