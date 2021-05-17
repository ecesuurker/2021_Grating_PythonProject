import csv
import random
from psychopy import visual, core, event, sound
import ast
from ast import literal_eval
import time
import sounddevice as sd
import soundfile as sf
import glob # lets you iterate through a folder of files 


class Experiment(object):


    def __init__(self, pp, category, cbList, fps=60.0):
        self.pp = pp
        self.fps = fps
        self.category = category
        # set up file paths, etc.
        #self.trials_fname = 'trial_structure/Colors_trials.txt'
        self.trials_fname = 'trial_structure/Colors_trials_simple.txt'
        self.log_fname = 'logs/' + str(cbList) + '_' + pp + '.csv'
        self.stimuli_folder = 'stimuli/'
        self.cbList = cbList
        variableFile = open("trial_structure/CounterbalanceVariables.txt", "r")
        counterbalance = csv.DictReader(variableFile, delimiter="\t")
        for row in counterbalance:
            if row["List_Number"] == str(cbList):
                self.angles = row["Angles"].split(" ")
                print(self.angles)
                self.label1 = row["Label1"]
                self.label2 = row["Label2"]
                self.sameKey = row["Same_key"]
                self.diffKey = row["Diff_key"]
                self.transferOrder = row["Transfer_Task_Order"]
                self.frequency = row["Grating_Frequency"].split(" ")
                print(self.frequency)


    def run(self):
        # set up presentation window color, and size
        bgcolor = 'grey'
        txtcolor = 'white'
        c = .5 # variable that stores contrast values 
        #self.win = visual.Window(fullscr=True, color=bgcolor, units='pix')
        self.win = visual.Window((1200, 900), color=bgcolor, units='pix')  # temporary presentation window setup, exchange for line above when running actual experiment

        # basic setup for audio recording with sounddevice
        sd.default.samplerate = 48000
        sd.default.channels = 1

        # set up timing related stuff
        self.frame_dur = 1.0 / self.fps
        self.clock = core.Clock()  # trial timer
        self.expclock = core.Clock()  # whole experiment timer
        # inter trial interval setup
        self.isi = core.StaticPeriod()
        self.isi.start(.5)

        # various stimulus presentation boxes for text and images
        self.word1 = visual.TextStim(self.win, color=txtcolor, height=30)
        self.word1.wrapWidth = 900
        self.word2 = visual.TextStim(self.win, color=txtcolor, height=30)
        self.word2.wrapWidth = 900
        self.title = visual.TextStim(self.win, pos=(0, 200), color=txtcolor, height=30)
        self.title.wrapWidth = 900
        self.box1 = visual.Rect(self.win, width=300, height=300, pos=[0,0], lineWidth=1, lineColor='black', fillColorSpace='rgb', fillColor=[0,.8,.4])
        self.box2 = visual.Rect(self.win, width=300, height=300, pos=[300,0], lineWidth=1, lineColor='black', fillColorSpace='rgb', fillColor=[0,.8,.4])
        self.fixation = visual.ShapeStim(self.win, 
            vertices=((0, -15), (0, 15), (0,0), (-15,0), (15, 0)),
            lineWidth=5,
            pos=[0,0],
            closeShape=False,
            lineColor="black")
        self.image_l = visual.ImageStim(self.win, pos=(0, 0), size=[300,300])
        self.grating = visual.GratingStim(self.win, units="pix", size=[200, 200], mask="gauss", contrast=1.0)


        # actually run the experiment routines
        with open(self.trials_fname, 'r') as trial_file, open(self.log_fname, 'w', newline='') as log_file:
            # read trial structure
            trials = csv.DictReader(trial_file, delimiter='\t')

            # set up log file
            log_fields = trials.fieldnames + ['keypress', 'RT', 'ACC', 't']
            log = csv.DictWriter(log_file, fieldnames=log_fields)
            log.writeheader()

            blocks = {}
            for trial in trials:
                if trial['block'] not in blocks.keys():
                    blocks[trial['block']] = [trial]
                else:
                    blocks[trial['block']].append(trial)


            # present the trials
            random.seed(self.pp)
            for block_number in sorted(blocks.keys()):
                trials = blocks[block_number]
                #if trials[0]['randomize'] == 'yes':
                 #   random.shuffle(trials)
                for trial in trials:
                    self.clock.reset()  # reset trial clock
                    trial = self.present_trial(trial)  # present the trial
                    log.writerow(trial)  # log the trial data
        self.win.close()



    # select the appriopriate trial subroutine
    def present_trial(self, trial):
        type = trial['type']
        if type == 'instructions':
            trial = self.instruction_trial(trial)
        elif type == 'exposure':
            trial = self.exposure_trial(trial)
        elif type == 'categorization':
            trial = self.categorization_trial(trial)
        elif type == 'discrimination':
            trial = self.discrimination_trial(trial)
        elif type == 'memory':
            trial = self.memory_trial(trial)
        else:
            # unknown trial type, return some kind of error?
            print('ERROR: unknown trial type')

        # log experiment timer and return trial data
        trial['t'] = self.expclock.getTime()
        return trial


    def instruction_trial(self, trial):
        # present instruction trial
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


    def exposure_trial(self, trial):
        self.fixation.draw()
        self.win.flip()
        core.wait(.5)
        self.word1.text = trial['label'].replace('<br>', '\n')
        self.word1.draw()
        self.win.flip()
        core.wait(1)
        self.box1.fillColor = literal_eval(trial['color'])
        self.box1.draw()
        self.win.flip()
        core.wait(1)
        self.isi.complete()
        self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial


    def categorization_trial(self, trial):
        ang = [0,1,2,3]
        random.shuffle(ang)
        for a in ang:
            self.fixation.draw()
            self.win.flip()
            core.wait(.5)
            self.grating.ori = literal_eval(self.angles[a])
            self.grating.sf = literal_eval(random.choice(self.frequency))
            self.grating.draw()
            self.word1.text = self.label1
            self.word2.text = self.label2
            positions = [(-200,-200),(200,-200)]
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
            if a < 2 and positions[0] == (-200,-200) and trial['keypress'] == self.sameKey or a > 2 and positions[1] == (200,-200) and trial["keypress"] == self.diffKey:
                trial['ACC'] = 1
                self.feedback(1)
            else:
                trial['ACC'] = 0
                self.feedback(0)
            self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial

    def memory_trial(self, trial):
        comparison = [[0,0],[1,1],[2,2],[3,3],[0,1],[1,2],[2,3]]
        random.shuffle(comparison)
        for t in comparison:
            random.shuffle(t)
            self.fixation.draw()
            self.win.flip()
            core.wait(.5)
            self.grating.ori = literal_eval(self.angles[t[0]])
            self.grating.sf = literal_eval(random.choice(self.frequency))
            self.grating.draw()
            self.win.flip()
            core.wait(1)
            self.fixation.draw()
            self.win.flip()
            core.wait(.5)
            self.grating.ori = literal_eval(self.angles[t[1]])
            self.grating.sf = literal_eval(random.choice(self.frequency))
            self.grating.draw()
            self.win.flip()
            core.wait(1)
            self.word1.text = trial['content'].replace('<br>', '\n')
            self.word1.draw()
            self.win.callOnFlip(self.clock.reset)
            self.isi.complete()
            self.win.flip()
            keys = event.waitKeys(keyList=['escape'] + [self.sameKey] + [self.diffKey], timeStamped=self.clock)
            trial['keypress'], trial['RT'] = keys[0]
            if trial['keypress'] == 'escape':
                core.quit()
            if trial['keypress'] == self.sameKey and t[0] != t[1] or trial["keypress"] == self.diffKey and t[0] == t[1]:
                trial['ACC'] = 0
            # self.feedback(1)
            else:
                trial['ACC'] = 1
            # self.feedback(0)
        self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial

    def discrimination_trial(self, trial):
        self.fixation.draw()
        self.win.flip()
        core.wait(.5)
        self.fixation.draw()
        self.box1.fillColor = literal_eval(trial['color'])
        self.box1.pos = (-300, 0)
        self.box1.draw()
        self.box2.fillColor = literal_eval(trial['color2'])
        self.box2.draw()
        self.win.flip()
        core.wait(1)
        self.word1.text = trial['content'].replace('<br>', '\n')
        self.word1.draw()
        self.win.callOnFlip(self.clock.reset)
        self.win.flip()
        self.isi.complete()
        keys = event.waitKeys(keyList=['escape'] + trial['keyboard'].split(' '), timeStamped=self.clock)
        trial['keypress'], trial['RT'] = keys[0]
        if trial['keypress'] == 'escape':
            core.quit()
        if trial['keypress'] == trial['key']:
            trial['ACC'] = 1
            # self.feedback(1)
        else:
            trial['ACC'] = 0
            # self.feedback(0)
        self.win.callOnFlip(self.isi.start, float(trial['ITI']) / 1000 - self.frame_dur)
        # flip buffer again and start ISI timer
        self.win.flip()
        return trial
    
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

if __name__ == '__main__':
    Experiment('test_99', 'Color', 3).run()
