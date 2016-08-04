import numpy as np
import os
import sys
import fileinput

# WE HAE USED H TIME AS THE NOISE TRIGS!!
## THUS WE NEED TO TIME SHIFT L!


fileToSearch = 'lalinference_1126074549-1129348536.dag'
dagFile = open(fileToSearch, 'r+')



# takes the data for the FAR, SNR, HTime, LTime and Time Slide val
dataMatrix = np.loadtxt('allTrigsandData_unique.txt',skiprows=1)
# some constants
FAR = 0
SNR = 1
H_TIME = 2
L_TIME = 3
TIME_SLIDE = 4 # h - l


for i in range(len(dataMatrix)):
    TimeSlideVal = (-1.0) * dataMatrix[i][TIME_SLIDE]
    # Save the string in this format: macroL1timeslide="TIME_SLIDE" macrotrigtime="1129097542.84"
    textToReplace = '"macroL1timeslide="'+str(TimeSlideVal)+'" macrotrigtime="'+str(dataMatrix[i][H_TIME])+'"'
    textToSearch = '"macroL1timeslide="0" macrotrigtime="'+str(dataMatrix[i][H_TIME])+'"'

    # since there are three instances of the string in each DAG
    for x in range(3):
        for line in fileinput.input( fileToSearch ):
            if textToSearch in line :
                print(str(x+1)+' match Found for '+str(dataMatrix[i][H_TIME]+' in:\n'))
                print(line)
            else:
                print( str(x+1)+' Match Not Found for '+str(dataMatrix[i][H_TIME])+'in:\n')
                print(line)
            #dagFile.write(line.replace( textToSearch, textToReplace ) )
dagFile.close()
