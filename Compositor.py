# ===============================
# AUTHOR: Eglė Plėštytė
#
# CREATE DATE: 2017 - 05 -10
#
# CLASS NAME: Compositor
#
# DESCRIPTION: A Compositor is the total rate of change of a state
# varieble, e.g. the concentration of some chemical species, say dEnzyme/dt
# ===============================

from sympy import Symbol

class  Compositor
    init_value = 0
    value = 0
    rate = '0'

    def __init__(self, name, init_value):
          self.name = name
          self.sym = Symbol(name)
          self.init_value = init_value
          self.value = init_value

    def addRate(self, new_rate):
        self.rate = self.rate + ' + (' + str(new_rate) + ')'
        return self

    def setInitialValue(self, init_value):
        self.init_value = init_value
        return self
