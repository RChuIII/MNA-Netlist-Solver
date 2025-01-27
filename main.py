from src import matrix as m
from src import components as c

G = m.Matrix(3,3, symbolic=True)
C = m.Matrix(3,3, symbolic=True)
b = m.Matrix(3,1, symbolic=True)

# I1 = c.CurrentSource(0,1,1)
# L1 = c.Inductor(1,0,0.799e-9)
# C1 = c.Capacitor(1,0,0.319e-6)
# C2 = c.Capacitor(2,3,63.72e-12)
# C3 = c.Capacitor(3,0,0.319e-6)
# R1 = c.Resistor(1,0,5)
# R2 = c.Resistor(1,2,5)
# R3 = c.Resistor(3,0,5)
# R4 = c.Resistor(3,4,5)
# R5 = c.Resistor(4,0,1e3)

# I1.add_to_netlist(b)
# L1.add_to_netlist(G, C, b)
# C1.add_to_netlist(C)
# C2.add_to_netlist(C)
# C3.add_to_netlist(C)
# R1.add_to_netlist(G)
# R2.add_to_netlist(G)
# R3.add_to_netlist(G)
# R4.add_to_netlist(G)
# R5.add_to_netlist(G)
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
# J1 = c.CurrentSource(0, 1, 1e-3)
# R1 = c.Resistor(1, 0, 1.2e3)
# C1 = c.Capacitor(1, 0, 10e-9)
# R2 = c.Resistor(1, 2, 1.01e3)
# L1 = c.Inductor(1, 2, 2e-9)
# C2 = c.Capacitor(2, 0, 20e-9)
# R3 = c.Resistor(2, 3, 1.14e3)
# L2 = c.Inductor(2, 3, 3e-9)
# C3 = c.Capacitor(3, 0, 20e-9)
# R4 = c.Resistor(3, 4, 1.45e3)
# C4 = c.Capacitor(3, 4, 10e-9)
# L3 = c.Inductor(3, 4, 3e-9)
# C5 = c.Capacitor(4, 0, 10e-9)
# R5 = c.Resistor(4, 0, 1.54e3)

# J1.add_to_netlist(b)

# R1.add_to_netlist(G)
# R2.add_to_netlist(G)
# R3.add_to_netlist(G)
# R4.add_to_netlist(G)
# R5.add_to_netlist(G)

# C1.add_to_netlist(C)
# C2.add_to_netlist(C)
# C3.add_to_netlist(C)
# C4.add_to_netlist(C)
# C5.add_to_netlist(C)

# L1.add_to_netlist(G, C, b)
# L2.add_to_netlist(G, C, b)
# L3.add_to_netlist(G, C, b)
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
J1 = c.CurrentSource(0, 1, "I1")
R1 = c.Resistor(1, 0, "g1")
VCCS1 = c.VCCS(1, 3, "gm", 1, 2)
C1 = c.Capacitor(2, 0, "C1")
R2 = c.Resistor(2, 3, "g2")
C2 = c.Capacitor(3, 0, "C2")

J1.add_to_netlist(b)
R1.add_to_netlist(G)
VCCS1.add_to_netlist(G)
C1.add_to_netlist(C)
R2.add_to_netlist(G)
C2.add_to_netlist(C)

print(G)
print()
print(C)
print()
print(b)