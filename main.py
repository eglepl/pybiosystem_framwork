#!/usr/bin/python
# -*- coding: utf-8 -*-
from Biosystem import *
from Part import *
from Rate import *


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

print (T, Y)

# plot the amount of B vs. time
# the second compositor added to the system was for B, so CompositorIndex('B') returns 2
#figure();
#plot(T, Y(:, sys.CompositorIndex('B')));
#xlabel('Time');
#ylabel('Concentration of B');

