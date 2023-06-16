from sudoku import *
from sudoku_input import lst_sudoku

my_sudoku = Sudoku(lst_sudoku)
my_sudoku.report_matrix()

end_of_loop = False
sav_found = my_sudoku.found_values

while not end_of_loop:
    my_sudoku.propose_solution()
    my_sudoku.report_matrix()

    if my_sudoku.found_values >= 81 or sav_found == my_sudoku.found_values:
        end_of_loop = True
    else:
        sav_found = my_sudoku.found_values

if my_sudoku.found_values < 81:
    print("continue with Sudoku")
    cell, lst_duo = my_sudoku.get_first_duo()
    my_sudoku.treat_input(cell+str(lst_duo[1]))
    my_sudoku.report_matrix()

print(f"\nCheck solution: result={my_sudoku.is_solution_ok()}")