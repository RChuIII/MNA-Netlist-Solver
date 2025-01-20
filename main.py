from src import matrix as m
from src import components as c

G = m.Matrix(4,4)
C = m.Matrix(4,4)
b = m.Matrix(4,1)

I1 = c.CurrentSource(0,1,1)
L1 = c.Inductor(1,0,0.799e-9)
C1 = c.Capacitor(1,0,0.319e-6)
C2 = c.Capacitor(2,3,63.72e-12)
C3 = c.Capacitor(3,0,0.319e-6)
R1 = c.Resistor(1,0,5)
R2 = c.Resistor(1,2,5)
R3 = c.Resistor(3,0,5)
R4 = c.Resistor(3,4,5)
R5 = c.Resistor(4,0,1e3)

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