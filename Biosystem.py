# -*- coding: utf-8 -*-

import numpy as np
from sympy import *
from scipy.integrate import *
from Compositor import Compositor
from Const import Const
import inspect

class BioSystem:

    parts = []
    compositors = []
    constants = []
    symbols = ['t']
    rates_determined = False

    def __init__(self):
        self.map_compositors = {}
        self.map_constants = {}

    def addCompositor(self, compositor, init_value=None):
        new_compositor = None
        if init_value == None:
            new_compositor = compositor
        else:
            name = compositor
            new_compositor = Compositor(name, init_value)
        self.compositors.append(new_compositor)
        self.map_compositors[new_compositor.name] = len(self.compositors) - 1
        self.symbols.append(new_compositor.sym)
        return new_compositor

    def compositorIndex(self, name):
        index = self.map_compositors.get(name)
        return index

    def addPart(self, new_part):
        self.parts.append(new_part)
        return self

    def addConstant(self, constant, init_value):
        new_constant = None
        if init_value == None:
            new_constant = constant
        else:
            new_constant = Const(constant, init_value)
        self.constants.append(new_constant)
        self.map_constants[new_constant.name] = len(self.constants) - 1
        return new_constant

    def determine_rates(self):
        if not self.rates_determined:
            for i in self.parts:
                p = i
                for k in range(0, len(p.compositors)):
                    p.compositors[k].addRate(p.rates[k])
            for k in self.compositors:
                constant_syms = list( map( (lambda c: c.sym), self.constants))
                constant_vals = list( map( (lambda c: c.value), self.constants))
                substitutions = zip(constant_syms, constant_vals);
                symexpr = sympify(k.rate).subs(substitutions)
                k.ratef = lambdify(self.symbols, symexpr)
            self.rates_determined = True
        return None

    def reset_rates(self):
        self.rates_determined = False
        for i in self.compositors:
            i.rate = '0'
            i.ratef = None
        return None

    def changeConstantValue(self, name, value):
        self.constants[self.map_constants[name]].value = value
        self.reset_rates()
        return None

    def changeInitialValue(self, name, value):
        compositor = self.compositors[self.map_compositors[name]]
        compositor.setInitialValue(value)
        compositor.value = value
        return None

    def reset_state_variables(self):
        for i in self.compositors:
            i.value = i.init_value
        return None


    def run(self, tspan):
        self.determine_rates()
        y0 = []
        for c in self.compositors:
            y0.append(c.value)
        t = np.linspace(tspan[0], tspan[1], int(tspan[1] - tspan[0]) * 17)
        #TODO: missing args for odeint from this function arguments
        y = odeint(self.sys_ode, y0, t)
        return (t, y)

    def sys_ode(self, y, t):
        dy = np.zeros(len(y))
        #TODO: find out what is cellarray
        # cellarray = num2cell(y);
        cellarray = None
        for i in range(0, len(self.compositors)):
            k = self.compositors[i]
            arg = [t] + list(y)
            dy[i] = k.ratef(*arg) # list as arguments
        return dy

    def run_pulses(self, pulse_series):
        num_pulses = len(pulse_series)

        T = []
        Y = []

        prev_start = 0
        prev_end = 0

        for i in range(0, num_pulses - 1):
            pulse = pulse_series[i]
            if pulse.compositor_name:
                self.compositors[self.map_compositors[pulse.compositor_name]].value = pulse.value

            sim_length = pulse_series[i+1].time - pulse.time
            tspan = [prev_end, prev_end + sim_length]
            (T_sim, Y_sim) = self.run(tspan)


            T = T + list(T_sim[2:])
            if(len(Y) > 0):
                Y = np.concatenate((Y, Y_sim[2:]))
            else:
                Y = Y_sim[2:]

            prev_start = pulse.time
            prev_end = prev_start + sim_length

            for j in range(0, len(self.compositors)):
                self.compositors[j].value = Y_sim[-1][j]

        self.reset_state_variables()
        return (T, Y)

    def time_to_index(ignore, T, t):
        i = 0
        while i < len(T):
            if T[i] >= t:
                break
            i = i + 1
        if T[i] == t:
            ix = i
        else:
            ix = i - 1
        return [ ix ]

    def interpolate_traces(ignore, iX1, iY1, iX2, iY2):
        X1 = iX2
        Y1 = iY2
        X2 = iX1
        Y2 = iY1
        swap = True
        if len(iX1) > len(iX2):
            X1 = iX1
            Y1 = iY1
            X2 = iX2
            Y2 = iY2
            swap = False

        interpolated = np.zeros(len(X1))
        max_j = len(X2) - 1
        j = 0
        for i in range(0, len(X1)):
            x1 = X1[i]
            x_diff = abs(x1 - X2[j])
            while (j < max_j - 1) and (abs(x1 - X2[j+1]) < x_diff):
                x_diff = min(x_diff, abs(x1 - X2[j+1]))
                j = j + 1

            x2 = X2[j]

            a = X2[j]
            b = Y2[j]
            c = X2[j + 1]
            d = Y2[j + 1]
            if x1 < x2 and j > 1:
                a = X2[j - 1]
                b = Y2[j - 1]
                c = X2[j]
                d = Y2[j]

            if (a - c) == 0:
                A = 0
            else:
                A = (b - d) / (a - c)

            B = b - A * a
            interpolated[i] = A *x1 + B

        x1 = X1
        y1 = Y1
        x2 = X1
        y2 = interpolated
        if swap:
            x1 = X1
            y1 = interpolated
            x2 = X1
            y2 = Y1
        return [x1, y1, x2, y2]
