import random, os, sys, time, numpy, pyglet, textwrap, itertools, csv, ast
from psychopy import visual, core, event, sound, gui

class Experiment():
    
    def __init__(self, ParticipantNumber, Category):
        self.PNum = ParticipantNumber
        self.category = Category
        
 
    
    def Instructions(self, fileName):
        inst = open(fileName, "r") #Instructions are read from Instructions.txt file
        lines = ""
        for line in inst:
            line = line.strip()
            if line is not '':
                lines += line + "\n"
            
        sent = visual.TextStim(expWin, color=txtColor, text=lines, height=30)
        sent.draw()
        expWin.flip()
        event.waitKeys(keyList=["space"]) #The stimuli on the window only change when space key is pressed
        
    def Stimuli(self):
        stimulus1 = visual.Rect(expWin, width=200, height=100, lineWidth=2, lineColor="black", fillColor="red", pos=(-300,0))
        stimulus1.draw()
        stimulus2 = visual.Rect(expWin, width=200, height=100, lineWidth =2, lineColor="black", fillColor="black", pos=(300,0))
        stimulus2.draw()
        expWin.flip()
        event.waitKeys(keyList=["space"])

            
        

bgColor = "grey" #First I determined the background color and text color
txtColor = "black"       
expWin = visual.Window(size=(1366,768),color=bgColor,units="pix") 
expDlg = gui.Dlg(title= "Experiment") #This is a different way to collect initial data such as Participant Id and Trial type
expDlg.addText("Participant Info") #Instead of asking from the console it asks through the window that is opened in a dialogue box
expDlg.addField("Participant ID: ") 
expDlg.addField("Experiment Type :", choices=["Grating", "Other"]) 
PData = expDlg.show()
if not expDlg.OK: #If the participant does not click OK the window closes
    expWin.close()
    
exp = Experiment(PData[0], PData[1])
exp.Instructions("Instructions.txt")
exp.Stimuli()
    

    
expWin.close()
    