import random, os, sys, time, numpy, pyglet, textwrap, itertools, csv, ast
from psychopy import visual, core, event, sound, gui

class Experiment():
    
    def __init__(self, ParticipantNumber, Category):
        self.PNum = ParticipantNumber
        self.category = Category
        self.trialType = random.randint(1, 2)
        fileName = ParticipantNumber + "_" + Category + "TT" + str(self.trialType) + ".csv"
        self.data = open(fileName, "w")
        trialFile = "TrialType" + str(self.trialType) + ".txt"
        self.trialFileName = open(trialFile, "r", newline=None)
    
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
        
    def Run(self):
        trials = csv.DictReader(self.trialFileName, delimiter="\t") #Reads the trial structure, the sizes of rectangles etc.
        dataFile = csv.DictWriter(self.data, fieldnames=["RT","KeyPress"]) #This is the data file that the participant data will be written
        dataFile.writeheader()
        for trial in trials:
            for i in range(int(trial["TrialNumber"])): #Determines how many trials each block have
                sizes = [int(trial["WidthofStimulus1"]), int(trial["WidthofStimulus2"])]
                random.shuffle(sizes) #This is for randomizing the presentation side of each stimulus
                timeFrame = core.StaticPeriod(win=expWin) #To determine time period for each trial
                timeFrame.start(0.5)
                stimulus1 = visual.Rect(expWin, height=100, width=sizes[0], lineWidth=2, lineColor="black", fillColor="red", pos=(-300,0))
                stimulus1.draw() #Stimuli presentations
                stimulus2 = visual.Rect(expWin, height=100, width=sizes[1], lineWidth =2, lineColor="black", fillColor="black", pos=(300,0))
                stimulus2.draw()
                if "," in trial["Names"]: #If two stimuli that belong to different categories are presented both of their category name is presented
                    name1 = trial["Names"][1:trial["Names"].find(",")] #Extracting names of categories from the file
                    name2 = trial["Names"][trial["Names"].find(",")+1:-1]
                    if sizes[0] != int(trial["WidthofStimulus1"]): 
                        name1, name2 = name2, name1 #Determines whether shuffling change the order, if it did it changes category names as well
                    
                    disp1 = visual.TextStim(expWin, color=txtColor, text=name1, pos=(-300,-100))
                    disp2 = visual.TextStim(expWin, color=txtColor, text=name2, pos= (300, -100))
                    disp1.draw() #Category names are displayed
                    disp2.draw()

                        
                else:
                    disp = visual.TextStim(expWin, color=txtColor, text=trial["Names"], pos=(0,-100))
                    disp.draw() 
                        
                expWin.flip()
                timeFrame.complete()
                

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
exp.Run()
    

    
expWin.close()
    