import copy
import random


class Node:
    def __init__(self, player, step=None, board=None):
        self.value = float("-inf")
        self.step = step
        self.player = player
        if step is not None:
            board.set_position(self.step[0], self.step[1], player)
        self.board = board

    def set_value(self, val):
        self.value = val

    def get_board(self):
        return self.board

    def set_step(self, step):
        self.step = step

    def get_player(self):
        return self.player


class Bot:
    def __init__(self):
        self.step = [0, 0]

    def collect_possible_moves(self, board, is_player_o):
        possible_moves = []
        # consider open 4 'O'
        if self.movement(board, 'O' if is_player_o else 'X', 4):
            possible_moves.append(self.step)
            return possible_moves
        # consider open 4 'X'
        if self.movement(board, 'X' if is_player_o else 'O', 4):
            possible_moves.append(self.step)
            return possible_moves
        # consider open 3
        possible_moves.extend(self.look_for_3_emp_emp(board, 'O' if is_player_o else 'X'))
        # consider open 3
        if len(possible_moves) == 0:
            possible_moves.extend(self.look_for_3_emp_emp(board, 'X' if is_player_o else 'O'))
        # consider every other possible moves
        if len(possible_moves) == 0:
            i = 3
            while i > 0:
                possible_moves.extend(self.collect_moves(board, 'O' if is_player_o else 'X', i))
                i -= 1
            possible_moves.extend(self.collect_moves(board, 'X' if is_player_o else 'O', 1))
        possible_moves = list(filter(lambda item: item is not None, possible_moves))
        possible_moves = self.drop_duplicates(possible_moves)
        return possible_moves

    def smart_move(self, board):
        if self.movement(board, 'O', 4):
            pass
        elif self.movement(board, 'X', 4):
            pass
        else:
            head = Node('0', board=board)
            head.set_value(self.minimax(head, 0, True, float('-inf'), float('+inf')))
            # self.step already set
        board.set_position(self.step[0], self.step[1], "O")
        return

    def heuristic(self, node):
        node_value = 0
        # collect points for open 4 rows
        node_value += len(list(filter(lambda item: item is not None, self.collect_moves(node.get_board(), 'O', 4)))) * 16
        node_value -= len(list(filter(lambda item: item is not None, self.collect_moves(node.get_board(), 'X', 4)))) * 16
        # collect points for all 4
        node_value += len(self.collect_moves(node.get_board(), 'O', 4)) * 8
        node_value -= len(self.collect_moves(node.get_board(), 'X' , 4)) * 8
        # collect points for 3 emp-emp
        node_value += len(self.look_for_3_emp_emp(node.get_board(), 'O')) * 4
        node_value -= len(self.look_for_3_emp_emp(node.get_board(), 'X')) * 4
        node_value += len(list(filter(lambda item: item is not None, self.collect_moves(node.get_board(), 'O', 2)))) * 2
        return node_value

    def minimax(self, node, depth, is_maximizing_player, alpha, beta):
        # if someone won return a corresponding inf value else return heuristic if depth reached
        if node.get_board().check_for_winner(node.get_player()):
            if node.get_player() == 'O':
                return float('+inf')
            else:
                return float('-inf')
        elif depth == 7:
            return self.heuristic(node)

        if is_maximizing_player:
            best_val = float('-inf')
            all_possible_moves = copy.deepcopy(self.collect_possible_moves(node.get_board(), True))
            for one_move in all_possible_moves:
                new_node = Node('O', one_move, board=copy.deepcopy(node.get_board()))
                value = self.minimax(new_node, depth + 1, False, alpha, beta)
                best_val = max(best_val, value)
                if value >= best_val and depth == 0:
                    self.step = one_move
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            return best_val

        else:
            best_val = float('+inf')
            all_possible_moves = copy.deepcopy(self.collect_possible_moves(node.get_board(), False))
            for one_move in all_possible_moves:
                new_node = Node('X', one_move, board=copy.deepcopy(node.get_board()))
                value = self.minimax(new_node, depth + 1, True, alpha, beta)
                best_val = min(best_val, value)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            return best_val

    def move(self, board):
        if self.movement(board, 'X', 4):
            board.set_position(self.step[0], self.step[1], "O")
            return
        else:
            possible_moves = self.look_for_3_emp_emp(board, 'X')
            if len(possible_moves) > 0:
                board.set_position(possible_moves[0][0], possible_moves[0][1], "O")
                return

        i = 4
        while i > 0:
            if self.movement(board, 'O', i):
                board.set_position(self.step[0], self.step[1], "O")
                return
            i -= 1

        self.movement(board, 'X', 1)
        board.set_position(self.step[0], self.step[1], "O")
        return

    def look_for_3_emp_emp(self, board, look_for):
        possible_moves = []
        for x in range(board.get_size()):
            for y in range(board.get_size()):
                if board.get_cell(x, y) == look_for:
                    # look for 3 right where both sides are empty
                    if board.get_cell(x, y - 1) == ' ' and board.get_cell(x, y + 1) == look_for and board.get_cell(
                            x, y + 2) == look_for and board.get_cell(x, y + 3) == ' ':
                        if self.movement_valid(x, y - 1, board):
                            possible_moves.append([x, y - 1])
                        elif self.movement_valid(x, y + 3, board):
                            possible_moves.append([x, y + 3])

                    # look for 3 left down where both sides are empty
                    if board.get_cell(x - 1, y + 1) == ' ' and board.get_cell(x + 1,
                                                                              y - 1) == look_for and board.get_cell(
                        x + 2, y - 2) == look_for and board.get_cell(x + 3, y - 3) == ' ':
                        if self.movement_valid(x - 1, y + 1, board):
                            possible_moves.append([x - 1, y + 1])
                        elif self.movement_valid(x + 3, y - 3, board):
                            possible_moves.append([x + 3, y - 3])

                    # look for 3 right down where both sides are empty
                    if board.get_cell(x - 1, y - 1) == ' ' and board.get_cell(x + 1,
                                                                              y + 1) == look_for and board.get_cell(
                        x + 2, y + 2) == look_for and board.get_cell(x + 3, y + 3) == ' ':
                        if self.movement_valid(x - 1, y - 1, board):
                            possible_moves.append([x - 1, y - 1])
                        elif self.movement_valid(x + 3, y + 3, board):
                            possible_moves.append([x + 3, y + 3])

                    # look for 3 down where both sides are empty
                    if board.get_cell(x - 1, y) == ' ' and board.get_cell(x + 1, y) == look_for and board.get_cell(
                            x + 2, y) == look_for and board.get_cell(x + 3, y) == ' ':
                        if self.movement_valid(x - 1, y, board):
                            possible_moves.append([x - 1, y])
                        elif self.movement_valid(x + 3, y, board):
                            possible_moves.append([x + 3, y])
        return possible_moves

    def movement(self, board, look_for, how_many):
        for x in range(board.get_size()):
            for y in range(board.get_size()):
                if board.get_cell(x, y) == look_for:
                    # count x right straight
                    if self.char_counter(board, x, y, look_for, how_many, 0, 1):
                        return True
                    # count x left down
                    if self.char_counter(board, x, y, look_for, how_many, 1, -1):
                        return True
                    # count x right down
                    if self.char_counter(board, x, y, look_for, how_many, 1, 1):
                        return True
                    # count x down
                    if self.char_counter(board, x, y, look_for, how_many, 1, 0):
                        return True

        return False

    def char_counter(self, board, x, y, look_for, how_many, x_inc, y_inc):
        prev_x = x - x_inc
        prev_y = y - y_inc

        counter = 1
        x += x_inc
        y += y_inc
        while counter != how_many:
            if 0 < x < board.get_size() and 0 < y < board.get_size() and board.get_cell(x, y) == look_for:
                counter += 1
                x += x_inc
                y += y_inc
            else:
                break
        if self.movement_valid(x, y, board) and counter == how_many:
            self.step = [x, y]
            return True
        elif self.movement_valid(prev_x, prev_y, board) and counter == how_many:
            self.step = [prev_x, prev_y]
            return True

        return False

    # this just collect possible moves in given direction
    def move_collector(self, board, x, y, look_for, how_many, x_inc, y_inc):
        prev_x = x - x_inc
        prev_y = y - y_inc

        counter = 1
        x += x_inc
        y += y_inc
        while counter != how_many:
            if 0 < x < board.get_size() and 0 < y < board.get_size() and board.get_cell(x, y) == look_for:
                counter += 1
                x += x_inc
                y += y_inc
            else:
                break
        if self.movement_valid(x, y, board) and counter == how_many:
            return [x, y]
        elif self.movement_valid(prev_x, prev_y, board) and counter == how_many:
            return [prev_x, prev_y]
        return None

    # call this to get all possible moves which connects to a certain amount of already placed X or O rows
    def collect_moves(self, board, look_for, how_many):
        possible_moves = []
        for x in range(board.get_size()):
            for y in range(board.get_size()):
                if board.get_cell(x, y) == look_for:
                    # count x right straight
                    possible_moves.append(self.move_collector(board, x, y, look_for, how_many, 0, 1))
                    # count x left down
                    possible_moves.append(self.move_collector(board, x, y, look_for, how_many, 1, -1))
                    # count x right down
                    possible_moves.append(self.move_collector(board, x, y, look_for, how_many, 1, 1))
                    # count x down
                    possible_moves.append(self.move_collector(board, x, y, look_for, how_many, 1, 0))

        return possible_moves

    def movement_valid(self, x, y, board):
        if board.get_cell(x, y) != 'X' and board.get_cell(x, y) != 'O' and 0 < x < 98 and 0 < y < 98:
            return True
        return False

    def drop_duplicates(self, list_in):
        tuple_list = [tuple(item) for item in list_in]
        unique_list = list(set(tuple_list))
        unique_list = [list(item) for item in unique_list]
        return unique_list
