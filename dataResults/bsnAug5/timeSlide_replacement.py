import numpy as np
import os
import sys
import fileinput
from tempfile import mkstemp
from shutil import move
from os import remove, close


dataFile = "/home/avi.vajpeyi/pycbcBackgroundTriggers/AllTrigsAndData_unique.txt"
Folder = "pycbcBackgroundTriggers"      # the folder in which the run was started
numList = [16,32,64]                      # the list of durations
fileNameList = ["lalinference_1126074285-1129348536.dag",
"lalinference_1126073757-1129348536.dag",
"lalinference_1126072701-1129348536.dag"]


def removeHashLine(fileToSearch):
    f = open(fileToSearch,"r")
    lines = f.readlines()
    f.close()
    f = open(fileToSearch, 'w')
    f.writelines([item for item in lines if '##' not in item])
    f.close()


def replace2(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)



def replace(textToReplace, textToSearch, fileToSearch):
    print("Text being searched: " + textToSearch)
    print("Text to replace: " + textToReplace)



    f = open(fileToSearch,"r")
    lines = f.readlines()
    f.close()


    f = open(fileToSearch, 'w')
    for line in lines:
        f.writelines([item for item in lines if '##' not in item])
    f.close()



    '''
    tempFile = open (fileToSearch, 'r+')
    print("Text being searched: " + textToSearch)
    print("Text to replace: " + textToReplace)

    count = 0
    for line in fileinput.input( fileToSearch):
        if textToSearch in line :
            count +=1
        tempFile.write(line.replace( textToSearch, textToReplace, 3 ) )
    print (str(count) + " matches \n\n")
    tempFile.close()


    '''


def dagFile(filePath, dataFile):


    fileToSearch = filePath
    removeHashLine(fileToSearch)

    # takes the data for the FAR, SNR, HTime, LTime and Time Slide val
    dataMatrix = np.loadtxt(dataFile)
    # some constants
    FAR = 0
    SNR = 1
    H_TIME = 2
    L_TIME = 3
    TIME_SLIDE = 4 # h - l

    for i in range(len(dataMatrix)):

        print ("Checking "+str(dataMatrix[i][H_TIME]))

        #TimeBeingSearched ='1128755932.49'
        TimeBeingSearched = dataMatrix[i][H_TIME]
        TimeSlideVal = (-1.0) * dataMatrix[i][TIME_SLIDE]

        # Save the string in this format: macroL1timeslide="TIME_SLIDE" macrotrigtime="1129097542.84"
        textToReplace = 'macroL1timeslide="'+str(TimeSlideVal)+'" macrotrigtime="'+str(TimeBeingSearched)+''
        textToSearch = 'macroL1timeslide="0" macrotrigtime="'+str(TimeBeingSearched)+''

        replace2( filePath, textToSearch,textToReplace)


#removeHashLine(fileName)
#replace("Bye", "hi", fileName)

#lalinference_1126074285-1129348536.dag
#lalinference_1126073757-1129348536.dag
#lalinference_1126072701-1129348536.dag


# iterating through the list of durations
for i, num in enumerate(numList):
    Number = str(num)
    print ("Processing files for duration " + Number + "s...")
    BASE_DIR ="/home/avi.vajpeyi/" + Folder + "/lalinferencenest/IMRPhenomPv2pseudoFourPN/"+Number+"s/"+fileNameList[i]
    dagFile(BASE_DIR, dataFile)
