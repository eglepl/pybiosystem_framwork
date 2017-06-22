# -*- coding: utf-8 -*-
# ===============================
# AUTHOR: Eglė Plėštytė
#
# CREATE DATE: 2017 - 05 - 10
#
# CLASS NAME: Pulse
#
# DESCRIPTION: A Pulse tells that at time $time we should set value of the
# compositor named $compositor_name to $value in our simulation.
# ===============================


class Pulse:

    def __init__(self, time, compositor_name, value):
        self.time = time
        self.compositor_name = compositor_name
        self.value = value
