import math
HOR = "-"
VER = "|"
SQUARE = "="
SPACE = " "
ROW_NUM_TO_CHAR = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J"}
ROW_CHAR_TO_NUM = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}


def count_occurrence_in_list(s, lst):
    cnt = 0
    for item in lst:
        if item == s:
            cnt += 1
    return cnt


def calculate_index_in_matrix(row, col):
    return row * 9 + col


def calculate_rc_in_matrix(i):
    r = math.floor(i / 9)
    c = i % 9
    return r, c


def calculate_coord(i):
    r, c = calculate_rc_in_matrix(i)
    return ROW_NUM_TO_CHAR[r] + str(c+1)


class Sudoku:
    def __init__(self, lst):
        print("Sudoku.__init__()", lst)
        self.found_values = 0
        print(f"$$$ self.found_values={self.found_values}")
        self.items_to_treat = []
        self.matrix = []   # this list will contain a tuple for every Sudoku cell (row, col, value, possible values)
        self.squares = {    # every square will contain a list of indices corresponding to a Sudoku cell
            "S1": [], "S2": [], "S3": [],
            "S4": [], "S5": [], "S6": [],
            "S7": [], "S8": [], "S9": []
        }
        self.fill_indices_in_squares()
        self.create_empty_matrix()
        self.level = round(100 - 100 * len(lst) / 81, 2)
        print(f"New  Sudoku: {len(lst)} items given on a total of 81 items - level {self.level}%")
        for item in lst:
            self.treat_input(item)
        print("Sudoku.__init__() has ended\n")

    def create_empty_matrix(self):
        print("Sudoku.create_empty_matrix()")
        for row in range(0, 9):
            for col in range(0, 9):
                self.matrix.append((row, col, 0, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

    def fill_indices_in_squares(self):
        print("Sudoku.fill_indices_in_squares()")
        for row in range(0, 9):
            for col in range(0, 9):
                ix = calculate_index_in_matrix(row, col)
                if row in [0, 1, 2] and col in [0, 1, 2]:
                    self.squares["S1"].append(ix)
                if row in [0, 1, 2] and col in [3, 4, 5]:
                    self.squares["S2"].append(ix)
                if row in [0, 1, 2] and col in [6, 7, 8]:
                    self.squares["S3"].append(ix)
                if row in [3, 4, 5] and col in [0, 1, 2]:
                    self.squares["S4"].append(ix)
                if row in [3, 4, 5] and col in [3, 4, 5]:
                    self.squares["S5"].append(ix)
                if row in [3, 4, 5] and col in [6, 7, 8]:
                    self.squares["S6"].append(ix)
                if row in [6, 7, 8] and col in [0, 1, 2]:
                    self.squares["S7"].append(ix)
                if row in [6, 7, 8] and col in [3, 4, 5]:
                    self.squares["S8"].append(ix)
                if row in [6, 7, 8] and col in [6, 7, 8]:
                    self.squares["S9"].append(ix)

    def transform_guess(self, guess):
        # In: A12 means add value 2 to cell A1
        # In: A1d2 means delete value 2 from the list of possibilities for cell A1
        # Out: ix, row, col, val, operand where operand in ["add", "remove"]
        print("Sudoku.transform_guess()", guess)
        guess = guess.upper()
        row = ROW_CHAR_TO_NUM[guess[0]]
        col = int(guess[1]) - 1
        ix = calculate_index_in_matrix(row, col)
        input_val = guess[2:]
        if len(input_val) == 1:
            val = int(guess[2])
            operand = "add"
        else:
            val = int(guess[3])
            operand = "remove"
        return ix, row, col, val, operand

    def treat_input(self, guess):
        print("\nSudoku.treat_input()", guess)
        ix, row, col, val, operand = self.transform_guess(guess)
        if operand == "add" and self.matrix[ix][2] == 0:
            self.matrix[ix] = (row, col, val, [])
            self.found_values += 1
            print(f"$$$ self.found_values={self.found_values} location={calculate_coord(ix)} value={val}")
            self.clear_square(ix, val)
            self.clear_row(row, col, val)
            self.clear_column(row, col, val)
        elif operand == "remove":
            print(f"{calculate_coord(ix)}: remove {val} from {self.matrix[ix][3]}")
            self.matrix[ix][3].remove(val)
            if len(self.matrix[ix][3]) == 1:
                val = self.matrix[ix][3][0]
                self.treat_input(calculate_coord(ix)+str(val))

    def get_square(self, ix):
        print("Sudoku.get_square()", ix)
        for square in self.squares:
            if ix in self.squares[square]:
                return square

    def clear_square(self, i, val):
        print(f"Sudoku.clear_square() i={i} val={val}")
        square = self.get_square(i)
        for ix in self.squares[square]:
            if i != ix and val in self.matrix[ix][3]:
                self.matrix[ix][3].remove(val)
                if len(self.matrix[ix][3]) == 1: # we generated a new correct guess
                    r_clr = self.matrix[ix][0]
                    c_clr = self.matrix[ix][1]
                    v_clr = self.matrix[ix][3][0]
                    self.matrix[ix] = (r_clr, c_clr, v_clr, [])
                    self.found_values += 1
                    print(f"$$$ self.found_values={self.found_values} location={calculate_coord(ix)} value={v_clr}")
                    self.clear_row(r_clr, c_clr, v_clr)
                    self.clear_column(r_clr, c_clr, v_clr)
                    self.clear_square(ix, v_clr)

    def clear_row(self, row, col, val):
        print(f"Sudoku.clear_row() row={row}, col={col}, val={val}")
        for c in range(0, 9):
            ix = calculate_index_in_matrix(row, c)
            if c != col and val in self.matrix[ix][3]:
                self.matrix[ix][3].remove(val)
                if len(self.matrix[ix][3]) == 1:  # we generated a new correct guess
                    r_clr = self.matrix[ix][0]
                    c_clr = self.matrix[ix][1]
                    v_clr = self.matrix[ix][3][0]
                    self.matrix[ix] = (r_clr, c_clr, v_clr, [])
                    self.found_values += 1
                    print(f"$$$ self.found_values={self.found_values} location={calculate_coord(ix)} value={v_clr}")
                    self.clear_square(ix, v_clr)
                    self.clear_column(r_clr, c_clr, v_clr)
                    self.clear_row(r_clr, c_clr, v_clr)

    def clear_column(self, row, col, val):
        print(f"Sudoku.clear_column() row={row}, col={col}, val={val}")
        for r in range(0, 9):
            ix = calculate_index_in_matrix(r, col)
            if r != row and val in self.matrix[ix][3]:
                self.matrix[ix][3].remove(val)
                if len(self.matrix[ix][3]) == 1:  # we generated a new correct guess
                    r_clr = self.matrix[ix][0]
                    c_clr = self.matrix[ix][1]
                    v_clr = self.matrix[ix][3][0]
                    self.matrix[ix] = (r_clr, c_clr, v_clr, [])
                    self.found_values += 1
                    print(f"$$$ self.found_values={self.found_values} location={calculate_coord(ix)} value={v_clr}")
                    self.clear_square(ix, v_clr)
                    self.clear_row(r_clr, c_clr, v_clr)
                    self.clear_column(r_clr, c_clr, v_clr)

    def report_matrix(self):
        print("\nSudoku.report_matrix()")
        print("######################")
        line_header = SPACE * 3
        for i in range(1, 10):
            line_header += SPACE * 4 + str(i) + SPACE * 5
        print(line_header)
        print("  " + SQUARE*91)
        for row in range(0, 9):
            line = f"{ ROW_NUM_TO_CHAR[row]} {VER}"
            for col in range(0, 9):
                ix = calculate_index_in_matrix(row, col)
                val = self.matrix[ix][2]
                if val == 0:
                    possibilities = ""
                    for possibility in self.matrix[ix][3]:
                        possibilities += str(possibility)
                    n_left = math.floor((9 - len(possibilities)) / 2)
                    n_right = 9 - n_left - len(possibilities)
                    line += SPACE * n_left + possibilities + SPACE * n_right
                else:
                    line += SPACE * 4 + str(val) + SPACE * 4
                if (col + 1) % 3 == 0:
                    line += VER
                else:
                    line += SPACE
            print(line)
            if (row + 1) % 3 == 0:
                print("  " + SQUARE * 91)
            else:
                print("  " + HOR * 91)
        print(f"found values: {self.found_values}\n")
        if self.found_values == 81:
            print("congratulations: you won")

    def report_squares(self):
        print("Sudoku.report_squares()")
        for square in self.squares:
            self.report_square(square)
            print()

    def report_square(self, square):
        print("Sudoku.report_square()", square)
        i = 0
        line = ""
        for ix in self.squares[square]:
            val = self.matrix[ix][2]
            lst = self.matrix[ix][3]
            if val == 0:
                line += "["
                for item in lst:
                    line += str(item) + ","
                line += "] "
            else:
                line += str(val)
            i += 1
            if i % 3 == 0:
                print(line)
                line = ""

    def report_possibilities(self):
        print("Sudoku.report_possibilities()")
        for row in range(0, 9):
            line = ""
            for col in range(0, 9):
                ix = row * 9 + col
                val = self.matrix[ix][2]
                lst = self.matrix[ix][3]
                if val == 0:
                    line += str(lst) + " "
                else:
                    line += str(val) + " "
            print(f"row {row}: ", line)

    def propose_solution(self):
        print("Sudoku.propose_solution()")
        print("#########################")
        self.find_duos()
        self.find_triples()
        self.find_unique_value_in_square()
        self.find_unique_value_in_row()
        self.find_unique_value_in_column()

    def find_duos(self):
        print("Sudoku.find_duos()")
        duos_in_square = {}
        for ix in range(0, 81):
            if len(self.matrix[ix][3]) == 2:
                print(calculate_coord(ix), self.matrix[ix][3])
                square = self.get_square(ix)
                duo = str(self.matrix[ix][3][0]) + str(self.matrix[ix][3][1])
                if square in duos_in_square:
                    if duo in duos_in_square[square]:
                        print(f"found duo {duo} in same square {square}")
                        val0_to_be_removed = int(duo[0])
                        val1_to_be_removed = int(duo[1])
                        for i in self.squares[square]:
                            if len(self.matrix[i][3]) == 2 and self.matrix[i][3][0] == val0_to_be_removed and \
                                   self.matrix[i][3][1] == val1_to_be_removed:
                                continue
                            else:
                                if val0_to_be_removed in self.matrix[i][3]:
                                    new_guess = calculate_coord(i) + "d" + duo[0]
                                    self.treat_input(new_guess)
                                if val1_to_be_removed in self.matrix[i][3]:
                                    new_guess = calculate_coord(i) + "d" + duo[1]
                                    self.treat_input(new_guess)
                    else:
                        duos_in_square[square].append(duo)
                else:
                    duos_in_square[square] = [duo]

    def find_triples(self):
        print("Sudoku.find_triples()")
        triples_in_square = {}
        for ix in range(0, 81):
            if len(self.matrix[ix][3]) == 3:
                print(calculate_coord(ix), self.matrix[ix][3])
                square = self.get_square(ix)
                triple = str(self.matrix[ix][3][0]) + str(self.matrix[ix][3][1]) + str(self.matrix[ix][3][2])
                if square in triples_in_square:
                    if count_occurrence_in_list(triple, triples_in_square[square]) == 2:
                        print(f"found triple {triple} 3 times in same square {square}")
                        val0_to_be_removed = int(triple[0])
                        val1_to_be_removed = int(triple[1])
                        val2_to_be_removed = int(triple[2])
                        for i in self.squares[square]:
                            if len(self.matrix[i][3]) == 3 and self.matrix[i][3][0] == val0_to_be_removed and \
                                   self.matrix[i][3][1] == val1_to_be_removed and \
                                   self.matrix[i][3][2] == val2_to_be_removed :
                                continue
                            else:
                                if val0_to_be_removed in self.matrix[i][3]:
                                    new_guess = calculate_coord(i) + "d" + triple[0]
                                    self.treat_input(new_guess)
                                if val1_to_be_removed in self.matrix[i][3]:
                                    new_guess = calculate_coord(i) + "d" + triple[1]
                                    self.treat_input(new_guess)
                                if val2_to_be_removed in self.matrix[i][3]:
                                    new_guess = calculate_coord(i) + "d" + triple[2]
                                    self.treat_input(new_guess)
                    else:
                        triples_in_square[square].append(triple)
                else:
                    triples_in_square[square] = [triple]

    def find_unique_value_in_square(self):
        print("Sudoku.find_unique_value_in_square()")
        for square in self.squares:
            square_occurrences = {}
            for i in range(1,10):
                square_occurrences[str(i)] = 0
            for i in self.squares[square]:
                for num in self.matrix[i][3]:
                    square_occurrences[str(num)] += 1
            for n, occ in square_occurrences.items():
                if occ == 1:
                    for i in self.squares[square]:
                        if int(n) in self.matrix[i][3]:
                            # print(f"{self.calculate_coord(i)} has unique value {n}")
                            new_guess = calculate_coord(i) + n
                            self.treat_input(new_guess)

    def find_unique_value_in_row(self):
        print("Sudoku.find_unique_value_in_row()")
        for row in range(0, 9):
            row_occurrences = {}
            for i in range(1, 10):
                row_occurrences[str(i)] = 0
            for i in range(0, 9):
                ix = i + row * 9
                for num in self.matrix[ix][3]:
                    row_occurrences[str(num)] += 1
            for n, occ in row_occurrences.items():
                if occ == 1:
                    for i in range(0, 9):
                        ix = i + row * 9
                        if int(n) in self.matrix[ix][3]:
                            # print(f"{self.calculate_coord(ix)} has unique value {n}")
                            new_guess = calculate_coord(ix) + n
                            self.treat_input(new_guess)

    def find_unique_value_in_column(self):
        print("Sudoku.find_unique_value_in_column()")
        for col in range(0, 9):
            col_occurrences = {}
            for i in range(1, 10):
                col_occurrences[str(i)] = 0
            for i in range(0, 9):
                ix = col + 9 * i
                for num in self.matrix[ix][3]:
                    col_occurrences[str(num)] += 1
            for n, occ in col_occurrences.items():
                if occ == 1:
                    for i in range(0, 9):
                        ix = col + 9 * i
                        if int(n) in self.matrix[ix][3]:
                            # print(f"{self.calculate_coord(ix)} has unique value {n}")
                            new_guess = calculate_coord(ix) + n
                            self.treat_input(new_guess)

    def get_first_duo(self):
        print("Sudoku.get_first_duo()")
        for ix in range(0,81):
            if len(self.matrix[ix][3]) == 2:
                return ROW_NUM_TO_CHAR[self.matrix[ix][0]]+str(self.matrix[ix][1]+1), self.matrix[ix][3]

    def is_solution_ok(self):
        for i in range(81):
            if len(self.matrix[i][3]) != 0 or self.matrix[i][2] == 0:
                return "NOK: some element(s) not found"

        for S, ix_lst in self.squares.items():
            check_lst = []
            for i in ix_lst:
                val = self.matrix[i][2]
                if not val in check_lst:
                    check_lst.append(val)
            if len(check_lst) != 9:
                return f"NOK: issue with square {S}"

        for row in range(9):
            check_lst = []
            for col in range(9):
                i = 9 * row + col
                val = self.matrix[i][2]
                if not val in check_lst:
                    check_lst.append(val)
            if len(check_lst) != 9:
                return f"NOK: issue with row {row}"

        for col in range(9):
            check_lst = []
            for row in range(9):
                i = 9 * row + col
                val = self.matrix[i][2]
                if not val in check_lst:
                    check_lst.append(val)
            if len(check_lst) != 9:
                return f"NOK: issue with column {col}"
        return "OK"


