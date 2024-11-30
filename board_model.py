import copy
from enums import *

class Board_Model:
    def __init__(self, board_state = None, jump_required = Movements.NOJUMP):
        if board_state is None:
            self.board_state = [[-1,'x',-1,'x',-1,'x',-1,'x'],
                                ['x',-1,'x',-1,'x',-1,'x',-1],
                                [-1,'x',-1,'x',-1,'x',-1,'x'],
                                ['x',0,'x',0,'x',0,'x',0],
                                [0,'x',0,'x',0,'x',0,'x'],
                                ['x',1,'x',1,'x',1,'x',1],
                                [1,'x',1,'x',1,'x',1,'x'],
                                ['x',1,'x',1,'x',1,'x',1]]
        else:
            self.board_state = copy.deepcopy(board_state)

        self.jump_required = jump_required
        self.board_strength = self.calculate_board_strength()

    def calculate_board_strength(self):
        tot = 0
        for rank in self.board_state:
            for phile in rank:
                if (type(phile)) == int:
                    tot += phile
        return tot

    def validate_moves(self, potential_moves, x, y):
        piece = self.board_state[y][x]
        up = piece > 0
        king = abs(piece) == 3
        ret_list = []
        for pot_y, pot_x, jump in potential_moves:
            if pot_x >= 0 and pot_x <= 7 and pot_y >= 0 and pot_y <= 7:
                target_loc = self.board_state[pot_y][pot_x]
                if (pot_y < y and up) or king or (pot_y > y and not up):
                    if jump == Movements.JUMP:
                        test_piece = self.board_state[(pot_y + y)//2][(pot_x + x)//2]
                        if test_piece not in ('x', 0):
                            if test_piece * piece < 0 and target_loc == 0:
                                ret_list.append((pot_y, pot_x))
                    elif target_loc == 0:
                        ret_list.append((pot_y, pot_x))
        return ret_list

    def adjust_board(self, x, y, tar_x, tar_y):
        ret_val = Board_Model(self.board_state)
        ret_val.board_state[tar_x][tar_y], ret_val.board_state[x][y] = ret_val.board_state[x][y], 0
        return ret_val
    
    def create_move_lists(self, player = [-3,-1]):
        ret_val = []
        for x in range(len(self.board_state)):
            for y in range(len(self.board_state[x])):
                if self.board_state[x][y] in player:
                    potential_moves = []
                    potential_moves.append((x-1, y-1, Movements.NOJUMP)) #A
                    potential_moves.append((x-1, y+1, Movements.NOJUMP)) #B
                    potential_moves.append((x+1, y-1, Movements.NOJUMP)) #C
                    potential_moves.append((x+1, y+1, Movements.NOJUMP)) #D
                    potential_moves.append((x-2, y-2, Movements.JUMP)) #E
                    potential_moves.append((x-2, y+2, Movements.JUMP)) #F
                    potential_moves.append((x+2, y-2, Movements.JUMP)) #G
                    potential_moves.append((x+2, y+2, Movements.JUMP)) #H

                    valid_moves = self.validate_moves(potential_moves, x, y)
                    for tar_x, tar_y in valid_moves:
                        print(tar_x, tar_y)
                        bm = self.adjust_board(x, y, tar_x, tar_y)
                        ret_val.append(bm.board_state)
        return ret_val

def main():
    bm = Board_Model([[0,'x',0,'x',0,'x',0,'x'],
                      ['x',0,'x',0,'x',1,'x',0],
                      [0,'x',0,'x',0,'x',0,'x'],
                      ['x',0,'x',0,'x',0,'x',0],
                      [0,'x',0,'x',0,'x',0,'x'],
                      ['x',0,'x',0,'x',0,'x',0],
                      [0,'x',0,'x',0,'x',0,'x'],
                      ['x',0,'x',-3,'x',0,'x',0]])
    cml = bm.create_move_lists()
    for item in cml:
        print('A:', item)

if __name__ == '__main__':
    main()
