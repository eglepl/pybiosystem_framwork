# ===============================
# AUTHOR: Eglė Plėštytė
#
# CREATE DATE: 2017 - 05 - 10
#
# CLASS NAME: Const
#
# DESCRIPTION: A Const is some constant in a system
# ===============================


from sympy import Symbol

class Const
    value = 0

    def __init__(self, name, value):
          if(name == 'gamma'):
            raise AssertionError('Don''t name your constants gamma, it''s a reserved keyword')
          self.name = name
          self.sym = Symbol(name)
          self.value = value
