# -*- coding: utf-8 -*-

## The representation of the rate law.
#
#  A Rate class defines chemical reaction rate formula using a string
#  representation of a rate law involving compositors, constants,
#  and potentially other functions (including of time).
#
#  @author Eglė Plėštytė
#  @date 2017-05-10

class Rate:

    ## The constructor
    #  @param self The object pointer.
    #  @param rate_string Chemical reaction rate formula represented as a string
    def __init__(self, rate_string):
        ## Chemical reaction rate string formula.
        self.rate_string = rate_string

    ## String representation of a rate object
    #  @param self The object pointer.
    #  @return string representation of a rate law
    def __str__(self):
        return self.rate_string