#Version: v0.1
#Date Last Updated: 12-20-2023

#%% MODULE BEGINS
module_name = 'Project_DK_Crew'

'''
Authors:
    Zachary Gros, Stephen Legnon

Date Created     :  12/5/2024
Date Last Updated:  12/6/2024
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
   import os
   #os.chdir("./../..")
#

#custom imports
import pickle as pckl
from scipy.signal import butter, filtfilt, iirfilter
import math
from scipy.stats import skew, kurtosis
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from mpl_toolkits import mplot3d
from scipy.cluster.hierarchy import dendrogram, linkage

#other imports
from   copy       import deepcopy as dpcpy

from   matplotlib import pyplot as plt
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
def kMeansPCAVisualization(data, dataType):
  ##PCA Components
  pca = PCA(n_components=3)
  principalComponents = pca.fit_transform(data[['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']])
  principalDf = pd.DataFrame(data = principalComponents, columns = ['pc1', 'pc2', 'pc3'])

  ##KMeans Clustering
  kmeans = KMeans(n_clusters=2)
  kmeans.fit(principalDf)
  labels = kmeans.labels_
  principalDf['cluster'] = labels

  ##Plot KMeans
  fig = plt.figure(figsize=(8, 6))
  ax = plt.axes(projection='3d')
  ax.scatter(xs=principalDf['pc1'], ys=principalDf['pc2'], zs=principalDf['pc3'], c=principalDf['cluster'])
  ax.set_title('KMeans Clustering '+ dataType +' (PCA Visualization)')
  ax.set_xlabel('Principal Component 1')
  ax.set_ylabel('Principal Component 2')
  ax.set_zlabel('Principal Component 3')
  fig.savefig('OUTPUT\\'+dataType+'_KMeans.png')
#

def hierarchicalPCAVisualization(data, dataType):
  ##PCA Components
  pca = PCA(n_components=3)
  principalComponents = pca.fit_transform(data[['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']])
  principalDf = pd.DataFrame(data = principalComponents, columns = ['pc1', 'pc2', 'pc3'])
  Z = linkage(principalDf, method='ward')

  ##Hierarchical Clustering 
  hierachical = AgglomerativeClustering(n_clusters=2)
  hierachical.fit(principalDf)
  labels = hierachical.labels_

  ##Plot Hierarchical
  fig = plt.figure(figsize=(8, 6))
  ax = plt.axes(projection='3d')
  ax.scatter(xs=principalDf['pc1'], ys=principalDf['pc2'], zs=principalDf['pc3'], c=principalDf['cluster'])
  ax.set_title('Hierarchical Clustering '+ dataType +' (PCA Visualization)')
  ax.set_xlabel('Principal Component 1')
  ax.set_ylabel('Principal Component 2')
  ax.set_zlabel('Principal Component 3')
  fig.savefig('OUTPUT\\'+dataType+'_Hierarchical.png')
  
  den = plt.figure(figsize=(8, 6))
  ax1 = plt.axes()
  dendrogram(Z)
  ax1.set_title(dataType+' Data Cluster Dendrogram')
  ax1.set_xlabel('Cluster Number')
  ax1.set_ylabel('Cluster Proximity')
  den.savefig('OUTPUT\\'+dataType+'_Hierarchical_Dendrogram.png')
#

def main():
    #PA2.1
    print(f"PA2.1")
    print(f"\"{module_name}\" module begins.")
    print(f"Sampling Rate: {soi['info']['eeg_info']['effective_srate']}")
    print(f"Min and Max Timestamp: {soi['tStamp'].min()}, {soi['tStamp'].max()}")
    
    F8 = pd.DataFrame(soi['series'][11], soi['tStamp'], columns=['Signals'])
    F8.index.name = 'Timestamps'
    F4 = pd.DataFrame(soi['series'][3], soi['tStamp'], columns=['Signals'])
    F4.index.name = 'Timestamps'
    Fz = pd.DataFrame(soi['series'][16], soi['tStamp'], columns=['Signals'])
    Fz.index.name = 'Timestamps'
    
    F8.to_csv('OUTPUT\\F8_raw.csv')
    F4.to_csv('OUTPUT\\F4_raw.csv')
    Fz.to_csv('OUTPUT\\Fz_raw.csv')

    fig, ax = plt.subplots(3, figsize=[15, 25])
    
    ax[0].plot(soi['series'][11])
    ax[0].axhline(F8['Signals'].mean(), color='r', linestyle='--', label='Mean')
    ax[0].set_title('F8')
    ax[0].legend()
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Signal (µV)')
    
    ax[1].plot(soi['series'][3])
    ax[1].axhline(F4['Signals'].mean(), color='r', linestyle='--', label='Mean')
    ax[1].set_title('F4')
    ax[1].legend()
    ax[1].set_xlabel('Time')
    ax[1].set_ylabel('Signal (µV)')
    
    ax[2].plot(soi['series'][16])
    ax[2].axhline(Fz['Signals'].mean(), color='r', linestyle='--', label='Mean')
    ax[2].set_title('Fz')
    ax[2].legend()
    ax[2].set_xlabel('Time')
    ax[2].set_ylabel('Signal (µV)')
    
    fig.savefig("OUTPUT\\Original_Plots.png")
    
    #PA2.2
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
    F8Filtered = F8Bandpass - np.mean(F8Bandpass)  
    F4Filtered = F4Bandpass - np.mean(F4Bandpass)  
    FzFiltered = FzBandpass - np.mean(FzBandpass)  

    ## Plotting the streams
    fig, ax = plt.subplots(3, figsize=[15, 25])
    
    ax[0].plot(F8Filtered)
    ax[0].set_title('F8 Filtered')

    ax[1].plot(F4Filtered)
    ax[1].set_title('F4 Filtered')

    ax[2].plot(FzFiltered)
    ax[2].set_title('Fz Filtered')
    
    fig.savefig("OUTPUT\\Filtered_Streams.png")
    
    #PA3
    subjects = sorted(os.listdir("INPUT"), key=len)
    L = 100
    
    trainingData = pd.DataFrame(columns=['FILENAME', 'SUBJECT', 'SESSION', 'CHANNEL', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'])
    testData = pd.DataFrame(columns=['FILENAME', 'SUBJECT', 'SESSION', 'CHANNEL', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'])

    trainingData.index.name = 'OBJECT ID'
    testData.index.name = 'OBJECT ID'
    
    for subject in subjects:
        if not os.path.isdir("INPUT\\"+subject):
            break
        sessions = sorted(os.listdir("INPUT\\"+subject), key=len)
        for session in sessions:
            files = sorted(os.listdir("INPUT\\"+subject+"\\"+session), key=len)
            for file in files:
                with open("INPUT\\"+subject+"\\"+session+"\\"+file, 'rb') as fp:
                    currFile = pckl.load(fp)
                #
                for i in [11, 3, 16]:
                    stream = currFile['series'][i]
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
                    if subject == 'sb1':
                        trainingData.loc[len(trainingData.index)] = [file, subject, session, soi['info']['eeg_info']['channels'][i]['label'], f1, f2, f3, f4, f5, f6, f7, f8]
                    #
                    elif subject == 'sb2':
                        testData.loc[len(testData.index)] = [file, subject, session, soi['info']['eeg_info']['channels'][i]['label'], f1, f2, f3, f4, f5, f6, f7, f8]
                    #
                #
            #
        #
        
    #
    
    ##CONVERT DATAFRAME TO CSV
    trainingData.to_csv('OUTPUT\\TrainValidateData.csv')
    testData.to_csv('OUTPUT\\TestData.csv')
    
    #PLOT DATA
    vPlotTrain, ax = plt.subplots(1)
    ax.violinplot(dataset=trainingData[['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']], showmeans=True)

    ax.set_title(label="Generated Features From Training Data")
    ax.set_xlabel("Feature Number")
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8])
    ax.set_xticklabels(['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'])
    vPlotTrain.savefig('OUTPUT\\vPlotTrainValidate.png')
    
    vPlotTest, ax = plt.subplots(1)
    ax.violinplot(dataset=testData[['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']], showmeans=True)

    ax.set_title(label="Generated Features From Test Data")
    ax.set_xlabel("Feature Number")
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8])
    ax.set_xticklabels(['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'])
    vPlotTest.savefig('OUTPUT\\vPlotTest.png')
    
    hPlotsTrain, axs = plt.subplots(nrows=2, ncols=4, constrained_layout=True, figsize=[15, 7])
    hPlotsTrain.suptitle("Histograms of Each Feature Generated From Training Data")
    axs[0][0].hist(trainingData['F1'])
    axs[0][0].set_title("F1")
    axs[0][1].hist(trainingData['F2'])
    axs[0][1].set_title("F2")
    axs[0][2].hist(trainingData['F3'])
    axs[0][2].set_title("F3")
    axs[0][3].hist(trainingData['F4'])
    axs[0][3].set_title("F4")
    axs[1][0].hist(trainingData['F5'])
    axs[1][0].set_title("F5")
    axs[1][1].hist(trainingData['F6'])
    axs[1][1].set_title("F6")
    axs[1][2].hist(trainingData['F7'])
    axs[1][2].set_title("F7")
    axs[1][3].hist(trainingData['F8'])
    axs[1][3].set_title("F8")
    hPlotsTrain.savefig('OUTPUT\\hPlotsTrainValidate.png')
    
    hPlotsTest, axs = plt.subplots(nrows=2, ncols=4, constrained_layout=True, figsize=[15, 7])
    hPlotsTest.suptitle("Histograms of Each Feature Generated From Test Data")
    axs[0][0].hist(testData['F1'])
    axs[0][0].set_title("F1")
    axs[0][1].hist(testData['F2'])
    axs[0][1].set_title("F2")
    axs[0][2].hist(testData['F3'])
    axs[0][2].set_title("F3")
    axs[0][3].hist(testData['F4'])
    axs[0][3].set_title("F4")
    axs[1][0].hist(testData['F5'])
    axs[1][0].set_title("F5")
    axs[1][1].hist(testData['F6'])
    axs[1][1].set_title("F6")
    axs[1][2].hist(testData['F7'])
    axs[1][2].set_title("F7")
    axs[1][3].hist(testData['F8'])
    axs[1][3].set_title("F8")
    hPlotsTest.savefig('OUTPUT\\hPlotsTest.png')
    
    #PA4
    kMeansPCAVisualization(trainingData, 'Training')
    kMeansPCAVisualization(testData, 'Testing')

    hierarchicalPCAVisualization(trainingData, 'Training')
    hierarchicalPCAVisualization(testData, 'Testing')
    pass
#

#%% MAIN CODE                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main code start here
with open("INPUT\\"+soi_file, 'rb') as fp:
    soi = pckl.load(fp)
#


#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main Self-run block
if __name__ == "__main__":
    
    print(f"\"{module_name}\" module begins.")
    
    #TEST Code
    main()