#!/usr/bin/python
# -*- coding: utf-8 -*-
from Biosystem import *
from Part import *
from Rate import *
from Pulse import *
import matplotlib.pyplot as plt

sys = BioSystem()
sys. addConstant('k', 0.1)
dAdt = sys.addCompositor('A', 10)
dBdt = sys.addCompositor('B', 0)
dEdt = sys.addCompositor('E', 1)

# define and add the part(s)
# this process involves A, B, E
# how this process affects A, B, E
reaction = Part('A + E -k> B + E', [dAdt, dBdt, dEdt], [Rate('-k * A * E'), Rate('k * A * E'), Rate('0')])
sys.addPart(reaction)

T = None
Y = None
# simulate the system from t = 0 to t = 25
# T holds a vector of time and Y is a matrix where each row is a vector of the values of the system variables corresponding to the compositors (in order of addition) for each moment of time in T
#(T, Y) = sys.run([0, 25])

# initial conditions
# spike in some A
# spike in a bit less A
# spike in more A again
# stop the simulation at time 400 with this empty string as the state variable parameter
pulses = []
pulses.append(Pulse(0, 'A', 10))
pulses.append(Pulse(100, 'A', 20))
pulses.append(Pulse(150, 'A', 5))
pulses.append(Pulse(250, 'A', 10))
pulses.append(Pulse(300, '', 0))
(T, Y) = sys.run_pulses(pulses)

#print Y[:, sys.compositorIndex('B')]

# plot the amount of B vs. time
# the second compositor added to the system was for B, so CompositorIndex('B') returns 2
plt.figure()
la = plt.plot(T, Y[:, sys.compositorIndex('A')], label="A")
lb = plt.plot(T, Y[:, sys.compositorIndex('B')], label="B")
le = plt.plot(T, Y[:, sys.compositorIndex('E')], label="E")
plt.legend()
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.show()
