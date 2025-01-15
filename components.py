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


class Component:
    def __init__(self, node_i, node_j, value):
        self.node_i = node_i  # node i connection
        self.node_j = node_j  # node b connection
        self.value = value    # component value (resistance, capacitance, etc.)

    def __str__(self):
        return f"{self.__class__.__name__}({self.node_i}, {self.node_j}, {self.value})"


class Resistor(Component):
    def __init__(self, node_i, node_j, resistance):
        super().__init__(node_i, node_j, resistance)
        self.resistance = resistance
    
    def add_to_netlist(self, G: Matrix) -> None:
        conductance = 1 / self.resistance # Calculate conductance
        if self.node_i != 0:
            G.matrix[self.node_i - 1][self.node_i - 1] = G.matrix[self.node_i - 1][self.node_i - 1] + conductance
        if self.node_j !=0:
            G.matrix[self.node_j - 1][self.node_j - 1] = G.matrix[self.node_j - 1][self.node_j - 1] + conductance
        if self.node_i != 0 and self.node_j != 0:
            G.matrix[self.node_i - 1][self.node_j - 1] = G.matrix[self.node_i - 1][self.node_j - 1] - conductance
            G.matrix[self.node_j - 1][self.node_i - 1] = G.matrix[self.node_j - 1][self.node_i - 1] - conductance


class Capacitor(Component):
    def __init__(self, node_i, node_j, capacitance):
        super().__init__(node_i, node_j, capacitance)
        self.capacitance = capacitance
    
    def add_to_netlist(self, C: Matrix) -> None:
        if self.node_i != 0:
            C.matrix[self.node_i - 1][self.node_i - 1] = C.matrix[self.node_i - 1][self.node_i - 1] + self.capacitance
        if self.node_j !=0:
            C.matrix[self.node_j - 1][self.node_j - 1] = C.matrix[self.node_j - 1][self.node_j - 1] + self.capacitance
        if self.node_i != 0 and self.node_j != 0:
            C.matrix[self.node_i - 1][self.node_j - 1] = C.matrix[self.node_i - 1][self.node_j - 1] - self.capacitance
            C.matrix[self.node_j - 1][self.node_i - 1] = C.matrix[self.node_j - 1][self.node_i - 1] - self.capacitance
        

class Inductor(Component):
    def __init__(self, node_i, node_j, inductance):
        super().__init__(node_i, node_j, inductance)
        self.inductance = inductance
    
    def add_to_netlist(self, G: Matrix, C: Matrix, b: Matrix) -> None:
        G.extend()
        C.extend()
        b.add_row()
        d = G.n - 1
        C.matrix[d][d] = -self.inductance
        if self.node_i != 0:
            G.matrix[self.node_i - 1][d] = 1
            G.matrix[d][self.node_i - 1] = 1
        if self.node_j !=0:
            G.matrix[self.node_j - 1][d] = -1
            G.matrix[d][self.node_j - 1] = -1

class CurrentSource(Component):
    def __init__(self, node_i, node_j, current):
        super().__init__(node_i, node_j, current)
        self.current = current

    def add_to_netlist(self, b: Matrix) -> None:
        if self.node_i != 0:
            b.matrix[self.node_i - 1][0] = b.matrix[self.node_i - 1][0] - self.current
        if self.node_j !=0:
            b.matrix[self.node_j - 1][0] = b.matrix[self.node_j - 1][0] + self.current
            
            
G = Matrix(4,4)
C = Matrix(4,4)
b = Matrix(4,1)
# print(G)
# print()
# G.initialize(1)
# print(G)
# print()
# G.extend()
# print(G)
# print()

I1 = CurrentSource(0,1,1)
L1 = Inductor(1,0,0.799e-9)
C1 = Capacitor(1,0,0.319e-6)
C2 = Capacitor(2,3,63.72e-12)
C3 = Capacitor(3,0,0.319e-6)
R1 = Resistor(1,0,5)
R2 = Resistor(1,2,5)
R3 = Resistor(3,0,5)
R4 = Resistor(3,4,5)
R5 = Resistor(4,0,1e3)

I1.add_to_netlist(b)
L1.add_to_netlist(G, C, b)
C1.add_to_netlist(C)
C2.add_to_netlist(C)
C3.add_to_netlist(C)
R1.add_to_netlist(G)
R2.add_to_netlist(G)
R3.add_to_netlist(G)
R4.add_to_netlist(G)
R5.add_to_netlist(G)


print(G)
print()
print(C)
print()
print(b)