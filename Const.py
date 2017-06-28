# -*- coding: utf-8 -*-

from sympy import Symbol

## A Const is some constant in a system.
#
#  A Const class defines numeric constant in a system.
#
#  @author Eglė Plėštytė
#  @date 2017-05-10

class Const:

    ## The constructor
    #  @param self The object pointer.
    #  @param name Name assigned to a Const.
    #  @param value Value of a constant.
    def __init__(self, name, value=0):
        if(name == 'gamma'):
            raise AssertionError('Don''t name your constants gamma, it''s a reserved keyword')
        ## A name of Const.
        self.name = name
        ## A Symbol with a @p name representing a constant.
        self.sym = Symbol(name)
        ## A value of Const.
        self.value = value
