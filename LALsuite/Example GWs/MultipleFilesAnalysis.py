pwdimport os

FILE_NAME = 1

BASE_DIR ='/home/avi.vajpeyi/backgroundAnalysis300July14/lalinferencenest/IMRPhenomPv2pseudoFourPN/4s'
MYCOMP_BASE_DIR = '/Users/Vajpeyi/Documents/LALsuite/lalinferenceData/IMRPhenomPv2pseudoFourPN/4s'





def coherentData():

    # File to output coherent data in
    coherent_output_file = open('coherent_output.txt', 'w')
    coherent_output = {}    # string that will contain the output


    # Open the folder in the set dir, and load the names of the file names
    coherent_DIR = BASE_DIR +'/coherence_test/'
    coherent_files = os.listdir( coherent_DIR )

    # Getting the File Names in the coherent_DIR
    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(coherent_DIR):
        for f in filenames:
            if 'coherence_test_H1L1_' in str(f):
                e = os.path.join(str(dirpath), str(f))
                file_list.append(e)

    # extracting the needed files and sorting them
    unsorted_files = []
    sorted_files = []
    for f in file_list:
        # extracting the number from the file name
        dashIndex = f.index("-")
        fnum = f[dashIndex+1:]
        dotIndex = fnum.index(".")
        fnum = fnum[:dotIndex]
        # the number of the file, and then the name
        unsorted_files.append([fnum,f])
    sorted_files= sorted(unsorted_files,key=lambda x: x[0])

    # Opening each file in order, storing GPS time and BayesFactor in output file
    for f in sorted_files:
        print (f[FILE_NAME])
        txtfile = open(f[FILE_NAME], 'r')
        coherent_output[f[FILE_NAME]] = []
        for line in txtfile:

            # getting the GPS time from file name
            GPStime = f[FILE_NAME]
            GPStime = GPStime[len(coherent_DIR+"coherence_test_H1L1_"):]
            dashIndex = GPStime.index("-")
            GPStime = GPStime[:dashIndex]

            line = line.strip('\n')
            coherent_output_file.write(line + '\t' + GPStime + '\n')

#------------------------------------------------------------------------


def incoherentData():

    # File to output coherent data in
    incoherent_output_file = open('incoherent_output.txt', 'w')
    incoherent_output = {}    # string that will contain the output

    # Open the folder in the set dir, and load the names of the file names
    incoherent_DIR = BASE_DIR +'/posterior_samples/'
    incoherent_files = os.listdir( incoherent_DIR )

    # Getting the File Names in the coherent_DIR
    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(incoherent_DIR):
        for f in filenames:
            if (('posterior_H1L1_'in str(f)) and ('.dat_B.txt'in str(f))):
                e = os.path.join(str(dirpath), str(f))
                file_list.append(e)
    print (file_list)

    # extracting the needed files and sorting them
    unsorted_files = []
    sorted_files = []
    for f in file_list:
        # extracting the number from the file name
        dashIndex = f.index("-")
        fnum = f[dashIndex+1:]
        dotIndex = fnum.index(".")
        fnum = fnum[:dotIndex]
        # the number of the file, and then the name
        unsorted_files.append([fnum,f])
    sorted_files= sorted(unsorted_files,key=lambda x: x[0])

    # Opening each file in order, storing GPS time and BayesFactor in output file
    for f in sorted_files:
        print (f[FILE_NAME])
        txtfile = open(f[FILE_NAME], 'r')
        incoherent_output[f[FILE_NAME]] = []
        for line in txtfile:

            # getting the GPS time from file name
            GPStime = f[FILE_NAME]
            GPStime = GPStime[len(incoherent_DIR+"posterior_H1L1_"):]
            dashIndex = GPStime.index("-")
            GPStime = GPStime[:dashIndex]

            firstSpace = line.index(' ')
            line = line[:firstSpace]
            #line = line.strip('\n')

            incoherent_output_file.write(line + '\t' + GPStime + '\n')

#------------------------------------------------------------------------



incoherentData()
coherentData()
