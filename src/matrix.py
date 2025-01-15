class Matrix:
    def __init__(self, n, m):
        self.n = n  # number of rows
        self.m = m  # number of columns
        self.matrix = self.create(n, m)
    
    def create(self, n, m):
        """Creates an n x m matrix initialized with zeros."""
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
        return "\n".join(["\t".join(map(str, row)) for row in self.matrix])