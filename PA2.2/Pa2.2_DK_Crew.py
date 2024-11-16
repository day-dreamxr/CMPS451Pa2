#Version: v0.1
#Date Last Updated: 11-8-2024

#%% MODULE BEGINS
module_name = 'DK Crew'

'''
Version: 1

Description:
    PA2.2

Authors:
    Zachary Gros, Stephen Legnon

Date Created     :  11/8/2024
Date Last Updated:  11/8/2024

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
import pickle as pckl
from scipy.signal import butter, filtfilt, iirfilter
import matplotlib.pyplot as plt
import numpy as np

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
#%%
def main():
    print(f"\"{module_name}\" module begins.")
    
    ## Stream streams
    F8 = soi['series'][11]
    F4 = soi['series'][3]
    Fz = soi['series'][16]

    ## Notch filter
    notchFilter1 = butter(1, [59,61], btype='bandstop', fs=1000)
    notchFilter2 = butter(1, [119,121], btype='bandstop', fs=1000)
    notchFilter3 = butter(1, [179,181], btype='bandstop', fs=1000)
    notchFilter4 = butter(1, [239,241], btype='bandstop', fs=1000)

    F8Notch = filtfilt(notchFilter1[0], notchFilter1[1], F8)
    F8Notch = filtfilt(notchFilter2[0], notchFilter2[1], F8Notch)
    F8Notch = filtfilt(notchFilter3[0], notchFilter3[1], F8Notch)
    F8Notch = filtfilt(notchFilter4[0], notchFilter4[1], F8Notch)

    F4Notch = filtfilt(notchFilter1[0], notchFilter1[1], F4)
    F4Notch = filtfilt(notchFilter2[0], notchFilter2[1], F4Notch)
    F4Notch = filtfilt(notchFilter3[0], notchFilter3[1], F4Notch)
    F4Notch = filtfilt(notchFilter4[0], notchFilter4[1], F4Notch)

    FzNotch = filtfilt(notchFilter1[0], notchFilter1[1], Fz)
    FzNotch = filtfilt(notchFilter2[0], notchFilter2[1], FzNotch)
    FzNotch = filtfilt(notchFilter3[0], notchFilter3[1], FzNotch)
    FzNotch = filtfilt(notchFilter4[0], notchFilter4[1], FzNotch)

    ## Then Impedance filter
    impedanceFilter = butter(1, [124,126], btype='bandstop', fs=1000)
    F8Impedance = filtfilt(impedanceFilter[0], impedanceFilter[1], F8Notch)
    F4Impedance = filtfilt(impedanceFilter[0], impedanceFilter[1], F4Notch)
    FzImpedance = filtfilt(impedanceFilter[0], impedanceFilter[1], FzNotch)

    ## Then Band Pass filter
    bandPassFilter = butter(1, [0.5,32], btype='bandpass', fs=1000)
    F8Bandpass = filtfilt(bandPassFilter[0], bandPassFilter[1], F8Impedance)
    F4Bandpass = filtfilt(bandPassFilter[0], bandPassFilter[1], F4Impedance)
    FzBandpass = filtfilt(bandPassFilter[0], bandPassFilter[1], FzImpedance)

    ## Rereference Data
    F8Bandpass = F8Bandpass - np.mean(F8Bandpass)  
    F4Bandpass = F4Bandpass - np.mean(F4Bandpass)  
    FzBandpass = FzBandpass - np.mean(FzBandpass)  

    ## Plotting the streams
    plt.figure(1).set_figwidth(20)
    plt.title('F8 Original')
    plt.plot(F8)

    plt.figure(2).set_figwidth(20)
    plt.title('F8 Filtered')
    plt.plot(F8Bandpass)

    plt.figure(3).set_figwidth(20)
    plt.title('F4 Original')
    plt.plot(F4)

    plt.figure(4).set_figwidth(20)
    plt.title('F4 Filtered')
    plt.plot(F4Bandpass)

    plt.figure(5).set_figwidth(20)
    plt.title('Fz Original')
    plt.plot(Fz)

    plt.figure(6).set_figwidth(20)
    plt.title('Fz Filtered')
    plt.plot(FzBandpass)
#

#%% MAIN CODE                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main code start here

with open(soi_file, 'rb') as fp:
    soi = pckl.load(fp)
#

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main Self-run block
if __name__ == "__main__":
    #TEST Code
    main()
# %%
