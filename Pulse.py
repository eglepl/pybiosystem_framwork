# -*- coding: utf-8 -*-

## Chemical reaction substance change of concentration at particular time.
#
#  A Pulse tells that at time @p time we should set value of the
#  compositor named @p compositor_name to @p value in our simulation.
#
#  @author Eglė Plėštytė
#  @date 2017-05-10

class Pulse:

    ## The constructor
    #  @param self The object pointer.
    #  @param time The time when to change a concentration of the @p
    #  compositor_name compositor.
    #  @param compositor_name Represents Biosystem compositor.
    #  @param value Compositor @p compositor_name concentration value at @p
    #  time.
    def __init__(self, time, compositor_name, value):
        ## The time when to change a concentration of the @p compositor_name
        #  compositor.
        self.time = time
        ## Compositor name in Biosystem.
        self.compositor_name = compositor_name
        ## Compositor @p compositor_name concentration value at @p time.
        self.value = value
