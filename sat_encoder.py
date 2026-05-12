from pysat.formula import CNF

class SudokuSATEncoder:
    def __init__(self, grid):
        self.grid = grid
        self.cnf = CNF()
        self.var_count = 0
        self.vars = {}
        var_id = 1
        
        for i in range(9):
            for j in range(9):
                for n in range(1, 10):
                    self.vars[(i, j, n)] = var_id
                    var_id += 1
        
        self.var_count = var_id - 1
    
    def var(self, row, col, num):
        return self.vars[(row, col, num)]
    
    def encode(self):

        for i in range(9):
            for j in range(9):
                clause = [self.var(i, j, n) for n in range(1, 10)]
                self.cnf.append(clause)
        
        for i in range(9):
            for j in range(9):
                for n1 in range(1, 10):
                    for n2 in range(n1 + 1, 10):
                        clause = [-self.var(i, j, n1), -self.var(i, j, n2)]
                        self.cnf.append(clause)
        for i in range(9):
            for n in range(1, 10):

                clause = [self.var(i, j, n) for j in range(9)]
                self.cnf.append(clause)

                for j1 in range(9):
                    for j2 in range(j1 + 1, 9):
                        clause = [-self.var(i, j1, n), -self.var(i, j2, n)]
                        self.cnf.append(clause)
        for j in range(9):
            for n in range(1, 10):
                clause = [self.var(i, j, n) for i in range(9)]
                self.cnf.append(clause)

                for i1 in range(9):
                    for i2 in range(i1 + 1, 9):
                        clause = [-self.var(i1, j, n), -self.var(i2, j, n)]
                        self.cnf.append(clause)
        
        for block_row in range(3):
            for block_col in range(3):
                for n in range(1, 10):
                    clause = []
                    for i in range(block_row * 3, block_row * 3 + 3):
                        for j in range(block_col * 3, block_col * 3 + 3):
                            clause.append(self.var(i, j, n))
                    self.cnf.append(clause)
                    
                    cells = [(i, j) for i in range(block_row * 3, block_row * 3 + 3)
                            for j in range(block_col * 3, block_col * 3 + 3)]
                    for idx1, (i1, j1) in enumerate(cells):
                        for i2, j2 in cells[idx1 + 1:]:
                            clause = [-self.var(i1, j1, n), -self.var(i2, j2, n)]
                            self.cnf.append(clause)
        
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    n = self.grid[i][j]
                    clause = [self.var(i, j, n)]
                    self.cnf.append(clause)
        
        return self.cnf
    
    def decode_solution(self, model):
        solution_grid = [[0 for _ in range(9)] for _ in range(9)]
        positive_vars = {var for var in model if var > 0}
        
        for i in range(9):
            for j in range(9):
                for n in range(1, 10):
                    var_id = self.var(i, j, n)
                    if var_id in positive_vars:
                        solution_grid[i][j] = n
                        break
        
        return solution_grid