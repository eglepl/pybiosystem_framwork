# -*- coding: utf-8 -*-
# ===============================
# AUTHOR: Eglė Plėštytė
#
# CREATE DATE: 2017 - 05 - 10
#
# CLASS NAME: Part
#
# DESCRIPTION: A Part is a process, changing the values of compositors according
# to some rate laws
# ===============================


class Part:

    def __init__(self, name, compositors, rates):
        self.name = name
        self.compositors = compositors
        self.rates = rates
