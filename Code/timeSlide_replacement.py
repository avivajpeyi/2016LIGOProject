import numpy as np
import os
import sys
import fileinput
from tempfile import mkstemp
from shutil import move
from os import remove, close

# The paths of the dags that need to be eddited! Provide initially
fileName = ["/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/16s/lalinference_1126074285-1129348536.dag", "/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/32s/lalinference_1126073757-1129348536.dag", "/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/64s/lalinference_1126072701-1129348536.dag" ]
# not including the first path as we have already eddited that dag --> "/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/lalinference_1126074549-1129348536.dag",


def removeHashLine(fileToSearch):
    f = open(fileToSearch,"r")
    lines = f.readlines()
    f.close()
    f = open(fileToSearch, 'w')
    f.writelines([item for item in lines if '##' not in item])
    f.close()
####################################

def replace(file_path, pattern, subst):
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
####################################

def addArgumentForReadingNewASD(dagToEdit):

    # get all lines in file
    f = open(dagToEdit,"r")
    lines = f.readlines()
    f.close()

    for i,line in enumerate(lines):

        print("Adjusting for new ASD for line number "+str(i))

        if "engine_H1L1.sub" in line: # then we need to add an arg

            # Need to match the VARstring with its appropriate ASD file
            VARstring = lines[i+2]

            # Breaking the string where ever a space is present
            VARstringBreakup = VARstring.split()

            # getting a segment of the path that we need
            pathSegmentIndex = VARstringBreakup.index('macroargument5="--roq-times') + 1
            pathSegment = VARstringBreakup[pathSegmentIndex]

            #splitting the path where ever '/' present
            pathSegmentBreakup = pathSegment.split('/')

            #getting the ROQ number from the path
            ROQnumIndex = pathSegmentBreakup.index("ROQdata") + 1
            ROQnum = pathSegmentBreakup[ROQnumIndex]

            #getting rid of the end portion of the path
            endString = ROQnum +'/tcs.dat'
            endIndex = pathSegment.index(endString)
            ASDfilePath = pathSegment[:endIndex]+"timeshiftedROQfiles/"+ROQnum+"/data-dumpL1-ASD.dat"

            # Adding the ASD file path the to VAR string
            newVARstring = VARstring.rstrip()+ ' macroargument10="--L1-psd '+ ASDfilePath+'"\n'

            replace(dagToEdit, VARstring, newVARstring)

        if "engine_L1.sub" in line: # then we need to add an arg

            # Need to match the VARstring with its appropriate ASD file
            VARstring = lines[i+2]

            # Breaking the string where ever a space is present
            VARstringBreakup = VARstring.split()

            # getting a segment of the path that we need
            pathSegmentIndex = VARstringBreakup.index('macroargument3="--roq-times') + 1
            pathSegment = VARstringBreakup[pathSegmentIndex]

            #splitting the path where ever '/' present
            pathSegmentBreakup = pathSegment.split('/')

            #getting the ROQ number from the path
            ROQnumIndex = pathSegmentBreakup.index("ROQdata") + 1
            ROQnum = pathSegmentBreakup[ROQnumIndex]

            #getting rid of the end portion of the path
            endString = ROQnum +'/tcs.dat'
            endIndex = pathSegment.index(endString)
            ASDfilePath = pathSegment[:endIndex]+"timeshiftedROQfiles/"+ROQnum+"/data-dumpL1-ASD.dat"

            # Adding the ASD file path the to VAR string
            newVARstring = VARstring.rstrip()+ ' macroargument7="--L1-psd '+ ASDfilePath+'"\n'

            replace(dagToEdit, VARstring, newVARstring)
    # Else, the line doesnt change
####################################

def applyTimeSlideToDagFile(dagToEdit):


    # WE HAE USED H TIME AS THE NOISE TRIGS!!
    ## THUS WE NEED TO TIME SHIFT L!

    removeHashLine(dagToEdit)

    # takes the data for the FAR, SNR, HTime, LTime and Time Slide val
    dataMatrix = np.loadtxt('AllTrigsAndData_unique.txt',skiprows=1)
    # some constants
    FAR = 0
    SNR = 1
    H_TIME = 2
    L_TIME = 3
    TIME_SLIDE = 4 # h - l

    for i in range(len(dataMatrix)):

        print ("Adding the time shifts for "+str(dataMatrix[i][H_TIME]))

        #TimeBeingSearched ='1128755932.49'
        TimeBeingSearched = dataMatrix[i][H_TIME]
        # IMPORTANT NOTE ON TIME-SLIDES:
        #   Time_H - Time_L = TimeSlideVal
        #   If L is ahead in time, we need to give it a negative value to shift it back
        #   If L is back in time, we need to give it a positive value to shift it ahead
        #
        # HOWEVER,
        #   L_slide is the value that has been already applied to get L1 in its current position.
        #
        TimeSlideVal =  dataMatrix[i][TIME_SLIDE]

        # Save the string in this format: macroL1timeslide="TIME_SLIDE" macrotrigtime="1129097542.84"
        textToReplace = 'macroL1timeslide="'+str(TimeSlideVal)+'" macrotrigtime="'+str(TimeBeingSearched)+''
        textToSearch = 'macroL1timeslide="0" macrotrigtime="'+str(TimeBeingSearched)+''

        offlineDir = "/Users/Vajpeyi/Documents/Ligo Summer Research /2016LIGOProjectProposal/dataResults/pycbcTrigs_gps_times/lalinference_1126074549-1129348536.dag"
        onlineDir  = dagToEdit
        replace(dagToEdit, textToSearch,textToReplace)
####################################

for i, path in enumerate(fileName):
    print("Editing the " + path + " dag file \n")
    applyTimeSlideToDagFile(path)
    addArgumentForReadingNewASD(path)
