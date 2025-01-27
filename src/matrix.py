class Matrix:
    def __init__(self, n, m, symbolic):
        self.n = n  # number of rows
        self.m = m  # number of columns
        self.symbolic = symbolic
        self.matrix = self.create(n, m, symbolic)
    
    def create(self, n, m, symbolic=False):
        """Creates an n x m matrix initialized with zeros."""
        if symbolic:
            return [[""] * m for _ in range(n)]
        return [[0] * m for _ in range(n)]
    
    def initialize(self, x):
        """Initializes all values in the matrix with the value x."""
        self.matrix = [[x] * self.m for _ in range(self.n)]
    
    def add_row(self):
        """Adds an extra row to the matrix, initialized with zeros."""
        self.matrix.append([0] * self.m)
        self.n += 1  # Update the row count

    def add_column(self):
        """Adds an extra column to the matrix, initialized with zeros."""
        for row in self.matrix:
            row.append(0)
        self.m += 1  # Update the column count
    
    def extend(self):
        self.add_column()
        self.add_row()

    def __str__(self):
        """
        Returns a string representation of the matrix.
        
        Each row of the matrix is represented as a string with the elements
        separated by tabs. The rows are then joined by newlines.
        
        :return: string representation of the matrix
        :rtype: str
        """
        matrix_str = ""
        max_len = max(len(s) for row in self.matrix for s in row)
        for row in self.matrix:
            row_str = "\t".join("0" if item == "" else str(item + (max_len - len(item))*" ").lstrip(" +") for item in row)
            matrix_str += row_str + "\n"
        return matrix_str.strip()