#!/usr/bin/python
# -*- coding: utf-8 -*-
from Biosystem import *
from Part import *
from Rate import *
from Pulse import *
import matplotlib.pyplot as plt

sys = BioSystem()
sys.addConstant('k', 0.05)
sys.addConstant('m', 0.02)
sys.addConstant('n', 0.07)
sys.addConstant('g', 0.01)

dAdt = sys.addCompositor('A', 10)
dBdt = sys.addCompositor('B', 0)
dEdt = sys.addCompositor('E', 1)
dFdt = sys.addCompositor('F', 0)

# define and add the part(s)
# this process involves A, B, E
# how this process affects A, B, E
reaction  = Part('A + E -k> B + E', [dAdt, dBdt, dEdt, dFdt], [Rate('-k * A * E'), Rate('k * A * E'), Rate('0'), Rate('0')])
reaction2 = Part('A + E  m< B + E', [dAdt, dBdt, dEdt, dFdt], [Rate('m * B * E'), Rate('-m * B * E'), Rate('0'), Rate('0')])
reaction3 = Part('B + E -n> F + E', [dAdt, dBdt, dEdt, dFdt], [Rate('0'), Rate('-n * B * E'), Rate('0'), Rate('n * B * E')])
reaction4 = Part('F + E -g> A + E', [dAdt, dBdt, dEdt, dFdt], [Rate('g * F * E'), Rate('0'), Rate('0'), Rate('-g * F * E')])
sys.addPart(reaction)
sys.addPart(reaction2)
sys.addPart(reaction3)
sys.addPart(reaction4)

T = None
Y = None
# simulate the system from t = 0 to t = 25
# T holds a vector of time and Y is a matrix where each row is a vector of the values of the system variables corresponding to the compositors (in order of addition) for each moment of time in T
#(T, Y) = sys.run([0, 25])

pulses = []
pulses.append(Pulse(0, 'A', 10))    # initial conditions
pulses.append(Pulse(100, 'A', 20))  # spike in some A
pulses.append(Pulse(150, 'A', 0))   # spike in a bit less A
pulses.append(Pulse(250, 'A', 10))  # spike in more A again
pulses.append(Pulse(500, '', 0))    # stop the simulation at time 300 with this empty string as the state variable parameter
(T, Y) = sys.run_pulses(pulses)

#print Y[:, sys.compositorIndex('B')]

# plot the amount of B vs. time
# the second compositor added to the system was for B, so CompositorIndex('B') returns 2
plt.figure()
la = plt.plot(T, Y[:, sys.compositorIndex('A')], label="A")
lb = plt.plot(T, Y[:, sys.compositorIndex('B')], label="B")
le = plt.plot(T, Y[:, sys.compositorIndex('E')], label="E")
le = plt.plot(T, Y[:, sys.compositorIndex('F')], label="F")
plt.legend()
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.show()
