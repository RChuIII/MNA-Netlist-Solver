from .matrix import Matrix
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
            G.matrix[self.node_i - 1][self.node_i - 1] += conductance
        if self.node_j !=0:
            G.matrix[self.node_j - 1][self.node_j - 1] += conductance
        if self.node_i != 0 and self.node_j != 0:
            G.matrix[self.node_i - 1][self.node_j - 1] += -conductance
            G.matrix[self.node_j - 1][self.node_i - 1] += -conductance

class Capacitor(Component):
    def __init__(self, node_i, node_j, capacitance):
        super().__init__(node_i, node_j, capacitance)
        self.capacitance = capacitance
    
    def add_to_netlist(self, C: Matrix) -> None:
        if self.node_i != 0:
            C.matrix[self.node_i - 1][self.node_i - 1] += self.capacitance
        if self.node_j !=0:
            C.matrix[self.node_j - 1][self.node_j - 1] += self.capacitance
        if self.node_i != 0 and self.node_j != 0:
            C.matrix[self.node_i - 1][self.node_j - 1] += -self.capacitance
            C.matrix[self.node_j - 1][self.node_i - 1] += -self.capacitance
        

class Inductor(Component):
    def __init__(self, node_i, node_j, inductance):
        super().__init__(node_i, node_j, inductance)
        self.inductance = inductance
    
    def add_to_netlist(self, G: Matrix, C: Matrix, b: Matrix) -> None:
        G.extend()
        C.extend()
        b.add_row()
        d = G.n - 1
        C.matrix[d][d] += -self.inductance
        if self.node_i != 0:
            G.matrix[self.node_i - 1][d] += 1
            G.matrix[d][self.node_i - 1] += 1
        if self.node_j !=0:
            G.matrix[self.node_j - 1][d] += -1
            G.matrix[d][self.node_j - 1] += -1

class CurrentSource(Component):
    def __init__(self, node_i, node_j, current):
        super().__init__(node_i, node_j, current)
        self.current = current

    def add_to_netlist(self, b: Matrix) -> None:
        if self.node_i != 0:
            b.matrix[self.node_i - 1][0] += -self.current
        if self.node_j !=0:
            b.matrix[self.node_j - 1][0] += self.current

class VCCS(Component):
    # Note j nodes are the CONTROLLING nodes, and k nodes are the CONTROLLED nodes
    # 1----[VCCS (gm(v1-v3))]----2 => j=1, j'=3, k=1, k'=2
    def __init__(self, node_j, node_jp, gm, node_k, node_kp):
        super().__init__(node_j, node_jp, gm)
        self.gm = gm
        self.node_j = node_j
        self.node_jp = node_jp
        self.node_k = node_k
        self.node_kp = node_kp
    
    def add_to_netlist(self, G: Matrix) -> None:
        if self.node_k != 0:
            if self.node_j != 0:
                G.matrix[self.node_k - 1][self.node_j - 1] += self.gm
            if self.node_jp != 0:
                G.matrix[self.node_k - 1][self.node_jp - 1] += -self.gm
        if self.node_kp != 0:
            if self.node_j != 0:
                G.matrix[self.node_kp - 1][self.node_j - 1] += -self.gm
            if self.node_jp != 0:
                G.matrix[self.node_kp - 1][self.node_jp - 1] += self.gm


class VCVS(Component):
    def __init__(self, node_j, node_jp, A, node_k, node_kp):
        super().__init__(node_j, node_jp, A)
        self.A = A
        self.node_j = node_j
        self.node_jp = node_jp
        self.node_k = node_k
        self.node_kp = node_kp

    def add_to_netlist(self, G: Matrix, C: Matrix, b: Matrix) -> None:
        G.extend()
        C.extend()
        b.add_row()
        d = G.n - 1
        if self.node_k != 0:
            G.matrix[self.node_k - 1][d] += 1
            G.matrix[d][self.node_k - 1] += 1

        if self.node_kp != 0:
            G.matrix[self.node_kp - 1][d] += -1
            G.matrix[d][self.node_kp - 1] += -1
        
        if self.node_j != 0:
            G.matrix[d][self.node_j] += -self.A

        if self.node_jp != 0:
            G.matrix[d][self.node_jp] += self.A

class CCCS(Component):
    def __init__(self, node_j, node_jp, alpha, node_k, node_kp):
        super().__init__(node_j, node_jp, alpha)
        self.alpha = alpha
        self.node_j = node_j
        self.node_jp = node_jp
        self.node_k = node_k
        self.node_kp = node_kp

    def add_to_netlist(self, G: Matrix, C: Matrix, b: Matrix) -> None:
        G.extend()
        C.extend()
        b.add_row()
        d = G.n - 1
        if self.node_k != 0:
            G.matrix[self.node_k - 1][d] += f" +{self.alpha}"

        if self.node_kp != 0:
            G.matrix[self.node_kp - 1][d] += f" -{self.alpha}"
        
        if self.node_j != 0:
            G.matrix[d][self.node_j] += "1"
            G.matrix[self.node_j][d] += "1"

        if self.node_jp != 0:
            G.matrix[d][self.node_jp] += "-1"
            G.matrix[self.node_jp][d] += "-1"

class CCVS(Component):
    def __init__(self, node_j, node_jp, _lambda, node_k, node_kp):
        super().__init__(node_j, node_jp, _lambda)
        self._lambda = _lambda
        self.node_j = node_j
        self.node_jp = node_jp
        self.node_k = node_k
        self.node_kp = node_kp

    def add_to_netlist(self, G: Matrix, C: Matrix, b: Matrix) -> None:
        # For controlling current
        G.extend()
        C.extend()
        b.add_row()
        d = G.n - 1

        # for controlled voltage source's current
        G.extend()
        C.extend()
        b.add_row()
        d2 = G.n - 1

        G.matrix[d2][d] += -self._lambda

        if self.node_j != 0:
            G.matrix[d][self.node_j] += 1
            G.matrix[self.node_j][d] += 1

        if self.node_jp != 0:
            G.matrix[d][self.node_jp] += -1
            G.matrix[self.node_jp][d] += -1

        if self.node_k != 0:
            G.matrix[d2][self.node_k] += 1
            G.matrix[self.node_k][d2] += 1

        if self.node_kp != 0:
            G.matrix[d2][self.node_kp] += -1
            G.matrix[self.node_kp][d2] += -1

class transformer(Component):
    def __init__(self, node_a, node_b, node_c, node_d, L1, L2, M):
        super().__init__(node_a, node_b, M)
        self.node_a = node_a
        self.node_b = node_b
        self.node_c = node_c
        self.node_d = node_d
        self.L1 = L1
        self.L2 = L2
        self.M = M
    
    def add_to_netlist(self, G: Matrix, C: Matrix, b: Matrix):
        # For node A/B transformer coil
        G.extend()
        C.extend()
        b.add_row()
        d = G.n - 1

        # For node C/D transformer coil
        G.extend()
        C.extend()
        b.add_row()
        d2 = G.n - 1

        C.matrix[d][d] += -self.L1
        C.matrix[d][d2] += -self.M
        C.matrix[d2][d] += -self.M
        C.matrix[d2][d2] += -self.L2

        if self.node_a != 0:
            G.matrix[d][self.node_a] += 1
            G.matrix[self.node_a][d] += 1

        if self.node_b != 0:
            G.matrix[d][self.node_b] += -1
            G.matrix[self.node_b][d] += -1

        if self.node_c != 0:
            G.matrix[d2][self.node_c] += 1
            G.matrix[self.node_c][d2] += 1

        if self.node_d != 0:
            G.matrix[d2][self.node_d] += -1
            G.matrix[self.node_d][d2] += -1