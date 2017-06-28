# -*- coding: utf-8 -*-

from sympy import Symbol

## Substance concentration.
#
#  A Compositor is the total rate of change of a state
#  variable, e.g. the concentration of some chemical substances, say dEnzyme/dt.
#
#  @author Eglė Plėštytė
#  @date 2017-05-10

class Compositor:

    ## The constructor
    #  @param self The object pointer.
    #  @param name Name assigned to a Compositor (Substance name).
    #  @param init_value Initial concentration of a substance.
    def __init__(self, name, init_value = 0):
        ## Rate formula of the compositor.
        self.rate = '0'
        ## Substance name in a system.
        self.name = name
        ## A Symbol with a @p name representing a substance.
        self.sym = Symbol(name)
        ## Initial concentration of a substance.
        self.init_value = init_value
        ## Current concentration of a substance.
        self.value = init_value

    ## Add new rate represented as a string.
    #  @param self The object pointer.
    #  @param new_rate Rate to add.
    #  @return The object pointer.
    def addRate(self, new_rate):
        self.rate = self.rate + ' + (' + str(new_rate) + ')'
        return self

    ## Set initial concentration.
    #  @param self The object pointer.
    #  @param init_value Initial concentration of a substance.
    #  @return The object pointer.
    def setInitialValue(self, init_value):
        self.init_value = init_value
        return self
