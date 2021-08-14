import csv
import random
from psychopy import visual, core, event
from ast import literal_eval


class Experiment(object):


    def __init__(self, participantNo, cbList, sessionNo, fps=60.0):
        self.fps = fps
        # set up file paths, etc.
        #self.trials_fname = 'trial_structure/Colors_trials.txt'
        #self.trials_fname = 'trial_structure/Colors_trials_simple.txt'
        self.log_fname = 'logs/' + str(cbList) + '_' + str(participantNo) + "_s" + str(sessionNo) + '.csv'
        self.cbList = cbList
        self.sNo = sessionNo
        variableFile = open("trial_structure/CounterbalanceVariables.txt", "r")
        counterbalance = csv.DictReader(variableFile, delimiter="\t")
        for row in counterbalance: #It reads out the trial file and assigns the variables
            if row["List_Number"] == str(cbList):
                self.angles = row["Angles"].split(" ") #split() function splits strings into list elements according to the delimeter
                self.label1 = row["Label1"]
                self.label2 = row["Label2"]
                self.sameKey = row["Same_key"]
                self.diffKey = row["Diff_key"]
                self.transferOrder = row["Transfer_Task_Order"]
                self.frequency = row["Grating_Frequency"].split(" ")
        log_file = open(self.log_fname, "w", newline="")
        log_fields = ['cbList','type', 'grating1_angle', 'grating1_freq', 'grating2_angle', 'grating2_freq','keypress', 'RT', 'ACC', 't']
        self.log = csv.DictWriter(log_file, fieldnames=log_fields)
        self.log.writeheader()
        ins = open("instructions/Instructions.csv", "r")
        i = csv.DictReader(ins)
        self.instructions = {} #reads instructions into a dictionary in which keys are the type of the instruction
        for r in i:
            self.instructions[r["Type"]] = r["Dutch"].replace("<<same>>", self.sameKey).replace("<<diff>>", self.diffKey)
        

    def run(self):
        # set up presentation window color, and size
        bgcolor = 'grey'
        txtcolor = 'white' 
        #self.win = visual.Window(fullscr=True, color=bgcolor, units='pix')
        self.win = visual.Window((1200, 900), color=bgcolor, units='pix')  # temporary presentation window setup, exchange for line above when running actual experiment

        # set up timing related stuff
        self.frame_dur = 1.0 / self.fps
        self.clock = core.Clock()  # trial timer
        self.expclock = core.Clock()  # whole experiment timer
        # inter trial interval setup
        self.isi = core.StaticPeriod()
        #self.isi.start(.5)

        # various stimulus presentation boxes for text and images
        self.word1 = visual.TextStim(self.win, color=txtcolor, height=30, wrapWidth = 900)
        self.word2 = visual.TextStim(self.win, color=txtcolor, height=30, wrapWidth = 900)
        self.title = visual.TextStim(self.win, pos=(0, 200), color=txtcolor, height=30, wrapWidth = 900)
        self.fixation = visual.ShapeStim(self.win, 
            vertices=((0, -15), (0, 15), (0,0), (-15,0), (15, 0)),
            lineWidth=5,
            pos=[0,0],
            closeShape=False,
            lineColor="black")
        self.image_l = visual.ImageStim(self.win, pos=(0, 0), size=[300,300])
        self.grating = visual.GratingStim(self.win, units="pix", size=[200, 200], mask="gauss", contrast=1.0)
        
        self.sessions(self.sNo)
        #I created a template grating similar to other shapes so that we can use it and manipulate only necessary things in the code below

        # actually run the experiment routines
        #with open(self.trials_fname, 'r') as trial_file, open(self.log_fname, 'w', newline='') as log_file:
        
        
            # read trial structure
            #trials = csv.DictReader(trial_file, delimiter='\t')

            # set up log file
        
        """   
            blocks = {}
            for trial in trials:
                if trial['block'] not in blocks.keys():
                    blocks[trial['block']] = [trial]
                else:
                    blocks[trial['block']].append(trial)
                    
            for block_number in sorted(blocks.keys()):
                trials = blocks[block_number]
                #if trials[0]['randomize'] == 'yes':
                 #   random.shuffle(trials)
                for trial in trials:
                    self.clock.reset()  # reset trial clock
                    trial = self.present_trial(trial)  # present the trial
                    log.writerow(trial)  # log the trial data


    # select the appriopriate trial subroutine
    def present_trial(self, trial):
        tType = trial['type']
        if tType == 'instructions':
            trial = self.instruction_trial(trial)
        elif tType == 'categorization':
            trial = self.categorization_trial(trial)
        elif tType == 'memory':
            trial = self.memory_trial(trial)
        else:
            # unknown trial type, return some kind of error?
            print('ERROR: unknown trial type')

        # log experiment timer and return trial data
        trial['t'] = self.expclock.getTime()
        return trial


    def instruction_trial(self, trial):
        # present instruction trial
        self.isi.start(.5)
        self.title.text = trial['title']
        self.title.draw()
        self.word1.text = trial['content'].replace('<br>', '\n')
        self.word1.draw()
        self.win.callOnFlip(self.clock.reset)
        self.isi.complete()
        self.win.flip()
        keys = event.waitKeys(keyList=['escape'] + trial['button1'].split(' '), timeStamped=self.clock)
        trial['keypress'], trial['RT'] = keys[0]
        if trial['keypress'] == 'escape':
            core.quit()
        #self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial
    """
    def categorization_trial(self, bNumber):
        self.instr("get ready")
        for i in range(bNumber): #determines for how many blocks the task runs
            ang = [0,1,2,3]#*24 #These are index values for angles. They indicate index number of the angle to be represented
            #adjusted the number of trials in a block
            random.shuffle(ang)
            for a in ang:
                self.clock.reset()
                trial = {}
                trial["cbList"] = self.cbList
                trial["type"] = "categorization"
                self.isi.start(.5)
                self.fixation.draw()
                self.win.flip()
                #core.wait(.5)
                self.isi.complete()
                trial["grating1_angle"], trial["grating1_freq"] = self.drawing(a)
                self.word1.text = self.label1
                self.word2.text = self.label2
                positions = [(-200,-200),(200,-200)] #Positions for the labels. I shuffle them so every trial they appear in random side
                random.shuffle(positions)
                self.word1.pos = positions[0]
                self.word2.pos = positions[1]
                self.word1.draw()
                self.word2.draw()
                self.win.flip()
                keys = event.waitKeys(keyList=['escape'] + [self.sameKey] + [self.diffKey], timeStamped=self.clock)
                trial['keypress'], trial['RT'] = keys[0]
                if trial['keypress'] == 'escape':
                    core.quit()
                if keys[0][0] == "a":
                    if a < 2 and positions[0] == (-200,-200):
                        trial['ACC'] = 1
                        self.feedback(1)
                    elif a > 1 and positions[1] == (-200,-200):
                        trial['ACC'] = 1
                        self.feedback(1)
                    else:
                        trial['ACC'] = 0
                        self.feedback(0)
                else:
                    if a < 2 and positions[0] == (200,-200):
                        trial['ACC'] = 1
                        self.feedback(1)
                    elif a > 1 and positions[1] == (200,-200):
                        trial['ACC'] = 1
                        self.feedback(1)
                    else:
                        trial['ACC'] = 0
                        self.feedback(0)
                trial['t'] = self.expclock.getTime()
                self.log.writerow(trial)
            if i != bNumber - 1:
                self.instr("Break") #break instruction is not displayed at the end of tasks
            #This accuracy code basically accepts an answer as accurate if the person pressed the left/right button and the appropriate word
            #was presented in left/right
            #self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
            self.win.flip()
        self.instr("Next task")
        return None

    def discrimination_trial(self, transfer="No"):
        self.instr("get ready")
        for i in range(2): #since there is a break in the middle of the task, I have written the code as two parts with a loop
            comparison = [[0,0],[1,1],[2,2],[3,3],[0,1],[1,2],[2,3]]  #These are indexes for the two angles that will be compared
            #comparison = comparison * 7
            #del comparison[random.randint(0,49)]
            random.shuffle(comparison)
            for t in comparison:
                self.clock.reset()
                trial = {}
                trial["cbList"] = self.cbList
                if transfer == "No":
                    trial["type"] = "discrimination"
                else:
                    trial["type"] = "discrimination_transfer"
                random.shuffle(t) #It shuffles the angles that will be compared so that everytime they appear in random order
                self.isi.start(.5)
                self.fixation.draw()
                self.win.flip()
                self.isi.complete()
                #core.wait(.5)
                self.isi.start(1)
                trial["grating1_angle"], trial["grating1_freq"] = self.drawing(t[0], transfer=transfer)
                self.win.flip()
                self.isi.complete()
                #core.wait(1)
                self.isi.start(.5)
                self.fixation.draw()
                self.win.flip()
                self.isi.complete()
                #core.wait(.5)
                self.isi.start(1)
                trial["grating2_angle"], trial["grating2_freq"] = self.drawing(t[1],transfer=transfer)
                self.win.flip()
                self.isi.complete()
                #core.wait(1)
                self.word1.text = "zelfde/anders"
                self.word1.pos = (0,0)
                self.word1.draw()
                self.win.callOnFlip(self.clock.reset)
                #self.isi.complete()
                self.win.flip()
                keys = event.waitKeys(keyList=['escape'] + [self.sameKey] + [self.diffKey], timeStamped=self.clock)
                trial['keypress'], trial['RT'] = keys[0]
                if trial['keypress'] == 'escape':
                    core.quit()
                if trial['keypress'] == self.sameKey and t[0] != t[1] or trial["keypress"] == self.diffKey and t[0] == t[1]:
                #This statement basically states that if the participants hit the key for same stimuli but they are different or hit different but they are the same, give accuracy zero
                    trial['ACC'] = 0
                # self.feedback(1)
                else:
                    trial['ACC'] = 1
                trial['t'] = self.expclock.getTime()
                self.log.writerow(trial)
            if i == 0:
                self.instr("Break")
            # self.feedback(0)
            #self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
            # flip buffer again and start ISI timer
            self.win.flip()
        self.instr("Next task")
        return None
    
    def drawing(self, angle, transfer="No"):
        ang = float(self.angles[angle])
        if transfer == "Yes":
            ang = ang + 90
            self.grating.ori = literal_eval(str(ang))
        else:
            self.grating.ori = literal_eval(str(ang))
        freq = random.choice(self.frequency)
        self.grating.sf = literal_eval(freq) #Randomly picks a frequency
        self.grating.draw()
        return ang, freq
  
    def feedback(self, accuracy):
        i = random.randint(1, 3)
        if int(accuracy) == 1:
            imgnameBeg = "Correct"
            titleText = "Well done!"
            word1Text = "Correct answer"
            FileExt = ".jpg"
        else:
            imgnameBeg = "Incorrect"
            titleText = "Sorry!"
            word1Text = "Wrong answer"
            FileExt = ".png"
        imgname = imgnameBeg + str(i) + FileExt
        self.image_l.image = imgname
        self.image_l.draw()
        self.title.text = titleText
        self.title.draw()
        self.word1.text = word1Text
        self.word1.pos = (0, -200)
        self.word1.draw()
        self.win.flip()
        core.wait(.5)
        return None
    
    def sessions(self, sNo): #a function for calling task functions according to the sessions and display instructions
        if int(sNo) == 1:
            self.instr("Initial intro")
            self.instr("Intro session1")
            self.instr("detailed instructions1")
            if int(self.transferOrder) == 1:
                self.discrimination_trial()
                self.discrimination_trial(transfer="Yes")
            else:
                self.discrimination_trial(transfer="Yes")
                self.discrimination_trial()
            self.instr("detailed instructions2")
            self.categorization_trial(2)
        elif int(sNo) == 2 or int(sNo) == 4:
            i = "welcome back" + str(sNo)
            self.instr(i)
            self.categorization_trial(10)
        elif int(sNo) == 3:
            self.instr("welcome back3")
            self.categorization_trial(4)
            self.discrimination_trial()
        elif int(sNo) == 5:
            self.instr("welcome back5")
            self.categorization_trial(4)
            self.discrimination_trial()
            self.discrimination_trial(transfer="Yes")
        self.win.close()
        return None
    
    def instr(self,instructions): #a function that displays instructions according to the type of the instruction
        self.word1.text = self.instructions[instructions]
        self.word1.pos = (0,50)
        self.word1.draw()
        self.win.flip()
        event.waitKeys()
        return None

if __name__ == '__main__':
    Experiment('test_99', 3, 1).run()
