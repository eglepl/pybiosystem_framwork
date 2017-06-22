# -*- coding: utf-8 -*-
# ===============================
# AUTHOR: Eglė Plėštytė
#
# CREATE DATE: 2017 - 05 - 10
#
# CLASS NAME: Rate
#
# DESCRIPTION: A Rate is a string representation of a rate law involving
# compositors, constants, and potentially other functions (including of time).
# ===============================


class Rate:

    def __init__(self, rate_string):
        self.rate_string = rate_string
