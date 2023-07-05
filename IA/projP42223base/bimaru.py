# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo tp009:
# 102536 Diogo Miranda
# 103458 David Pires

import sys
import copy
import numpy as np

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)



class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


    def update_boats(self, size):
        return self.board.update_boats(size)


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    boats_1 = 4
    boats_2 = 3
    boats_3 = 2
    boats_4 = 1
    
    def __init__(self) -> None:
            self.board = np.full((10, 10), ".")
            self.cleared_rows = 0
            self.cleared_cols = 0
    
    def update_boats(self, size):
        if size == 1:
            self.boats_1 -= 1
        elif size == 2:
            self.boats_2 -= 1
        elif size == 3:
            self.boats_3 -= 1
        elif size == 4:
            self.boats_4 -= 1
        
        return
    
    def check_hints(self):
        for i in range(0, cluesNumber):
            if self.board[int(clues[i][0])][int(clues[i][1])] != clues[i][2].lower():
                return False
            self.board[int(clues[i][0])][int(clues[i][1])] = clues[i][2]
        return True
    
    def check_for_empty(self):
        for i in range(1,11):
            if self.rowValues[i] == "0" and not (self.cleared_rows & (1 << (i-1))):
                self.cleared_rows |= (1 << (i-1))
                for j in range(0,10):
                    if self.board[i-1][j] == ".":
                        self.board[i-1][j] = "w"
            if self.colValues[i] == "0" and not (self.cleared_cols & (1 << (i-1))):
                self.cleared_cols |= (1 << (i-1))
                for j in range(0,10):
                    if self.board[j][i-1] == ".":
                        self.board[j][i-1] = "w"
        return
    
    def fill_1(self, first, last):
        
        self.board[first[0]][first[1]] = "t"
        self.rowValues[first[0]+1] = str(int(self.rowValues[first[0]+1]) - 1)
        
        if first[0] != 0:
            self.board[first[0]-1][first[1]] = "w"
        if first[1] != 0:
            self.board[first[0]][first[1]-1] = "w"
        if first[1] != 9:
            self.board[first[0]][first[1]+1] = "w"
        
        first[0] += 1
        
        while first[0] != last[0]:
            self.board[first[0]][first[1]] = "m"
            self.rowValues[first[0]+1] = str(int(self.rowValues[first[0]+1]) - 1)
            
            if first[1] != 0:
                self.board[first[0]][first[1]-1] = "w"
            if first[1] != 9:
                self.board[first[0]][first[1]+1] = "w"

            first[0] += 1
            
        if first[0] != 9:
            self.board[first[0]+1][first[1]] = "w"
        
        self.board[first[0]][first[1]] = "b"
        self.rowValues[first[0]+1] = str(int(self.rowValues[first[0]+1]) - 1)
    
    def fill_2(self, first, last):
        
        self.board[first[0]][first[1]] = "l"
        self.colValues[first[1]+1] = str(int(self.colValues[first[1]+1]) - 1)
        
        if first[0] != 0:
            self.board[first[0]-1][first[1]] = "w"
        if first[0] != 9:
            self.board[first[0]+1][first[1]] = "w"
        if first[1] != 0:
            self.board[first[0]][first[1]-1] = "w"
        
        first[1] += 1
        
        while first[1] != last[1]:
            self.board[first[0]][first[1]] = "m"
            self.colValues[first[1]+1] = str(int(self.colValues[first[1]+1]) - 1)
            
            if first[0] != 0:
                self.board[first[0]-1][first[1]] = "w"
            if first[0] != 9:
                self.board[first[0]+1][first[1]] = "w" 
            
            first[1] += 1
        
        if first[1] != 9:
            self.board[first[0]][first[1]+1] = "w"
        
        
        self.board[first[0]][first[1]] = "r"
        self.colValues[first[1]+1] = str(int(self.colValues[first[1]+1]) - 1)
    
    def fill(self, first, direction, last, size, hint = False):
        if size == 1:
            if hint == True:
                self.boats_1 -= 1
            self.board[first[0]][first[1]] = "c"
            self.rowValues[first[0]+1] = str(int(self.rowValues[first[0]+1]) - 1)
            self.colValues[first[1]+1] = str(int(self.colValues[first[1]+1]) - 1)
            if first[0] != 0:
                self.board[first[0]-1][first[1]] = "w"
            if first[0] != 9:
                self.board[first[0]+1][first[1]] = "w"
            if first[1] != 0:
                self.board[first[0]][first[1]-1] = "w"
            if first[1] != 9:
                self.board[first[0]][first[1]+1] = "w"
            if first[0] != 0 and first[1] != 0:
                self.board[first[0]-1][first[1]-1] = "w"
            if first[0] != 0 and first[1] != 9:
                self.board[first[0]-1][first[1]+1] = "w"
            if first[0] != 9 and first[1] != 0:
                self.board[first[0]+1][first[1]-1] = "w"
            if first[0] != 9 and first[1] != 9:
                self.board[first[0]+1][first[1]+1] = "w"
            return
        
        if direction == 1:
            self.fill_1(first, last)
            self.colValues[first[1]+1] = str(int(self.colValues[first[1]+1]) - size)
        elif direction == 2:
            self.fill_2(first, last)
            self.rowValues[first[0]+1] = str(int(self.rowValues[first[0]+1]) - size)
        return

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        try:
            """Avoid default "wrapping around" behavior"""
            if row < 0 or col < 0:
                raise IndexError
            return self.board[row][col]
        except IndexError:
            return None
        
    def adjacent_vertical_values(self, first, last) -> int:
        """Devolve os valores imediatamente acima e abaixo, respectivamente."""
        if first[0] == last[0]:
            return (
                self.get_value(first[0] + 1, first[1]) in (".", "w", None)
                and self.get_value(first[0] - 1, first[1]) in (".", "w", None)
                and self.get_value(first[0], first[1] + 1) in (".", "w", None)
                and self.get_value(first[0], first[1] - 1) in (".", "w", None)
                and self.get_value(first[0] + 1, first[1] + 1) in (".", "w", None)
                and self.get_value(first[0] + 1, first[1] - 1) in (".", "w", None)
                and self.get_value(first[0] - 1, first[1] + 1) in (".", "w", None)
                and self.get_value(first[0] - 1, first[1] - 1) in (".", "w", None)
            )

        cell = [first[0], first[1]]
        
        while cell[0] != last[0]:
            if (
                (self.get_value(cell[0] + 1, cell[1]) not in (".", "w", None))
                or (self.get_value(cell[0] - 1, cell[1]) not in (".", "w", None))
                or (self.get_value(cell[0], cell[1] + 1) not in (".", "w", None))
                or (self.get_value(cell[0], cell[1] - 1) not in (".", "w", None))
                or (self.get_value(cell[0] + 1, first[1] + 1) not in (".", "w", None))
                or (self.get_value(cell[0] + 1, first[1] - 1) not in (".", "w", None))
                or (self.get_value(cell[0] - 1, first[1] + 1) not in (".", "w", None))
                or (self.get_value(cell[0] - 1, first[1] - 1) not in (".", "w", None))
            ):
                return False
            
            cell[0] += 1
        
        if (
                (self.get_value(last[0] + 1, last[1]) not in (".", "w", None))
                or (self.get_value(last[0] - 1, last[1]) not in (".", "w", None))
                or (self.get_value(last[0], last[1] + 1) not in (".", "w", None))
                or (self.get_value(last[0], last[1] - 1) not in (".", "w", None))
                or (self.get_value(last[0] + 1, last[1] + 1) not in (".", "w", None))
                or (self.get_value(last[0] + 1, last[1] - 1) not in (".", "w", None))
                or (self.get_value(last[0] - 1, last[1] + 1) not in (".", "w", None))
                or (self.get_value(last[0] - 1, last[1] - 1) not in (".", "w", None))
            ):
            return False
        
        return True
        
    def adjacent_horizontal_values(self, first, last) -> int:
        """Returns the immediately left and right values, respectively."""
        # Check all the adjacent values of all the cells of a horizontal grid
        if first[1] == last[1]:
            return (
                (self.get_value(first[0] + 1, first[1]) in (".", "w", None))
                and (self.get_value(first[0] - 1, first[1]) in (".", "w", None))
                and (self.get_value(first[0], first[1] + 1) in (".", "w", None))
                and (self.get_value(first[0], first[1] - 1) in (".", "w", None))
                and (self.get_value(first[0] + 1, first[1] + 1) in (".", "w", None))
                and (self.get_value(first[0] + 1, first[1] - 1) in (".", "w", None))
                and (self.get_value(first[0] - 1, first[1] + 1) in (".", "w", None))
                and (self.get_value(first[0] - 1, first[1] - 1) in (".", "w", None))
            )

        cell = [first[0], first[1]]

        while cell[1] != last[1]:
            if (
                (self.get_value(cell[0] + 1, cell[1]) not in (".", "w", None))
                or (self.get_value(cell[0] - 1, cell[1]) not in (".", "w", None))
                or (self.get_value(cell[0], cell[1] + 1) not in (".", "w", None))
                or (self.get_value(cell[0], cell[1] - 1) not in (".", "w", None))
                or (self.get_value(cell[0] + 1, first[1] + 1) not in (".", "w", None))
                or (self.get_value(cell[0] + 1, first[1] - 1) not in (".", "w", None))
                or (self.get_value(cell[0] - 1, first[1] + 1) not in (".", "w", None))
                or (self.get_value(cell[0] - 1, first[1] - 1) not in (".", "w", None))
            ):
                return False
            
            cell[1] += 1

        if (
                (self.get_value(last[0] + 1, last[1]) not in (".", "w", None))
                or (self.get_value(last[0] - 1, last[1]) not in (".", "w", None))
                or (self.get_value(last[0], last[1] + 1) not in (".", "w", None))
                or (self.get_value(last[0], last[1] - 1) not in (".", "w", None))
                or (self.get_value(last[0] + 1, last[1] + 1) not in (".", "w", None))
                or (self.get_value(last[0] + 1, last[1] - 1) not in (".", "w", None))
                or (self.get_value(last[0] - 1, last[1] + 1) not in (".", "w", None))
                or (self.get_value(last[0] - 1, last[1] - 1) not in (".", "w", None))
            ):
            return False

        return True
    
    def print_board(self):
        """Imprime o tabuleiro."""
        for row in self.board:
            print(''.join(str(cell) if cell != 0 else '.' for cell in row))
        
        return 
    
    def all_water(self, first):
        return self.get_value(first[0]+1,first[1]) in {"w",None} and self.get_value(first[0]-1,first[1]) in {"w",None} and self.get_value(first[0],first[1]+1) in {"w",None} and self.get_value(first[0],first[1]-1) in {"w",None} and self.get_value(first[0]+1,first[1]+1) in {"w",None} and self.get_value(first[0]+1,first[1]-1) in {"w",None} and self.get_value(first[0]-1,first[1]+1) in {"w",None} and self.get_value(first[0]-1,first[1]-1) in {"w",None}



    def resolve_hints(self, first = True):

        for i in range(1,5):
            hit = False
            if i == 1:
                for a in range(len(cluesT)-1,-1,-1):
                    if (not first and int(self.colValues[cluesT[a][1] + 1]) == 2 and self.get_value(cluesT[a][0] + 1, cluesT[a][1])  == ".") or (self.get_value(cluesT[a][0] + 2, cluesT[a][1]) in ("w", None) and self.get_value(cluesT[a][0] + 1, cluesT[a][1]) == "."):
                        self.boats_2 -= 1
                        self.fill([cluesT[a][0], cluesT[a][1]], 1, [cluesT[a][0] + 1, cluesT[a][1]], 2)
                    elif first:
                        for b in range(len(cluesB)-1,-1,-1):
                            if cluesT[a][1] == cluesB[b][1] and cluesB[b][0] - cluesT[a][0] <= 3:
                                self.fill([cluesT[a][0], cluesT[a][1]], 1, [cluesB[b][0], cluesB[b][1]], cluesB[b][0] - cluesT[a][0] + 1)
                                if cluesB[b][0] - cluesT[a][0] == 1:
                                    self.boats_2 -= 1
                                elif cluesB[b][0] - cluesT[a][0] == 2:
                                    self.boats_3 -= 1
                                elif cluesB[b][0] - cluesT[a][0] == 3:
                                    self.boats_4 -= 1
                                hit = True
                                break
                        if hit:
                            break  
                        for c in range(len(cluesM)-1,-1,-1):
                            if cluesT[a][1] == cluesM[c][1] and cluesT[a][0] + 2 == cluesM[c][0]:
                                self.fill([cluesT[a][0], cluesT[a][1]], 1, [cluesM[c][0] + 1, cluesM[c][1]], 4)
                                self.boats_4 -= 1
                                break
            if i == 2:
                for a in range(len(cluesB)-1,-1,-1):
                    if (not first and int(self.colValues[cluesB[a][1] + 1]) == 2 and self.get_value(cluesB[a][0] - 1, cluesB[a][1]) == ".") or (self.get_value(cluesB[a][0] - 2, cluesB[a][1]) in ("w", None) and self.get_value(cluesB[a][0] - 1, cluesB[a][1]) == "."):
                        self.boats_2 -= 1
                        self.fill([cluesB[a][0]-1, cluesB[a][1]], 1, [cluesB[a][0], cluesB[a][1]], 2)
                    elif first:
                        for e in range(len(cluesM)-1,-1,-1):
                            if cluesB[a][1] == cluesM[e][1] and cluesB[a][0] - 2 == cluesM[e][0]:
                                self.fill([cluesM[e][0] - 1, cluesM[e][1]], 1, [cluesB[a][0], cluesB[a][1]], 4)
                                self.boats_4 -= 1
                                break
            if i == 3:
                for a in range(len(cluesL)-1,-1,-1):
                    if (not first and int(self.rowValues[cluesL[a][0] + 1]) == 2 and self.get_value(cluesL[a][0], cluesL[a][1] + 1) == ".") or (self.get_value(cluesL[a][0], cluesL[a][1] + 2) in ("w", None) and self.get_value(cluesL[a][0], cluesL[a][1] + 1) == "."):
                        self.boats_2 -= 1
                        self.fill([cluesL[a][0], cluesL[a][1]], 2, [cluesL[a][0], cluesL[a][1] + 1], 2)
                    elif first:
                        for f in range(len(cluesR)-1,-1,-1):
                            if cluesL[a][0] == cluesR[f][0] and cluesR[f][1] - cluesL[a][1] <= 3:
                                self.fill([cluesL[a][0], cluesL[a][1]], 2, [cluesR[f][0], cluesR[f][1]], cluesR[f][1] - cluesL[a][1] + 1)
                                if cluesR[f][1] - cluesL[a][1] == 1:
                                    self.boats_2 -= 1
                                elif cluesR[f][1] - cluesL[a][1] == 2:
                                    self.boats_3 -= 1
                                elif cluesR[f][1] - cluesL[a][1] == 3:
                                    self.boats_4 -= 1
                                hit = True
                                break
                            
                        if hit:
                            break
                        for g in range(len(cluesM)):
                            if cluesL[a][0] == cluesM[g][0] and cluesL[a][1] + 2 == cluesM[g][1]:
                                self.fill([cluesL[a][0], cluesL[a][1]], 2, [cluesM[g][0], cluesM[g][1] + 1], 4)
                                self.boats_4 -= 1
                                break
            if i == 4:
                for a in range(len(cluesR)-1,-1,-1):
                    if (not first and int(self.rowValues[cluesR[a][0] + 1]) == 2 and self.get_value(cluesR[a][0], cluesR[a][1] - 1) == ".") or (self.get_value(cluesR[a][0], cluesR[a][1] - 2) in ("w", None) and self.get_value(cluesR[a][0], cluesR[a][1] - 1) == "."):
                        self.boats_2 -= 1
                        self.fill([cluesR[a][0], cluesR[a][1] - 1], 2, [cluesR[a][0], cluesR[a][1]], 2)
                    elif first:
                        for j in range(len(cluesM)-1,-1,-1):
                            if cluesR[a][0] == cluesM[j][0] and cluesR[a][1] - 2 == cluesM[j][1]:
                                self.fill([cluesM[j][0], cluesM[j][1] - 1], 2, [cluesR[a][0], cluesR[a][1]], 4)
                                self.boats_4 -= 1
                                break
        self.check_for_empty()
        return
    
    def put_water_L(self, row, col):
        if self.get_value(row-1,col-1) != None: self.board[row-1][col-1] = "w"
        if self.get_value(row-1,col) != None:   self.board[row-1][col] = "w"
        if self.get_value(row-1,col+1) != None: self.board[row-1][col+1] = "w"
        if self.get_value(row-1,col+2) != None: self.board[row-1][col+2] = "w"
        if self.get_value(row,col-1) != None:   self.board[row][col-1] = "w"
        if self.get_value(row+1,col-1) != None: self.board[row+1][col-1] = "w"
        if self.get_value(row+1,col) != None:   self.board[row+1][col] = "w"
        if self.get_value(row+1,col+1) != None: self.board[row+1][col+1] = "w"
        if self.get_value(row+1,col+2) != None: self.board[row+1][col+1] = "w"
        return

    def put_water_R(self, row, col):
        if self.get_value(row-1,col-2) != None: self.board[row-1][col-2] = "w"
        if self.get_value(row-1,col-1) != None: self.board[row-1][col-1] = "w"
        if self.get_value(row-1,col) != None:   self.board[row-1][col] = "w"
        if self.get_value(row-1,col+1) != None: self.board[row-1][col+1] = "w"
        if self.get_value(row,col+1) != None:   self.board[row][col+1] = "w"
        if self.get_value(row+1,col-2) != None: self.board[row+1][col-2] = "w"
        if self.get_value(row+1,col-1) != None: self.board[row+1][col-1] = "w"
        if self.get_value(row+1,col) != None:   self.board[row+1][col] = "w"
        if self.get_value(row+1,col+1) != None: self.board[row+1][col+1] = "w"
        return

    def put_water_T(self, row, col):
        if self.get_value(row-1,col-1) != None: self.board[row-1][col-1] = "w"
        if self.get_value(row-1,col) != None:   self.board[row-1][col] = "w"
        if self.get_value(row-1,col+1) != None: self.board[row-1][col+1] = "w"
        if self.get_value(row,col-1) != None:   self.board[row][col-1] = "w"
        if self.get_value(row,col+1) != None:   self.board[row][col+1] = "w"
        if self.get_value(row+1,col-1) != None: self.board[row+1][col-1] = "w"
        if self.get_value(row+1,col+1) != None: self.board[row+1][col+1] = "w"
        if self.get_value(row+2,col-1) != None: self.board[row+1][col-1] = "w"
        if self.get_value(row+2,col+1) != None: self.board[row+1][col+1] = "w"   
        return

    def put_water_B(self, row, col):
        if self.get_value(row-2,col-1) != None: self.board[row-1][col-1] = "w"
        if self.get_value(row-2,col+1) != None: self.board[row-1][col+1] = "w"
        if self.get_value(row-1,col-1) != None: self.board[row-1][col-1] = "w"
        if self.get_value(row-1,col+1) != None: self.board[row-1][col+1] = "w"
        if self.get_value(row,col-1) != None:   self.board[row][col-1] = "w"
        if self.get_value(row,col+1) != None:   self.board[row][col+1] = "w"
        if self.get_value(row+1,col-1) != None: self.board[row+1][col-1] = "w"
        if self.get_value(row+1,col) != None:   self.board[row+1][col] = "w"
        if self.get_value(row+1,col+1) != None: self.board[row+1][col+1] = "w"
        return

    def put_water_M(self, row, col):
        if self.get_value(row+1,col+1) != None: self.board[row+1][col+1] = "w"
        if self.get_value(row-1,col-1) != None: self.board[row-1][col-1] = "w"
        if self.get_value(row+1,col-1) != None: self.board[row+1][col-1] = "w"
        if self.get_value(row-1,col+1) != None: self.board[row-1][col+1] = "w"
        return


    @staticmethod
    def parse_instance(self):
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
            
        PS: Foi-se colocado o argumento self de forma a guardar como atributos mais facilmente o input
        
        """
        global cluesNumber
        global clues
        global cluesL
        global cluesR
        global cluesT
        global cluesB
        global cluesM

        cluesNumber = 0
        clues = []
        cluesL = []
        cluesR = []
        cluesT = []
        cluesB = []
        cluesM = []
        self.rowValues = sys.stdin.readline().split()
        self.colValues = sys.stdin.readline().split()
        cluesNumber = int(sys.stdin.readline())
        
        for i in range(0,cluesNumber):
            clues.append(sys.stdin.readline().split()[1:])
            if clues[i][2] == 'C':
                self.fill([int(clues[i][0]), int(clues[i][1])], 1, [int(clues[i][0]), int(clues[i][1])], 1, True)
            elif clues[i][2] == 'L':
                cluesL.append([int(clues[i][0]), int(clues[i][1])])
                self.put_water_L(int(clues[i][0]), int(clues[i][1]))
            elif clues[i][2] == 'R':
                cluesR.append([int(clues[i][0]), int(clues[i][1])])
                self.put_water_R(int(clues[i][0]), int(clues[i][1]))
            elif clues[i][2] == 'T':
                cluesT.append([int(clues[i][0]), int(clues[i][1])])
                self.put_water_T(int(clues[i][0]), int(clues[i][1]))
            elif clues[i][2] == 'B':
                cluesB.append([int(clues[i][0]), int(clues[i][1])])
                self.put_water_B(int(clues[i][0]), int(clues[i][1]))
            elif clues[i][2] == 'M':
                cluesM.append([int(clues[i][0]), int(clues[i][1])])
                self.put_water_M(int(clues[i][0]), int(clues[i][1]))
            elif clues[i][2] == "W":
                self.board[int(clues[i][0])][int(clues[i][1])] = "w"
        
        self.check_for_empty()
        self.resolve_hints()
        self.resolve_hints(False)

        return 


class Bimaru(Problem):
    
    def __init__(self, state: BimaruState):
        """O construtor especifica o estado inicial."""
        self.initial = state
        super().__init__(self.initial) #while no other members are needed
        return
    
    def copy_board(self, board):
        return copy.deepcopy(board)
    
    def check_all_values_row(self, first, last, state) -> bool:
        for i in range(first[1], last[1] + 1):
            if state.board.board[first[0]][i] != ".":
                return False
        return True

    def check_all_values_col(self, first, last, state) -> bool:
        for i in range(first[0], last[0] + 1):
            if state.board.board[i][first[1]] != ".":
                return False
        return True

    def available_grids(self, state, size) -> np.array:

        result = []
        board = state.board
        
        # avoid putting water on hints
        for clue in clues:
            if ( (board.get_value(int(clue[0]), int(clue[1])) == "w") and (clue[2] != "W") ):   
                return np.array([])
            
        # avoid putting water near M hints
        for clue in cluesM:
            if ( ( board.get_value(clue[0]-1, clue[1]) == "w" or board.get_value(clue[0]+1, clue[1]) == "w" ) and
                 ( board.get_value(clue[0], clue[1]-1) == "w" or board.get_value(clue[0], clue[1]+1) == "w" )
                ):
                return np.array([])
            
        # avoid putting water near L hints
        for clue in cluesL:
            if ( board.get_value(clue[0], clue[1]+1) == "w" ) :
                return np.array([])    
            
        # avoid putting water near R hints
        for clue in cluesR:
            if ( board.get_value(clue[0], clue[1]-1) == "w" ) :
                return np.array([])
            
        # avoid putting water near T hints
        for clue in cluesT:
            if ( board.get_value(clue[0]+1, clue[1]) == "w" ) :
                return np.array([])
            
        # avoid putting water near B hints
        for clue in cluesB:
            if ( board.get_value(clue[0]-1, clue[1]) == "w" ) :
                return np.array([])

        checked_rows = set()
        checked_cols = set()
        max_range = 10 - size + 1

        for i in range(1, 11):

            rowVal = int(board.rowValues[i])
            if rowVal >= size:

                count = np.count_nonzero(board.board[i-1] == ".")
                if count < rowVal: return np.array([])

                for j in range(max_range):
                    if (
                    (size > 1 and self.check_all_values_row([i-1,j],[i-1,j + size - 1], state))
                        or (size == 1 and board.board[i-1][j] == ".")
                    ) and board.adjacent_horizontal_values(
                        np.array([i-1, j]), np.array([i-1, j + size - 1])
                    ):
                        if size != 1:
                            result.append([np.array([i - 1, j]), np.array([i - 1, j + size - 1])])
                        elif j not in checked_cols:
                            checked_rows.add(i-1)
                            result.append([np.array([i - 1, j]), np.array([i - 1, j + size - 1])])
                            

            colVal = int(board.colValues[i])
            if colVal >= size:

                count = np.count_nonzero(board.board[:, i-1] == ".")
                if count < colVal: return np.array([])

                for j in range(max_range):
                    if (
                    (size > 1 and self.check_all_values_col([j,i-1],[j + size - 1,i-1], state))
                        or (size == 1 and board.board[j, i-1] == ".")
                    ) and board.adjacent_vertical_values(
                        np.array([j, i-1]), np.array([j + size - 1, i-1])
                    ):
                        if size != 1:
                            result.append([np.array([j, i - 1]), np.array([j + size - 1, i - 1])])
                        elif j not in checked_rows:
                            checked_cols.add(i-1)
                            result.append([np.array([j, i - 1]), np.array([j + size - 1, i - 1])])

        return np.array(result)

    def valid_size(self, state, size):
        if size == 1:
            return state.board.boats_1 > 0
        elif size == 2:
            return state.board.boats_2 > 0
        elif size == 3:
            return state.board.boats_3 > 0
        elif size == 4:
            return state.board.boats_4 > 0


    def actions(self, state: BimaruState): #[]
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        result = []
        if state.board.boats_1 == 0 and state.board.boats_2 == 0 and state.board.boats_3 == 0 and state.board.boats_4 == 0:
            return result
        # given that an action is [size, [first, last]] creates a list of actions with all the sizes and all the grids
        for i in reversed(range(1,5)):
            if self.valid_size(state ,i):
                grids = self.available_grids(state, i)
                reversed_grids = grids[::-1]
                for j in range(0, len(reversed_grids)):
                    result.append([i, reversed_grids[j]])
                break

        return result
    
    def check_direction(self, first, last) -> int:
        if first[0] == last[0]:
            return 2
        elif first[1] == last[1]:
            return 1

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_state = BimaruState(self.copy_board(state.board))
        direction = self.check_direction(action[1][0], action[1][1])
        new_state.board.fill(action[1][0], direction, action[1][1], action[0])
        new_state.update_boats(action[0])
        new_state.board.resolve_hints(False)
    
        return new_state
    

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if state.board.boats_1 == 0 and state.board.boats_2 == 0 and state.board.boats_3 == 0 and state.board.boats_4 == 0 and state.board.cleared_rows == (2**10 -1) and state.board.cleared_cols == (2 ** 10 - 1) and state.board.check_hints() == True:
            return True
        return False
    
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass


def clear_board(board : Board):
    #replace every "w" with "."
    for i in range(0,10):
        for j in range(0,10):
            if board.board[i][j] == "w":
                board.board[i][j] = "."
    return

if __name__ == "__main__":

    board = Board()
    board.parse_instance(board)
    bimaru = BimaruState(board)
    problem = Bimaru(bimaru)
    solution_node = depth_first_tree_search(problem)
    clear_board(solution_node.state.board)
    solution_node.state.board.print_board()