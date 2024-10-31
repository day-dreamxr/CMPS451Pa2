#Version: v0.1
#Date Last Updated: 12-20-2023

#%% STANDARDS   -DO NOT include this block in a new module
'''
Unless otherwise required, use the following guidelines
* Style:
    - Sort all alphabatically
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
 
* Performance and Safety:
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

'''

#%% MODULE BEGINS
module_name = '<***>'

'''
Version: <***>

Description:
    <***>

Authors:
    <***>

Date Created     :  <***>
Date Last Updated:  <***>

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


from matplotlib import pyplot as plt
#import mne
import numpy  as np 
import os
import pandas as pd
import seaborn as sns

#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
subject = 'sb1'
session = 'se1'
soi_file = '1_132_bk_pic.pckl'

#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Global declarations Start Here



#Class definitions Start Here



#Function definitions Start Here
def main():
    pass
#

#%% MAIN CODE                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main code start here

with open('1_132_bk_pic.pckl', 'rb') as fp:
    soi = pckl.load(fp)
#

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main Self-run block
if __name__ == "__main__":
    
    print(f"\"{module_name}\" module begins.")
    
    print(f"{soi['info']['eeg_info']['channels'][11]['label']}")
    print(f"{soi['info']['eeg_info']['channels'][3]['label']}")
    print(f"{soi['info']['eeg_info']['channels'][16]['label']}")
    
    print(f"{soi['series'][11]}")
    plt.plot(soi['series'][11], soi['tStamp'])
    
    
    #TEST Code
    main()
# %%
