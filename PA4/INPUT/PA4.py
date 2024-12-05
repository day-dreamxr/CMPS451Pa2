#%% MODULE BEGINS
module_name = 'PA4 DK Crew'

'''
Version: <***>

Description:
    <***>

Authors:
    Zachary Gros
    Stephen Legnon

Date Created     :  11/27/2024
Date Last Updated:  12/01/2024

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
from   matplotlib import pyplot as plt
import os
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA

#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Global declarations Start Here



#Class definitions Start Here


#Function definitions Start Here
def kMeansPCAVisualization(data, dataType):
  ##PCA Components
  pca = PCA(n_components=2)
  principalComponents = pca.fit_transform(data[['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']])
  principalDf = pd.DataFrame(data = principalComponents, columns = ['pc1', 'pc2'])

  ##KMeans Clustering
  kmeans = KMeans(n_clusters=2)
  kmeans.fit(principalDf)
  labels = kmeans.labels_
  principalDf['cluster'] = labels

  ##Plot KMeans
  plt.figure(figsize=(8, 6))
  sns.scatterplot(x='pc1', y='pc2', hue='cluster', data=principalDf, palette='viridis')
  plt.title('KMeans Clustering '+ dataType +' (PCA Visualization)')
  plt.xlabel('Principal Component 1')
  plt.ylabel('Principal Component 2')
  plt.show()
  plt.savefig('OUTPUT\\'+dataType+'_KMeans.png')
#

def hierarchicalPCAVisualization(data, dataType):
  ##PCA Components
  pca = PCA(n_components=2)
  principalComponents = pca.fit_transform(data[['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']])
  principalDf = pd.DataFrame(data = principalComponents, columns = ['pc1', 'pc2'])

  ##Hierarchical Clustering 
  hierachical = AgglomerativeClustering(n_clusters=2)
  hierachical.fit(principalDf)
  labels = hierachical.labels_
  principalDf['cluster'] = labels

  ##Plot Hierarchical
  plt.figure(figsize=(8, 6))
  sns.scatterplot(x='pc1', y='pc2', hue='cluster', data=principalDf, palette='viridis')
  plt.title('Hierarchical Clustering '+ dataType +' (PCA Visualization)')
  plt.xlabel('Principal Component 1')
  plt.ylabel('Principal Component 2')
  plt.show()
  plt.savefig('OUTPUT\\'+dataType+'_Hierarchical.png')
#

def main():
  trainingData = pd.read_csv('INPUT\\TrainValidateData.csv')
  testData = pd.read_csv('INPUT\\TestData.csv')

  kMeansPCAVisualization(trainingData, 'Training')
  kMeansPCAVisualization(testData, 'Testing')

  hierarchicalPCAVisualization(trainingData, 'Training')
  hierarchicalPCAVisualization(testData, 'Testing')
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

# Assessment 
# It seems as though for both the Kmeans and hierarchical clustering that any data
# that falls in the center ends up being fully clustered into one or the other without
# much overlap until there is a noticeable separation between the principal component 1
# and 2. PCA analysis was used on the 8 feature dataset so that it could more easily 
# clustered and visualized while still taking into account the overall features from the 
# data set. 