import random
import sys
import tkinter as tk
from tkinter import messagebox


class Checker:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.is_queen = False

    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col



def get_cell_color(row, col):
    return "white" if (row + col) % 2 == 0 else "black"


def is_valid_cell(row, col):
    return 0 <= row < 7 and 0 <= col < 8


class CheckersBoard:
    def __init__(self, master):
        # Шашки
        self.cells = [[None for _ in range(8)] for _ in range(7)]
        # Канвасы, где мы ррисуем, по сути квадратики
        self.canvas_cells = [[None for _ in range(8)] for _ in range(7)]
        # Если мы выбрали шашку
        self.prev_highlighted = None
        # Окно, где у нас всё находится
        self.master = master
        # Возможные ходы, подсвечиваются
        self.highlighted_moves = []
        # Конец игры
        self.isOver = False
        # Ход игрока
        self.isPlayerTurn = True
        # Цвет игрока
        self.playerColor = "blue"
        # Цвет автобота
        self.autoColor = "red"
        # Ходы, которые нужно сделать
        self.required_highlighted = []

    # Перемещаем шашку на доске
    def place_checker(self, checker):
        if is_valid_cell(checker.row, checker.col):
            self.cells[checker.row][checker.col] = checker

    def get_cell_color(self, row, col):
        if self.cells[row][col] is not None:
            return self.cells[row][col].color
        else:
            return "white" if (row + col) % 2 == 0 else "black"

    # Создаём шашки, а также рисуем их в канвасах
    def draw_starting_position(self):
        for row in range(7):
            for col in range(8):
                if get_cell_color(row, col) == "white" and (row + col) % 2 == 0:
                    if row < 3:
                        checker_color = "red"
                        if row == 0 and (col == 2 or col == 4):
                            is_queen = True
                            checker = Checker(checker_color, row, col)
                            checker.is_queen = is_queen
                            self.place_checker(checker)

                            self.canvas_cells[row][col].create_oval(5, 5, 55, 55, fill=checker_color, tags="checker")
                            self.canvas_cells[row][col].create_oval(10, 10, 50, 50, fill='yellow',
                                                                    tags="crown")
                            self.canvas_cells[row][col].is_queen = is_queen
                        else:
                            checker = Checker(checker_color, row, col)
                            self.place_checker(checker)
                            is_queen = False
                            self.canvas_cells[row][col].create_oval(5, 5, 55, 55, fill=checker_color, tags="checker")
                            self.canvas_cells[row][col].is_queen = is_queen
                    elif row > 3:
                        checker_color = "blue"
                        if row == 6 and (col == 2 or col == 4):
                            is_queen = True
                            checker = Checker(checker_color, row, col)
                            checker.is_queen = is_queen
                            self.place_checker(checker)

                            self.canvas_cells[row][col].create_oval(5, 5, 55, 55, fill=checker_color, tags="checker")
                            self.canvas_cells[row][col].create_oval(10, 10, 50, 50, fill='yellow',
                                                                    tags="crown")
                            self.canvas_cells[row][col].is_queen = is_queen
                        else:
                            checker = Checker(checker_color, row, col)
                            self.place_checker(checker)
                            is_queen = False
                            self.canvas_cells[row][col].create_oval(5, 5, 55, 55, fill=checker_color, tags="checker")
                            self.canvas_cells[row][col].is_queen = is_queen

    # Создаем канвасы и окрашиваем их
    def create_gui(self):
        for row in range(7):
            for col in range(8):
                cell = tk.Canvas(self.master, width=60, height=60, bg=get_cell_color(row, col))
                cell.grid(row=row, column=col)
                cell.bind("<Button-1>", lambda event, r=row, c=col: self.on_cell_click(r, c, self.playerColor))
                self.canvas_cells[row][col] = cell
        self.draw_starting_position()

    # Отслеживание нажатий на канвас
    def on_cell_click(self, row, col, color):
        item_id = self.canvas_cells[row][col].find_withtag("checker")
        if item_id:
            # Получаем цвет
            current_color = self.canvas_cells[row][col].itemcget(item_id, "fill")
            if current_color == color:
                # Когда можно перешагнуть, нельзя выбирать другие ходы
                if self.required_highlighted and (row, col) not in self.required_highlighted:
                    if len(self.find_possibilities_to_attack(row, col)) == 0:
                        print(f"Есть подсвеченные ячейки, попытка выбрать неподсвеченную")
                        return

                # Снимаем подсветку с предыдущей ячейки, если она была подсвечена
                self.clear_highlighted_moves()
                # Выделяем необходимые
                self.light_required_moves()
                # Подсвечиваем для хода с этой ячейки
                self.light_current_cell(row, col)

        else:
            # Берем выделенную
            if self.prev_highlighted:
                prev_row, prev_col = self.prev_highlighted
                if (row, col) in self.highlighted_moves:
                    # Получаем цвет ходящего
                    if not self.isPlayerTurn:
                        color = self.playerColor
                    else:
                        color = self.autoColor
                    # Двигаем
                    self.move_checker(prev_row, prev_col, row, col)
                    deleted = False
                    # Если далеко пошли, значит надо проверить, кого убили
                    if abs(prev_row - row) > 1 and abs(prev_col - col) > 1:
                        # Проверяем, что атака происходит по диагонали
                        if abs(prev_row - row) == abs(prev_col - col):
                            deleted = True
                            self.delete_checker(prev_row, prev_col, row, col, color)
                    # Отрисовка
                    self.canvas_cells[prev_row][prev_col].delete('checker')
                    self.canvas_cells[prev_row][prev_col].delete('crown')
                    self.canvas_cells[row][col].create_oval(5, 5, 55, 55, fill=self.cells[row][col].color,
                                                            tags="checker")
                    if self.cells[row][col].is_queen:
                        self.canvas_cells[row][col].create_oval(10, 10, 50, 50, fill='yellow', tags="crown")
                    self.canvas_cells[prev_row][prev_col].config(bg="gray")
                    if self.is_game_over(color):
                        return
                    if not self.isPlayerTurn:
                        # Для автобота
                        if deleted and len(self.find_possibilities_to_attack(row, col)) > 0:
                            # Если мы можем продолжить кушать шашки
                            self.clear_highlighted_moves()
                            self.clear_saved_moves()
                            self.auto_turn()
                        else:
                            # Очищаем все и передаём ход
                            self.clear_highlighted_moves()
                            self.clear_saved_moves()
                            self.find_necessary_moves(self.playerColor)
                            self.light_required_moves()
                            self.isPlayerTurn = True
                    else:
                        # Для юзеробота
                        if deleted and len(self.find_possibilities_to_attack(row, col)) > 0:
                            # Если можно дальше кушать
                            self.isPlayerTurn = True
                            self.clear_highlighted_moves()
                            self.clear_saved_moves()
                            self.required_highlighted.append((row, col))
                            self.light_required_moves()
                        else:
                            # Очищаем и передаём
                            self.isPlayerTurn = False
                            self.clear_highlighted_moves()
                            self.clear_saved_moves()
                            self.auto_turn()

    # Очистка пометок на доске
    def light_current_cell(self, row, col):
        # Подсвечиваем текущую ячейку
        self.canvas_cells[row][col].config(bg="gray")
        # Получаем доступные ходы для выбранной шашки
        selected_checker = self.cells[row][col]
        available_moves = self.get_available_moves(self.cells[row][col])
        # Подсвечиваем клетки для доступных ходов
        for move_row, move_col in available_moves:
            self.canvas_cells[move_row][move_col].config(bg="lightgreen")
            self.highlighted_moves.append((move_row, move_col))
        # Обновляем предыдущую подсвеченную ячейку
        self.prev_highlighted = (row, col)

    # Очистка необходимых ходов
    def light_required_moves(self):
        for val in self.required_highlighted:
            self.canvas_cells[val[0]][val[1]].config(bg='red')

    # Для выбранной фишки находим подходящие ходы
    def get_available_moves(self, checker):
        moves = []
        row, col = checker.row, checker.col
        req_moves = self.find_possibilities_to_attack(row, col)
        if len(req_moves) > 0:
            if checker.is_queen:
                moves.extend(req_moves)
            else:
                return req_moves
        # Шашки могут двигаться по диагонали
        if checker.is_queen:
            # добавляем ходы королевы
            moves.extend(self.find_queen_moves(row, col, -1, 1))
            moves.extend(self.find_queen_moves(row, col, -1, -1))
            moves.extend(self.find_queen_moves(row, col, 1, 1))
            moves.extend(self.find_queen_moves(row, col, 1, -1))
        else:
            if checker.color == "red":
                moves.append((row + 1, col - 1))
                moves.append((row + 1, col + 1))
            elif checker.color == "blue":
                moves.append((row - 1, col - 1))
                moves.append((row - 1, col + 1))
        # Теперь уберем из списка те ходы, которые выходят за границы доски
        moves = [(r, c) for r, c in moves if 0 <= r < 8 and 0 <= c < 8]
        # Уберем из списка ходы, которые уже заняты другими шашками
        moves = [(r, c) for r, c in moves if self.cells[r][c] is None]
        return moves

    # Ходы королевы
    def find_queen_moves(self, row, col, row_dif, col_dif):
        moves = []
        ch_row = row + row_dif
        ch_col = col + col_dif
        while 8 > ch_col >= 0 and 7 > ch_row >= 0:
            if self.cells[ch_row][ch_col] is None and get_cell_color(ch_row, ch_col) == 'white':
                moves.append((ch_row, ch_col))
            else:
                break
            ch_row += row_dif
            ch_col += col_dif
        return moves

    # Можно ли ходить, для оценки конца игры
    def is_there_moves(self, color):
        return len(self.get_possible_checkers(color)) > 0

    # Смотри количество, которым можем ходить, тоже для оценки конца игры
    def count_checkers_by_color(self, color):
        count = 0
        for inner_ar in self.cells:
            for checker in inner_ar:
                if checker is not None and checker.color == color:
                    count += 1
        return count

    # Проверка на конец игры
    def is_game_over(self, color):
        checkers_count = self.count_checkers_by_color(color)
        is_game_over = False
        is_lose = False
        if checkers_count == 0:
            is_game_over = True
            if color == self.playerColor:
                is_lose = True

        if not self.is_there_moves(self.autoColor) or not self.is_there_moves(self.playerColor):
            is_game_over = True
            if self.count_checkers_by_color(self.playerColor) < self.count_checkers_by_color(self.autoColor):
                is_lose = True

        if is_game_over:
            if is_lose:
                message = 'Вы програли\nНачнём заново?'
            else:
                message = 'Вы выиграли\nНачнём заново?'
            if messagebox.askyesno('Конец игры', message):
                self.restart()
            else:
                sys.exit(1)

        return is_game_over

    # Очищаем выделенные клетки
    def clear_highlighted_moves(self):
        for inner_list in self.canvas_cells:
            for val in inner_list:
                if val["background"] != 'black':
                    val.config(bg='white')

    # Убираем почетки
    def clear_saved_moves(self):
        self.prev_highlighted = []
        self.required_highlighted = []
        self.highlighted_moves = []

    # Перемещаем фишки доске, также меняем координаты внутри фишек
    def move_checker(self, prev_row, prev_col, row, col):
        checker = self.cells[prev_row][prev_col]
        self.cells[prev_row][prev_col] = None
        checker.move(row, col)
        self.cells[row][col] = checker

    # Символический метод начала игры
    def start_game(self):
        self.create_gui()

    # Ищем ходы, которыми нужно ходить за игрока цвета
    def find_necessary_moves(self, color):
        self.clear_highlighted_moves()
        for row in range(7):
            for col in range(8):
                if self.cells[row][col] is None:
                    continue
                if self.cells[row][col].color != color:
                    continue
                if self.cells[row][col].is_queen:
                    continue
                if len(self.find_possibilities_to_attack(row, col)) > 0:
                    self.required_highlighted.append((row, col))

    # Берем шашку и оцениваем, можно ли ходить
    def find_possibilities_to_attack(self, row, col):
        color = self.cells[row][col].color
        moves = []
        if not self.cells[row][col].is_queen:
            if (col - 2 >= 0) and (row - 2 >= 0) and (self.cells[row - 1][col - 1] is not None) and (
                    self.cells[row - 1][col - 1].color != color) and (self.cells[row - 2][col - 2] is None):
                moves.append((row - 2, col - 2))
            if (col + 2 < 8) and (row - 2 >= 0) and (self.cells[row - 1][col + 1] is not None) and (
                    self.cells[row - 1][col + 1].color != color) and (self.cells[row - 2][col + 2] is None):
                moves.append((row - 2, col + 2))
            if (col - 2 >= 0) and (row + 2 < 7) and (self.cells[row + 1][col - 1] is not None) and (
                    self.cells[row + 1][col - 1].color != color) and (self.cells[row + 2][col - 2] is None):
                moves.append((row + 2, col - 2))
            if (col + 2 < 8) and (row + 2 < 7) and (self.cells[row + 1][col + 1] is not None) and (
                    self.cells[row + 1][col + 1].color != color) and (self.cells[row + 2][col + 2] is None):
                moves.append((row + 2, col + 2))
        else:
            moves.extend(self.find_queen_attack(row, col, -1, -1, color))
            moves.extend(self.find_queen_attack(row, col, -1, 1, color))
            moves.extend(self.find_queen_attack(row, col, 1, -1, color))
            moves.extend(self.find_queen_attack(row, col, 1, 1, color))
        return moves

    def find_queen_attack(self, row, col, row_dif, col_dif, color):
        enemy_has_met = False
        moves = []
        ch_row = row + row_dif
        ch_col = col + col_dif
        while 8 > ch_col >= 0 and 7 > ch_row >= 0:  # Изменили условие на 7 для высоты
            if self.cells[ch_row][ch_col] is None and get_cell_color(ch_row, ch_col) == 'white' and enemy_has_met:
                moves.append((ch_row, ch_col))
            if self.cells[ch_row][ch_col] is not None:
                if enemy_has_met:
                    break
                else:
                    if self.cells[ch_row][ch_col].color == color:
                        break
                    else:
                        enemy_has_met = True
            ch_row += row_dif
            ch_col += col_dif
        return moves

    def auto_turn(self):
        if len(self.required_highlighted) == 0:
            self.find_necessary_moves(self.autoColor)
        if len(self.required_highlighted) > 0:
            move = random.choice(self.required_highlighted)
            prev_row = move[0]
            prev_col = move[1]
            self.on_cell_click(prev_row, prev_col, self.autoColor)
            row, col = random.choice(self.highlighted_moves)
        else:
            checker = random.choice(self.get_possible_checkers(self.autoColor))
            prev_row, prev_col = checker.row, checker.col
            self.on_cell_click(prev_row, prev_col, self.autoColor)
            next_move = random.choice(self.highlighted_moves)
            row, col = next_move[0], next_move[1]
        self.on_cell_click(row, col, self.autoColor)

    # Проверяем, есть ли у нас шашки, которые могут ходить
    def get_possible_checkers(self, color):
        checkers = []
        for row in range(7):
            for col in range(8):
                moves = []
                checker = self.cells[row][col]
                if checker is None:
                    continue
                if checker.color != color:
                    continue
                row, col = checker.row, checker.col
                # Шашки могут двигаться по диагонали
                if checker.is_queen:
                    moves.extend(self.find_queen_moves(row, col, -1, 1))
                    moves.extend(self.find_queen_moves(row, col, -1, -1))
                    moves.extend(self.find_queen_moves(row, col, 1, 1))
                    moves.extend(self.find_queen_moves(row, col, 1, -1))
                else:
                    if self.autoColor == checker.color:
                        moves.append((row + 1, col - 1))
                        moves.append((row + 1, col + 1))
                    elif self.playerColor == checker.color:
                        moves.append((row - 1, col - 1))
                        moves.append((row - 1, col + 1))
                # Теперь уберем из списка те ходы, которые выходят за границы доски
                moves = [(r, c) for r, c in moves if 0 <= r < 7 and 0 <= c < 8]
                # Уберем из списка ходы, которые уже заняты другими шашками
                moves = [(r, c) for r, c in moves if self.cells[r][c] is None]
                if len(moves) > 0 or len(self.find_possibilities_to_attack(row, col)) > 0:
                    checkers.append(checker)
        return checkers

    def delete_checker(self, prev_row, prev_col, row, col, enemy_color):
        if prev_row > row:
            low_row = row
            high_row = prev_row
        else:
            low_row = prev_row
            high_row = row
        if prev_col > col:
            low_col = col
            high_col = prev_col
        else:
            low_col = prev_col
            high_col = col

        deleted = False  # Флаг, указывающий, была ли фишка срублена
        for r in range(low_row, high_row + 1):
            for c in range(low_col, high_col + 1):
                checker = self.cells[r][c]
                if checker is not None and checker.color == enemy_color:
                    # Проверяем, что атака происходит по диагонали
                    if abs(prev_row - row) == abs(prev_col - col):
                        deleted = True
                        self.cells[r][c] = None
                        self.canvas_cells[r][c].delete('checker')
                        self.canvas_cells[r][c].delete('crown')

        return deleted

    def restart(self):
        self.cells = [[None for _ in range(8)] for _ in range(8)]
        self.canvas_cells = [[None for _ in range(8)] for _ in range(8)]
        self.prev_highlighted = None
        self.highlighted_moves = []
        self.isOver = False
        self.isPlayerTurn = True
        self.required_highlighted = []
        self.start_game()
