# -*- coding: utf-8 -*-

import numpy as np
from sympy import *
from scipy.integrate import *
from Compositor import Compositor
from Const import Const
import inspect

## Biological system to simulate
#
#  In order to analyze a biological system you create a BioSystem
#  object.
#
#  Biological system might need some constants (Const) and compositors
#  (Compositor). Compositors are the total rates of change of substance state
#  variables.
#
#  Then parts (Part) are declared and added to a system. Part is a process in
#  a system (reaction) that affect some state variables by changing their
#  value  according to a rate law (Rate).
#
#  Then a simulation can be started.
#
#  Example:
#
#  @code
#
# from Biosystem import *
# from Part import *
# from Rate import *
# from Pulse import *
# import matplotlib.pyplot as plt
#
# sys = BioSystem()
# sys.addConstant('k', 0.05)
# dAdt = sys.addCompositor('A', 10)
# dBdt = sys.addCompositor('B', 0)
# dEdt = sys.addCompositor('E', 1)
# reaction  = Part(
# 'A + E -k> B + E',
# [dAdt, dBdt, dEdt],
# [Rate('-k * A * E'), Rate('k * A * E'), Rate('0')])
# sys.addPart(reaction)
# T = None
# Y = None
# (T, Y) = sys.run([0, 25])
#
# # Plot the simulation data
# plt.figure()
# plt.plot(T, Y[:, sys.compositorIndex('A')], label="A")
# plt.plot(T, Y[:, sys.compositorIndex('B')], label="B")
# plt.plot(T, Y[:, sys.compositorIndex('E')], label="E")
# plt.legend()
# plt.xlabel('Time')
# plt.ylabel('Concentration')
# plt.show()
#
#  @endcode
#
#  @author Eglė Plėštytė
#  @date 2017-06-15

class BioSystem:

    ## The constructor
    #  @param self The object pointer.
    #  @param compositors Compositors involving chemical reactions.
    #  @param constants Constants of a Biosystem.
    #  @param symbols A Symbol with a @p name representing a substance.
    def __init__(self):
        ## Parts in a Biosystem.
        self.parts = []
        ## Compositors involving chemical reactions.
        self.compositors = []
        ## Constants in a Biosystem.
        self.constants = []
        ## List of all the Compositor symbols in ths BioSystem
        #  by initializing symbols with t we allow t to be a variable of
        #  time that's not a Compositor or Constant.
        self.symbols = ['t']
        ## A mapping between constant name and its index in @p constants list.
        self.map_constants = {}
        ## A mapping between compositor name and its index in @p constants list.
        self.map_compositors = {}
        ## Flag if function determine_rates was called.
        #  If False we need to call determine_rates again.
        self.rates_determined = False

    ## Create or add a compositor to the system
    #  @param self The object pointer.
    #  @param compositor_or_name
    #     Compositor object to add if @p init_value == None,
    #     else Compositor name to add with an @p init_value.
    #
    #  @param init_value Initial value of a Compositor or None.
    #  @return The Compositor object that was added.
    def addCompositor(self, compositor_or_name, init_value=None):
        new_compositor = None
        if init_value == None:
            new_compositor = compositor_or_name
        else:
            name = compositor_or_name
            new_compositor = Compositor(name, init_value)
        self.compositors.append(new_compositor)
        self.map_compositors[new_compositor.name] = len(self.compositors) - 1
        self.symbols.append(new_compositor.sym)
        return new_compositor

    ## Get compositor index in the @p compositors with name @p name.
    #  @param self The object pointer.
    #  @param name Existing compositor name.
    #  @return the index of a compositor in the system.
    def compositorIndex(self, name):
        index = self.map_compositors.get(name)
        return index

    ## Add a part to the system.
    #  @param self The object pointer.
    #  @param new_part Part object to add.
    #  @return Current system object pointer.
    def addPart(self, new_part):
        self.parts.append(new_part)
        return self

    ## Create or add a Constant to the system
    #  @param self The object pointer.
    #  @param constant_or_name
    #    Constant object to add if @p init_value == None,
    #    else Constant name to add with an @p init_value.
    #
    #  @param init_value Initial value of a Constant or None.
    #  @return The Constant object that was added.
    def addConstant(self, constant_or_name, init_value):
        new_constant = None
        if init_value == None:
            new_constant = constant_or_name
        else:
            new_constant = Const(constant_or_name, init_value)
        self.constants.append(new_constant)
        self.map_constants[new_constant.name] = len(self.constants) - 1
        return new_constant

    ## Determine rates of all compositors unless already determined.
    #  @param self The object pointer.
    #  @return None.
    def determine_rates(self):
        if not self.rates_determined:
            for i in self.parts:
                p = i
                for k in range(0, len(p.compositors)):
                    p.compositors[k].addRate(p.rates[k])
            for k in self.compositors:
                ## All Constant symbols.
                constant_syms = list( map( (lambda c: c.sym), self.constants))
                ## All Constant values.
                constant_vals = list( map( (lambda c: c.value), self.constants))
                ## Pairs of symbols and its value.
                substitutions = zip(constant_syms, constant_vals)
                ## Convert Compositor rate string/formula to sympy expression
                #  and substitute all constants with its values.
                symexpr = sympify(k.rate).subs(substitutions)
                ## Convert sympy expression to python function with arguments:
                #  time, compositor1_name, compositor2_name, ...
                k.ratef = lambdify(self.symbols, symexpr)
            self.rates_determined = True
        return None

    ## Reset all Compositor rates to '0'.
    #  @param self The object pointer.
    #  @return None.
    def reset_rates(self):
        self.rates_determined = False
        for i in self.compositors:
            i.rate = '0'
            i.ratef = None
        return None

    ## Set Constant value by Constant name.
    #  @param self The object pointer.
    #  @param name The name of existing Constant.
    #  @param value New value of the Constant.
    #  @return None.
    def changeConstantValue(self, name, value):
        self.constants[self.map_constants[name]].value = value
        self.reset_rates()
        return None

    ## Set Compositor value and initial value by a Compositor name.
    #  @param self The object pointer.
    #  @param name The name of existing Compositor.
    #  @param value New value of the Compositor @p initial_value and Compositor
    #  @p value.
    #  @return None.
    def changeInitialValue(self, name, value):
        compositor = self.compositors[self.map_compositors[name]]
        compositor.setInitialValue(value)
        compositor.value = value
        return None

    ## Reset all Compositor values to its initial value.
    #  @param self The object pointer.
    #  @return None.
    def reset_state_variables(self):
        for i in self.compositors:
            i.value = i.init_value
        return None

    ## Run a simulation of the Biosystem.
    #  @param self The object pointer.
    #  @param tspan Time interval to simulate, for example [t0, t1].
    #  @return Tuple (T, Y), where T - time point list, Y - matrix consisting
    #  of Compositor values at a time points.
    def run(self, tspan):
        self.determine_rates()
        y0 = []
        for c in self.compositors:
            y0.append(c.value)
        delta = max(int(tspan[1] - tspan[0]) * 17, 1000);
        t = np.linspace(tspan[0], tspan[1], delta)
        y = odeint(self.sys_ode, y0, t)
        return (t, y)

    ## Ordinary diferential equatation of the system.
    #  @param self The object pointer.
    #  @param y System compositors values.
    #  @param t Time point.
    #  @return change of Compositor values.
    def sys_ode(self, y, t):
        dy = np.zeros(len(y))

        for i in range(0, len(self.compositors)):
            k = self.compositors[i]
            arg = [t] + list(y) # Add time component to y
            dy[i] = k.ratef(*arg) # list as arguments for function
        return dy

    ## Run simulation given pulse list. Last pulse is not simulated.
    #  Each pulse defines time, Compositor, Compositor value to set at
    #  provided time.
    #
    #  When the Pulse time comes Pulse defined Compositor is set to value
    #  provided. Normal simulation is carried on till next Pulse. While
    #  there is next Pulse - action repeats.
    #
    #  First Pulse should start at t = 0 time.
    #  Each next Pulse time should be greater than previous.
    #  Last Pulse is not simulated - it is a stop time.
    #
    #  Example:
    #
    #  @code
    #
    # from Biosystem import *
    # from Part import *
    # from Rate import *
    # from Pulse import *
    # import matplotlib.pyplot as plt
    #
    # sys = BioSystem()
    # sys.addConstant('k', 0.05)
    # dAdt = sys.addCompositor('A', 10)
    # dBdt = sys.addCompositor('B', 0)
    # dEdt = sys.addCompositor('E', 1)
    # reaction  = Part(
    # 'A + E -k> B + E',
    # [dAdt, dBdt, dEdt],
    # [Rate('-k * A * E'), Rate('k * A * E'), Rate('0')])
    # sys.addPart(reaction)
    # T = None
    # Y = None
    #
    # pulses = []
    #
    # # initial condition
    # pulses.append(Pulse(0, 'A', 10))
    #
    # # spike in some A
    # pulses.append(Pulse(100, 'A', 20))
    #
    # # spike in a bit less A
    # pulses.append(Pulse(150, 'A', 5))
    #
    # # spike in more A again
    # pulses.append(Pulse(250, 'A', 10))
    #
    # # stop the simulation at time 500 with this empty string as the state
    # # variable parameter
    # pulses.append(Pulse(500, '', 0))
    #
    # # Run pulsed simulation
    # (T, Y) = sys.run_pulses(pulses)
    #
    # # Plot the simulation data
    # plt.figure()
    # plt.plot(T, Y[:, sys.compositorIndex('A')], label="A")
    # plt.plot(T, Y[:, sys.compositorIndex('B')], label="B")
    # plt.plot(T, Y[:, sys.compositorIndex('E')], label="E")
    # plt.legend()
    # plt.xlabel('Time')
    # plt.ylabel('Concentration')
    # plt.show()
    #
    #  @endcode
    #
    #  @param self The object pointer.
    #  @param pulse_series List of pulse objects.
    #  @return Tuple (T, Y), where T - time point list, Y - matrix consisting
    #  of Compositor values at a time points.

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

    ## Find the index in T (time point) list that gives a value just before t
    #  or exact t.
    #  @param ignore Ignored argument.
    #  @param T A list of time points.
    #  @param t Time.
    #  @return Index of T just before t (or exact t).
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

    ## Given two (x, y) traces, interpolate the less dense one to
    #  have values for each x-value in the denser trace.
    #  iX1, iY1 form one trace; iX2, iY2 another. The "denser" trace (more
    #  datapoints) is used as the basis. Suppose the first is the denser
    #  trace. Then for each value of iX1, we find a linear fit of the second
    #  trace at that value using the two closest values of iX2.
    #  iX1, iX2 are assumed to be ordered and to both start at the same
    #  value. Assume iY1, iY2 are columns, iX1, iX2 are rows.
    #  @param ignore Ignored argument.
    #  @param iX1 List of X values in first trace.
    #  @param iY1 List of Y values in first trace.
    #  @param iX2 List of X values in second trace.
    #  @param iY2 List of Y values in second trace.
    #  @return Tuple matched and interpolated traces.
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
        return (x1, y1, x2, y2)
        return (x1, y1, x2, y2)
