from pysat.solvers import Solver
from sat_encoder import SudokuSATEncoder

def find_all_solutions(grid):

    encoder = SudokuSATEncoder(grid)
    cnf = encoder.encode()
    
    solver = Solver(name='glucose3', bootstrap_with=cnf)
    
    solutions = []

    if not solver.solve():
        solver.delete()
        return False, []

    model = solver.get_model()
    first_solution = encoder.decode_solution(model)
    solutions.append(first_solution)
    

    current_solution = first_solution
    while True:    
        negated_clause = []
        for i in range(9):
            for j in range(9):
                n = current_solution[i][j]
                var_id = encoder.var(i, j, n)
                negated_clause.append(-var_id)
        
        solver.add_clause(negated_clause)

        if not solver.solve():
            break

        model = solver.get_model()
        current_solution = encoder.decode_solution(model)
        solutions.append(current_solution)

        if len(solutions) >= 100:
            break
    
    solver.delete()
    
    return True, solutions