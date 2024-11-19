#Version: v0.1
#Date Last Updated: 12-20-2023

#%% STANDARDS   -DO NOT include this block in a new module
'''
Unless otherwise required, use the following guidelines
* Style:
    - Write the code in aesthetically-pleasing style
    - Names should be self-explanatory
        - "the main variable designator_variable group name": "child_parent"
            - pm_single, not singlepm, dataDf_grpL_1 , not dataDf_grpL1; "_1" is safer for bugs.
    - Comment adequately.
        - Add a comment for each code block, such as a loop-block, that describe the functionality
    - Use relative path
    - Use generic coding instead of manually-entered constant values
    - Legends should be good enough in color, linestyle, shape etc. to distinguish data series.
    - Always test your code with an artificial data whose return value is known.
    - Add the symbol # at the end of EACH block.
    - Sort imports aphabetically
 
* Performance and Safety:
    - Avoid use of global variables. If needed, use cautiously. Add suffix 
        - "_gl" to global variables
        - "_ui" to the user interface variables    
    - Code must be efficient (data-structure, functionality).
    - Avoid if-block in a loop-block unless it is required.
    - Do not calculate a common/constant value inside a loop.
    - Avoid declarations in a loop-block unless it is required.
    - Avoid initializing variables inside a loop unless it is required.
    - Initialize an array if size is known.
    - Save data in categorized folders.
    - import only the components from a package/module to be used instead of entire one.

    - Avoid using global scope
    - Prefer to use immutable types
    - Use deep-copy
    - Use [None for i in Sequence] instead of [None]*len(Sequence)
    - Initialize objects with None (null) (NOT zero) if their size is known instead of using append-like methods.
    - Operations with dataframe
        - Sort by the same column  name, and then reset index. As an example,
            grid_EntrpAll = x_trans.value_counts(subset=featureLst,normalize=True)
            reset_index().sort_values(featureLst).reset_index()
    - Utilize process logging


'''

#%% MODULE BEGINS
module_name = 'PA3 DK Crew'

'''
Version: <***>

Description:
    <***>

Authors:
    Zachary Gros

Date Created     :  11/17/2024
Date Last Updated:  11/17/2024

Doc:
    <***>

Notes:
    <***>
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
   import os
   #os.chdir("./../..")
#

#custom imports
import pickle as pckl

#other imports
from   copy       import deepcopy as dpcpy

import math
from   matplotlib import pyplot as plt
#import mne
import numpy  as np 
import os
import pandas as pd
import seaborn as sns

#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Global declarations Start Here



#Class definitions Start Here



#Function definitions Start Here
def main():
    subjects = sorted(os.listdir("INPUT"), key=len)
    L = 100
    
    data = pd.DataFrame(columns=['FILENAME', 'SUBJECT', 'SESSION', 'CHANNEL', 'F1', 'F2','F3', 'F4', 'F5', 'F6', 'F7', 'F8'])
    data.index.name = 'OBJECT ID'
    print(data)
    
    for subject in subjects:
        sessions = sorted(os.listdir("INPUT\\"+subject), key=len)
        for session in sessions:
            files = sorted(os.listdir("INPUT\\"+subject+"\\"+session), key=len)
            for file in files:
                with open("INPUT\\"+subject+"\\"+session+"\\"+file, 'rb') as fp:
                    soi = pckl.load(fp)
                #
                windowMeans = []
                
                windowBounds = [0, L]
                windowNum = 0
                numOfWindows = math.ceil(len(soi['series'][11]))
                while windowNum <= numOfWindows:
                    #WINDOW THE DATA
                    windowedData = soi['series'][11][range(0, 100)]
                    windowMean = windowedData.mean()
                    windowMeans.append(windowMean)
                    
                    
                    
                    #MOVE WINDOW
                    windowNum = windowNum + 1
                    windowBounds = [(windowNum * 0.75) * L, (windowNum * 0.75 + 1) * L]
                #
                
                #GENERATE FEATURES
                print(windowMeans)
                
                #PUT FEATURES IN DATAFRAME
            #
        #
    #
    
    #CONVERT DATAFRAME TO CSV
    data.to_csv('Data.csv')
#

#%% MAIN CODE                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main code start here




#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main Self-run block
if __name__ == "__main__":
    
    print(f"\"{module_name}\" module begins.")
    
    #TEST Code
    main()