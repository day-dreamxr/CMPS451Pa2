#Version: v0.1
#Date Last Updated: 12-20-2023

#%% MODULE BEGINS
module_name = 'DK Crew'

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
import mne
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

with open(soi_file, 'rb') as fp:
    soi = pckl.load(fp)
#

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main Self-run block
if __name__ == "__main__":
    
    print(f"\"{module_name}\" module begins.")
    
    F8 = pd.DataFrame(soi['series'][11], soi['tStamp'])
    F4 = pd.DataFrame(soi['series'][3], soi['tStamp'])
    Fz = pd.DataFrame(soi['series'][16], soi['tStamp'])

    fig, ax = plt.subplots(3, figsize=[15, 25])
    
    ax[0].plot(F8)
    ax[0].set_xlim([soi['tStamp'].min(), soi['tStamp'].max()])
    ax[0].axhline(F8[0].mean(), color='r', linestyle='--', label='Mean')
    ax[0].set_title('F8')
    ax[0].legend()
    ax[0].set_xlabel('Timestamp (µs)')
    ax[0].set_ylabel('Signal (µV)')
    
    ax[1].plot(F4)
    ax[1].set_xlim([soi['tStamp'].min(), soi['tStamp'].max()])
    ax[1].axhline(F4[0].mean(), color='r', linestyle='--', label='Mean')
    ax[1].set_title('F4')
    ax[1].legend()
    ax[1].set_xlabel('Timestamp (µs)')
    ax[1].set_ylabel('Signal (µV)')
    
    ax[2].plot(Fz)
    ax[2].set_xlim([soi['tStamp'].min(), soi['tStamp'].max()])
    ax[2].axhline(Fz[0].mean(), color='r', linestyle='--', label='Mean')
    ax[2].set_title('Fz')
    ax[2].legend()
    ax[2].set_xlabel('Timestamp (µs)')
    ax[2].set_ylabel('Signal (µV)')
    
    #TEST Code
    main()
# %%
