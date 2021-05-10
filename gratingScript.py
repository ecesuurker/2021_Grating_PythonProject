from psychopy import visual, core, event
import numpy
g1 = numpy.linspace(0.03,0.04,4)
g2 = numpy.linspace(0.035,0,045,4)

myWin = visual.Window((1200, 900), color="grey", units="pix")
grating = visual.GratingStim(myWin, units="pix", size=[200, 200], sf = 0.04, ori=53, 
                             mask="gauss", contrast=1.0)

grating.draw()

myWin.flip()

event.waitKeys()

myWin.close()