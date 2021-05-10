import csv #I just created values that will be counterbalanced
import numpy  

angle = [numpy.linspace(50,59,4,dtype="int"), numpy.linspace(53,62,4,dtype="int")]
names = [["knurp", "blash"],["blash", "knurp"]]
keys =[["z","."],[".","z"]]
transferTask = [[1],[2]] #Since this is about the order of the trials I thought that their 
#order can be arranged with an if condition
gratingFreq = [numpy.linspace(0.03,0.042,4), numpy.linspace(0.033,0.045,4)]
counterbalance = {}
trials = [0,0,0,0,0] #I did not create the list totally empty because I cannot manipulate
i=1 #indexes if the list is empty
for i1 in range(2): #these loops create all 16 combinations and put them in a list and number them
    trials[0] = angle[i1]
    for i2 in range(2):
        trials[1] = names[i2]
        for i3 in range(2):
            trials[2] = keys[i3]
            for i4 in range(2):
                trials[3] = transferTask[i4]
                for i5 in range(2):
                    trials[4] = gratingFreq[i5]
                    counterbalance[i] = trials.copy() #If I don't put the copy of the list to dict 
                    i+=1                    #lists in the dict change as well
print(counterbalance)
fileName = "trial_structure/CounterbalanceVariables.txt"
file = open(fileName, "w", newline="")
fileField = ["Trial_Number", "Angles", "Label1", "Label2", "Same_key", "Diff_key", "Transfer_Task_Order", "Grating_Frequency"]
f = csv.DictWriter(file, fieldnames=fileField, delimiter="\t")
f.writeheader()
for j in range(1,17):
    row = {}
    row[fileField[0]] = j
    row[fileField[1]] = counterbalance[j][0]
    row[fileField[2]] = counterbalance[j][1][0]
    row[fileField[3]] = counterbalance[j][1][1]
    row[fileField[4]] = counterbalance[j][2][0]
    row[fileField[5]] = counterbalance[j][2][1]
    row[fileField[6]] = counterbalance[j][3][0]
    row[fileField[7]] = counterbalance[j][4]
    f.writerow(row)
file.close()