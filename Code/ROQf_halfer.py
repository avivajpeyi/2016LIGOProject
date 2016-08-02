
import h5py
import numpy as np
from scipy import sparse as sp
import os
import fnmatch



def halfFreq(BASE_DIR):

    # load the data from the two f.npy files

    fnodes_linear = np.load(BASE_DIR+"fnodes_linear.npy")
    fnodes_quadratic = np.load(BASE_DIR+"fnodes_quadratic.npy")

    np.save(BASE_DIR+"fnodes_linear_original.npy", fnodes_linear)
    np.save(BASE_DIR+"fnodes_quadratic_original.npy", fnodes_quadratic)

    np.save(BASE_DIR+"fnodes_linear.npy", fnodes_linear/2.0)
    np.save(BASE_DIR+"fnodes_quadratic.npy", fnodes_quadratic/2.0)

numList = [8,16,32,64] # the list of durations
#numList = [8]

# iterating through the list of durations
for num in numList:
    Number = str(num)
    print ("Processing files for duration " + Number + "s...")
    BASE_DIR ="/home/avi.vajpeyi/ROQfiles/"+Number+'s/'
    halfFreq(BASE_DIR)
