import statistics
import sys

from itertools import chain


class Cell:
    def __init__(self, number):
        self.number = number
        self.adjacent_cells = set()  # adjacent same-color cells
        self.__possible_neighbors = self.__calculate_possible_neighbors()

    def is_valid_neighbor(self, cell):
        return cell.number in self.__possible_neighbors

    def __calculate_possible_neighbors(self):
        possible_neighbors_set = set()

        vertically_head = self.number % 7 == 0
        vertically_tail = self.number % 7 == 6

        for neighbor in chain(
                range(self.number - 7, self.number - 5),
                range(self.number - 1, self.number + 2, 2),
                range(self.number + 6, self.number + 8),
        ):
            if neighbor < 0 or neighbor > 48:
                continue
            if vertically_head and neighbor in [
                self.number - 1,
                self.number + 6,
            ]:
                continue
            if vertically_tail and neighbor in [
                self.number - 6,
                self.number + 1,
            ]:
                continue

            possible_neighbors_set.add(neighbor)

        return possible_neighbors_set


def check_win_traverse(cell, traversed, head, tail, color):
    traversed.add(cell)
    if color == 1:  # blue
        if cell.number % 7 == 0:
            head = True
        if cell.number % 7 == 6:
            tail = True
    else:  # red
        if cell.number // 7 == 0:
            head = True
        if cell.number // 7 == 6:
            tail = True
    for adj_cell in cell.adjacent_cells:
        if adj_cell not in traversed:
            head, tail = check_win_traverse(adj_cell, traversed, head, tail, color)
    return head, tail


def check_win(player_set, color):
    traversed = set()
    for cell in player_set:
        head = False
        tail = False
        if cell not in traversed:
            head, tail = check_win_traverse(cell, traversed, head, tail, color)
            if head and tail:
                return True
    return False


def calculate_utility_traverse(cell, traversed, total_thread_length, horizontal_indices, vertical_indices):
    traversed.add(cell)
    horizontal_indices.append(cell.number % 7)
    vertical_indices.append(cell.number // 7)
    # if len(cell.adjacent_cells - traversed) != 0:
    #     total_thread_length += 1
    for adj_cell in cell.adjacent_cells:
        if adj_cell not in traversed:
            total_thread_length += 1
            total_thread_length = calculate_utility_traverse(adj_cell, traversed, total_thread_length,
                                                             horizontal_indices, vertical_indices)
    return total_thread_length


def calculate_utility(player_set, color):
    traversed = set()
    total_thread_length = 0
    horizontal_indices = list()
    vertical_indices = list()
    for cell in player_set:
        if cell not in traversed:
            total_thread_length = calculate_utility_traverse(cell, traversed, total_thread_length, horizontal_indices,
                                                             vertical_indices)
    horizontal_indices_pstdev = statistics.pstdev(horizontal_indices)  # pstdev: population standard deviation
    vertical_indices_pstdev = statistics.pstdev(vertical_indices)
    if horizontal_indices_pstdev == 0:
        horizontal_indices_pstdev += 1 / sys.maxsize
    if vertical_indices_pstdev == 0:
        vertical_indices_pstdev += 1 / sys.maxsize
    if color == 1:  # blue
        utility = pow(horizontal_indices_pstdev / vertical_indices_pstdev, total_thread_length)
    else:  # red
        utility = pow(vertical_indices_pstdev / horizontal_indices_pstdev, total_thread_length)
    return utility


def color_cell(player_set: set[Cell], white_set: set[Cell], white_cell: Cell):
    white_set -= {white_cell}
    player_set |= {white_cell}
    for fellow_cell in player_set:
        if fellow_cell.is_valid_neighbor(white_cell):
            fellow_cell.adjacent_cells.add(white_cell)
        if white_cell.is_valid_neighbor(fellow_cell):
            white_cell.adjacent_cells.add(fellow_cell)


def uncolor_cell(player_set: set[Cell], white_set: set[Cell], white_cell: Cell):
    player_set -= {white_cell}
    white_set |= {white_cell}
    for fellow_cell in player_set:
        if fellow_cell.is_valid_neighbor(white_cell):
            fellow_cell.adjacent_cells.remove(white_cell)
        if white_cell.is_valid_neighbor(fellow_cell):
            white_cell.adjacent_cells.remove(fellow_cell)


def negamax(player_set: set[Cell], opponent_set: set[Cell], white_set: set[Cell], depth: int, alpha: int, beta: int, color: int):
    # color: 1 for blue, -1 for red
    if depth == 0 or len(white_set) == 0 or check_win(opponent_set, -color):
        if color == 1:
            return color * (calculate_utility(player_set, color) - calculate_utility(opponent_set, -color)), None
        else:
            return color * (calculate_utility(opponent_set, -color) - calculate_utility(player_set, color)), None
    value = -sys.maxsize
    move = -1
    for white_cell in white_set.copy():
        color_cell(player_set, white_set, white_cell)
        negamax_result, _ = negamax(opponent_set, player_set, white_set, depth - 1, -beta, -alpha, -color)
        uncolor_cell(player_set, white_set, white_cell)
        if -negamax_result > value:
            move = white_cell.number
            value = max(value, -negamax_result)
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value, move


def main():
    cell_list: list[Cell] = list()
    white_set: set[Cell] = set()
    blue_set: set[Cell] = set()
    red_set: set[Cell] = set()
    for cell_number in range(0, 49):
        new_cell = Cell(cell_number)
        cell_list.append(new_cell)
        white_set.add(new_cell)
    list_of_lines: list[str] = list()
    for j in range(0, 49):
        if j < 10:
            list_of_lines.append(str(j) + " ")
        else:
            list_of_lines.append(str(j))
    print("Type '0' for starting the game or '1' for CPU to start the game")
    turn: bool = bool(int(input()))
    console(list_of_lines)
    while True:
        if turn:
            print("CPU turn : ")
            _, place_of_move = negamax(blue_set, red_set, white_set, 4, -sys.maxsize, sys.maxsize, 1)
            color_cell(blue_set, white_set, cell_list[place_of_move])
            print(place_of_move)
            list_of_lines[place_of_move] = "B "
            console(list_of_lines)
            if check_win(blue_set, 1) and len(blue_set) >= 7:
                print("Blue won")
                break
            if len(white_set) == 0:
                print("game over")
                break
            turn = not turn
        else:
            print("player turn\nplease enter your choice : ")
            while True:
                place_of_move = int(input())
                if cell_list[place_of_move] not in white_set:
                    print("Enter a valid number")
                else:
                    break
            color_cell(red_set, white_set, cell_list[place_of_move])
            list_of_lines[place_of_move] = "R "
            console(list_of_lines)
            if check_win(red_set, -1) and len(red_set) >= 7:
                print("Red won.")
                break
            if len(white_set) == 0:
                print("game over")
                break
            turn = not turn


def console(lines: list[str]):
    count1 = 0
    count2 = 7
    row_space = 0
    for i in range(0, 9):
        print("\033[31mR   ", end=" ")
    print("\033[0m", end="")

    for i in range(0, 8):
        for numOfRow in range(0, row_space):
            print(" ", end=" ")
        if i != 0:
            print(" ", end=" ")
            print("\033[34mB\033[0m   ", end=" ")
            for line in range(count1, count2):
                colored = False
                if "B" in lines[line]:
                    colored = True
                    print("\033[34m", end="")
                if "R" in lines[line]:
                    colored = True
                    print("\033[31m", end="")
                print(lines[line] + "  ", end=" ")
                if colored:
                    print("\033[0m", end="")
            print(" \033[34mB\033[0m")
            count1 += 7
            count2 += 7
            row_space += 1
        else:
            print("")

    for numOfRowSpaceForRed in range(0, row_space + 1):
        print(" ", end=" ")

    print("\033[31m", end="")
    for i in range(0, 9):
        print("R   ", end=" ")
    print("\033[0m", end="")

    print("\nplayer (RED) connects horizontally. ")
    print("CPU (BLUE) connects vertically. ")
    print()


if __name__ == "__main__":
    main()
