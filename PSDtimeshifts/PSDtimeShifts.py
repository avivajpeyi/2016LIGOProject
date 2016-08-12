import numpy as np
import os
import sys
import fileinput
from tempfile import mkstemp
from shutil import move
from os import remove, close





fileToSearch = 'lalinference_1126074549-1129348536.sh' #


# takes the data for the FAR, SNR, HTime, LTime and Time Slide val
dataMatrix = np.loadtxt('AllTrigsAndData_unique.txt',skiprows=1)
# some constants
FAR = 0
SNR = 1
H_TIME = 2
L_TIME = 3
TIME_SLIDE = 4 # h - l



onlinePath = '/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/ROQdata/timeshiftedROQfiles'
directoryToCreate = '/Users/Vajpeyi/Documents/Ligo Summer Research /2016LIGOProjectProposal/PSDtimeshifts/timeshiftedROQfiles'
if not os.path.exists(onlinePath):
    os.makedirs(onlinePath)


'''
/home/avi.vajpeyi/local/bin/lalinference_datadump --L1-flow 10 --psdlength 1024 --randomseed 1268060671 --seglen 8 --L1-channel L1:DCS-CALIB_STRAIN_C01 --L1-timeslide 0 --H1-flow 10 --H1-timeslide 0 --trigtime 1127002734.67 --psdstart 1127001781.0 --H1-cache /home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/caches/H-H1_HOFT_C01_CACHE-1126074549-3273987.lcf --L1-cache /home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/caches/L-L1_HOFT_C01_CACHE-1126074549-3273987.lcf --srate 1024 --H1-channel H1:DCS-CALIB_STRAIN_C01 --outfile /home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/ROQdata/1018/data-dump  --data-dump  --ifo H1  --ifo L1
/home/avi.vajpeyi/local/bin/lalinference_datadump --L1-flow 10 --psdlength 1024 --randomseed 1671023922 --seglen 8 --L1-channel L1:DCS-CALIB_STRAIN_C01 --L1-timeslide 0 --H1-flow 10 --H1-timeslide 0 --trigtime 1126257549.25 --psdstart 1126256821.0 --H1-cache /home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/caches/H-H1_HOFT_C01_CACHE-1126074549-3273987.lcf --L1-cache /home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/caches/L-L1_HOFT_C01_CACHE-1126074549-3273987.lcf --srate 1024 --H1-channel H1:DCS-CALIB_STRAIN_C01 --outfile /home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/ROQdata/973/data-dump  --data-dump  --ifo H1  --ifo L1
'''


###
#   generateDataDumpList(fileToSearch)
#
#   Opens the sh file and extracts the data dump commands
#
#   Return value:
#       A list with the data-dump command for each instance
###
def generateDataDumpList(fileToSearch):
    f = open(fileToSearch,"r")
    lines = f.readlines()
    f.close()

    sub = "/home/avi.vajpeyi/local/bin/lalinference_datadump --L1-flow 10 --psdlength 1024"
    dataDumpList =[]

    for string in lines:
        if sub in string:
            dataDumpList.append(string)
    return dataDumpList


def adjustDataDumpCommand(commandBreakup, L_shiftedTime):

    # note commandBreakup = origCommand.split()

    timsshifted_L1trigTime = L_shiftedTime
    adjustedPSDtime = timsshifted_L1trigTime - 540.1


    '''
    An exmaple of the result of splitting the command:

    commandBreakup = origCommand.split() -->


    0   '/home/avi.vajpeyi/local/bin/lalinference_datadump',
    1   '--L1-flow',
    2   '10',
    3   '--psdlength',
    4   '1024',
    5   '--randomseed',
    6   '1876456972',
    7   '--seglen',
    8   '8',
    9   '--L1-channel',
    10  'L1:DCS-CALIB_STRAIN_C01',
    11  '--L1-timeslide',
    12  '0',
    13  '--H1-flow',
    14  '10',
    15  '--H1-timeslide',
    16  '0',
    17  '--trigtime',
    18  '1128755932.49',
    19  '--psdstart',
    20  '1128755381.0',
    21  '--H1-cache',
    22  '/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/caches/H-H1_HOFT_C01_CACHE-1126074549-3273987.lcf',
    23  '--L1-cache',
    24  '/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/caches/L-L1_HOFT_C01_CACHE-1126074549-3273987.lcf',
    25  '--srate',
    26  '1024',
    27  '--H1-channel',
    28  'H1:DCS-CALIB_STRAIN_C01',
    29  '--outfile',
    30  '/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/ROQdata/936/data-dump',
    31  '--data-dump',
    32  '--ifo',
    33  'H1',
    34  '--ifo',
    35  'L1'
    '''
    newString = ''


    # sameStartPortion consists of commandBreakup[0] to commandBreakup[4]
    sameStartPortion = "/home/avi.vajpeyi/local/bin/lalinference_datadump --L1-flow 10 --psdlength 1024 "
    newString = newString + sameStartPortion


    # adding the commandBreakup[5] to commandBreakup[12] (the randomseed to L1-timeslide)
    '''
    5   '--randomseed',
    6   '1876456972',
    7   '--seglen',
    8   '8',
    9   '--L1-channel',
    10  'L1:DCS-CALIB_STRAIN_C01',
    11  '--L1-timeslide',
    12  '0',
    '''
    ranSeedIndex = commandBreakup.index("--randomseed") + 1
    ranSeedVal   = commandBreakup[ranSeedIndex]
    seglenIndex  = commandBreakup.index("--seglen") + 1
    seglenVal    = commandBreakup[seglenIndex]

    stringSection2 = '--randomseed ' +ranSeedVal+' --seglen ' +seglenVal+' --L1-channel L1:DCS-CALIB_STRAIN_C01 --L1-timeslide 0 '
    newString = newString + stringSection2


    # Skipping commandBreakup[13] to commandBreakup[16] as they involve H
    '''
    13  '--H1-flow',
    14  '10',
    15  '--H1-timeslide',
    16  '0',
    '''

    # changing trig time to L's timeshifted trig time
    '''
    17  '--trigtime',
    18  '1128755932.49',
    '''
    trigtimeString = "--trigtime " +str(timsshifted_L1trigTime)+ " "
    newString = newString + trigtimeString

    # changing psd start to (time shifted L - 540.1)
    '''
    19  '--psdstart',
    20  '1128755381.0',
    '''
    adjustedPSDtimeString = "--psdstart " + str(adjustedPSDtime)+ " "
    newString = newString + adjustedPSDtimeString

    # Skipping commandBreakup[21] to commandBreakup[22] as they involve H
    '''
    21  '--H1-cache',
    22  '/home/avi.vajpeyi/p.....',
    '''

    # adding the commandBreakup[23] to commandBreakup[26]
    '''
    23  '--L1-cache',
    24  '/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/caches/L-L1_HOFT_C01_CACHE-1126074549-3273987.lcf',
    25  '--srate',
    26  '1024',
    '''
    L1_cacheIndex = commandBreakup.index("--L1-cache") + 1
    L1_cacheVal   = commandBreakup[L1_cacheIndex]
    srateIndex = commandBreakup.index("--srate") + 1
    srateVal   = commandBreakup[srateIndex]
    newString = newString + '--L1-cache ' +L1_cacheVal+' --srate '+ srateVal +' '

    # Skipping commandBreakup[27] to commandBreakup[28] as they involve H
    '''
    27  '--H1-channel',
    28  'H1:DCS-CALIB_STRAIN_C01',
    '''

    # changing the out directory for the file ---> first we create the dir for it
    '''
    29  '--outfile',
    30  '/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/ROQdata/936/data-dump',
    '''
    pathSections = commandBreakup[30].split('/')
    ROQfileNumIndex =  pathSections.index("ROQdata") + 1
    offlinePath = '/Users/Vajpeyi/Documents/Ligo Summer Research /2016LIGOProjectProposal/PSDtimeshifts/timeshiftedROQfiles/'+ pathSections[ROQfileNumIndex]+"/"
    onlinePath = '/home/avi.vajpeyi/pycbcBackgroundTriggers/lalinferencenest/IMRPhenomPv2pseudoFourPN/8s/ROQdata/timeshiftedROQfiles/'+ pathSections[ROQfileNumIndex]+"/"
    if not os.path.exists(onlinePath):
        os.makedirs(onlinePath)


    newString = newString + "--outfile "+onlinePath +"/data-dump "

    # adding the end '--data-dump --ifo L1' instead of adjusting lines 31 - 35
    '''
    31  '--data-dump',
    32  '--ifo',
    33  'H1',
    34  '--ifo',
    35  'L1'
    '''
    newString = newString + "--data-dump --ifo L1"

    return newString

def generateNewCommandList(dataMatrix):

    # NewCommandString will store the string with the new adjusted commands to generate the PSDs
    NewCommandString = ""

    # OriginalCommandList is a list of all the commands as strings
    OriginalCommandList = generateDataDumpList(fileToSearch)

    # OriginalCommandListBreakup is a list of the list of the different commands, broken into seperate words
    OriginalCommandListBreakup = []
    for i in range(len(OriginalCommandList)):
        OriginalCommandListBreakup.append(OriginalCommandList[i].split())
    # each orignal command is broken into seperate words

    # Going through the entire list of the different trigger times for the noise events
    for i in range(len(dataMatrix)):

        HOrigTime = dataMatrix[i][H_TIME]
        LOrigTime = dataMatrix[i][L_TIME]
        TimeSlideVal = (-1.0) * dataMatrix[i][TIME_SLIDE]
        L_timeshifted = LOrigTime

        print ("Editing command for "+str(HOrigTime)+"...\n\n")

        # Need to see if the trig time matches the H time
        #   -- ROQ files are specific for dif Trig times
        # need to match each orig command with the trig time

        # The original command list has the tirgger time set as the H time, so we will search for that
        SearchTime = str(HOrigTime)
        #doubleDimIndex will store the index at which the list of the command breakup with SearchTime in the command is present, and the index at which the Searchtime is found in this list
        doubleDimIndex = [(index, row.index(SearchTime)) for index, row in enumerate(OriginalCommandListBreakup) if SearchTime in row]
        print ("Found at ")
        print(doubleDimIndex)
        # SpecificCommandBreakup will store the specifc original command associated with the given trigger time
        SpecificCommandBreakup = OriginalCommandListBreakup[doubleDimIndex[0][0]]
        # newCommand will store the adjusted command, with the lines containing H deleted, and the new L shifted time, output file, PSD starttime
        newCommand = adjustDataDumpCommand(SpecificCommandBreakup, L_timeshifted)
        # Appending the new string to the
        NewCommandString = NewCommandString + "\n" + newCommand

        print("Old Command breakup: \n ")
        print(SpecificCommandBreakup)

        print("\nNew Command:\n")
        print(newCommand)

    return (NewCommandString+'\n')


outputString = generateNewCommandList(dataMatrix)
text_file = open("PSD_commands.txt", "w")
text_file.write(outputString)
text_file.close()
