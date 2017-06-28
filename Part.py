# -*- coding: utf-8 -*-

## Representation of a chemical reaction.
#
#  A Part is a process, changing the values of compositors according
#  to some rate laws.
#
#  @author Eglė Plėštytė
#  @date 2017-05-10

class Part:

    ## The constructor
    #  @param self The object pointer.
    #  @param name Name assigned to a Part.
    #  @param compositors Compositors involving chemical reactions.
    #  @param rates Chemical reactions substances change.
    def __init__(self, name, compositors, rates):
        ## Name assigned to a Part.
        self.name = name
        ## Compositors involving chemical reactions.
        self.compositors = compositors
        ## Chemical reactions substances change.
        self.rates = rates
