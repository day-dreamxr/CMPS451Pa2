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
from scipy.signal import butter, filtfilt, iirfilter
from scipy.stats import skew, kurtosis

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
    
    data = pd.DataFrame(columns=['FILENAME', 'SUBJECT', 'SESSION', 'CHANNEL', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'])
    data.index.name = 'OBJECT ID'
    
    for subject in subjects:
        sessions = sorted(os.listdir("INPUT\\"+subject), key=len)
        for session in sessions:
            files = sorted(os.listdir("INPUT\\"+subject+"\\"+session), key=len)
            for file in files:
                with open("INPUT\\"+subject+"\\"+session+"\\"+file, 'rb') as fp:
                    soi = pckl.load(fp)
                #
                for i in [11, 3, 16]:
                    stream = soi['series'][i]
                    ##APPLY FILTERS
                    notchFilter1 = butter(1, [59,61], btype='bandstop', fs=1000)
                    notchFilter2 = butter(1, [119,121], btype='bandstop', fs=1000)
                    notchFilter3 = butter(1, [179,181], btype='bandstop', fs=1000)
                    notchFilter4 = butter(1, [239,241], btype='bandstop', fs=1000)

                    filteredStream = filtfilt(notchFilter1[0], notchFilter1[1], stream)
                    filteredStream = filtfilt(notchFilter2[0], notchFilter2[1], filteredStream)
                    filteredStream = filtfilt(notchFilter3[0], notchFilter3[1], filteredStream)
                    filteredStream = filtfilt(notchFilter4[0], notchFilter4[1], filteredStream)
                    
                    impedanceFilter = butter(1, [124,126], btype='bandstop', fs=1000)
                    filteredStream = filtfilt(impedanceFilter[0], impedanceFilter[1], filteredStream)
                    
                    bandPassFilter = butter(1, [0.5,32], btype='bandpass', fs=1000)
                    filteredStream = filtfilt(bandPassFilter[0], bandPassFilter[1], filteredStream)
                    
                    ##WINDOW DATA
                    windowMeans = []
                    windowStds = []
                    windowBounds = [0, L]
                    windowNum = 0
                    numOfWindows = math.ceil(len(filteredStream)/L)
                    while windowNum <= numOfWindows:
                        ##WINDOW THE DATA
                        windowedData = filteredStream[int(windowBounds[0]):int(windowBounds[1])]
                        windowMeans.append(np.mean(windowedData))
                        windowStds.append(np.std(windowedData))
                    
                        ##MOVE WINDOW
                        windowNum = windowNum + 1
                        windowBounds = [(windowNum * 0.75) * L, (windowNum * 0.75 + 1) * L]
                        if windowBounds[1] > len(filteredStream):
                            windowBounds[1] = len(filteredStream)
                        #
                    #
                    ##GENERATE FEATURES
                    f1 = np.mean(windowMeans)
                    f2 = np.std(windowMeans)
                    f3 = skew(windowMeans)
                    f4 = kurtosis(windowMeans)
                    f5 = np.mean(windowStds)
                    f6 = np.std(windowStds)
                    f7 = skew(windowStds)
                    f8 = kurtosis(windowStds)
                    
                    ##ADD FEATURES TO DATAFRAME
                    data.loc[len(data.index)] = [file, subject, session, soi['info']['eeg_info']['channels'][i]['label'], f1, f2, f3, f4, f5, f6, f7, f8]
                #
            #
        #
    #
    
    ##CONVERT DATAFRAME TO CSV
    data.to_csv('OUTPUT\\Data.csv')
    
    vPlot, ax = plt.subplots(1)
    ax.violinplot(dataset=data[['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']], showmeans=True)
    ax.set_title(label="Generated Features From DataSmall.zip")
    ax.set_xlabel("Feature Number")
    vPlot.savefig('OUTPUT\\vPlot.png')
    
    hPlots, axs = plt.subplots(nrows=2, ncols=4, constrained_layout=True, figsize=[15, 7])
    hPlots.suptitle("Histograms of Each Feature Generated From DataSmall.zip")
    axs[0][0].hist(data['F1'])
    axs[0][0].set_title("F1")
    axs[0][1].hist(data['F2'])
    axs[0][1].set_title("F2")
    axs[0][2].hist(data['F3'])
    axs[0][2].set_title("F3")
    axs[0][3].hist(data['F4'])
    axs[0][3].set_title("F4")
    axs[1][0].hist(data['F5'])
    axs[1][0].set_title("F5")
    axs[1][1].hist(data['F6'])
    axs[1][1].set_title("F6")
    axs[1][2].hist(data['F7'])
    axs[1][2].set_title("F7")
    axs[1][3].hist(data['F8'])
    axs[1][3].set_title("F8")
    hPlots.savefig('OUTPUT\\hPlots.png')
#

#%% MAIN CODE                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main code start here


#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main Self-run block
if __name__ == "__main__":
    
    print(f"\"{module_name}\" module begins.")
    
    #TEST Code
    main()
# %%
