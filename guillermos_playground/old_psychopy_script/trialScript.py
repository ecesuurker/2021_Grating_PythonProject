import csv #I just created values that will be counterbalanced
angle = [[100,103,106,109],[103,106,109,112]] #I have written two possibilities for variable
names = [["knurp", "blash"],["blash", "knurp"]]
keys =[["z","."],[".","z"]]
transferTask = [[1],[2]] #Since this is about the order of the trials I thought that their 
#order can be arranged with an if condition
counterbalance = {}
trials = [0,0,0,0] #I did not create the list totally empty because I cannot manipulate
i=1 #indexes if the list is empty
for i1 in range(2): #these loops create all 16 combinations and put them in a list and number them
    trials[0] = angle[i1]
    for i2 in range(2):
        trials[1] = names[i2]
        for i3 in range(2):
            trials[2] = keys[i3]
            for i4 in range(2):
                trials[3] = transferTask[i4]
                counterbalance[i] = trials.copy() #If I don't put the copy of the list to dict 
                i+=1                    #lists in the dict change as well

for num in range(1,17): #This loop creates 16 files
    fileName = "trial_structure/TT_" + str(num) + ".txt"
    file = open(fileName, "w", newline="")
    oldTrials = open("trial_structure/Colors_trials_simple.txt","r")
    template = csv.DictReader(oldTrials, delimiter='\t') #I used the field names from the colors experiment trial file
    logField = template.fieldnames
    log = csv.DictWriter(file, fieldnames=logField, delimiter="\t")
    log.writeheader()