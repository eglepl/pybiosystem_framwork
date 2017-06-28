
from Biosystem import *
from Part import *
from Rate import *
from Pulse import *
import matplotlib.pyplot as plt

sys = BioSystem()
sys.addConstant('k', 0.05)
dAdt = sys.addCompositor('A', 10)
dBdt = sys.addCompositor('B', 0)
dEdt = sys.addCompositor('E', 1)
reaction  = Part(
'A + E -k> B + E',
[dAdt, dBdt, dEdt],
[Rate('-k * A * E'), Rate('k * A * E'), Rate('0')])
sys.addPart(reaction)
T = None
Y = None
(T, Y) = sys.run([0, 25])

# Plot the simulation data
plt.figure()
plt.plot(T, Y[:, sys.compositorIndex('A')], label="A")
plt.plot(T, Y[:, sys.compositorIndex('B')], label="B")
plt.plot(T, Y[:, sys.compositorIndex('E')], label="E")
plt.legend()
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.show()