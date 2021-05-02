from psychopy import visual, core, event

myWin = visual.Window((1200, 900), color="grey", units="pix")
grating = visual.GratingStim(myWin, units="pix", size=[200, 200], sf = 5.0 / 150.0, ori=135.0, 
                             mask="gauss", contrast=1.0)

grating.draw()

myWin.flip()

event.waitKeys()

myWin.close()