import pandas as pd
import numpy as np

class univariate():

    def QuanQual(dataset):
        Qual = []
        Quan = []
        for ColumnName in dataset.columns:
            if dataset[ColumnName].dtype == "O":
                Qual.append(ColumnName)
            else:
                Quan.append(ColumnName)
        return Qual,Quan
        
    # Frequency Function
    def Frequency(ColumnName,dataset):
        freqTable = pd.DataFrame(columns = ["Unique Values","Frequency","Relative Frequency","Cusum"])
        freqTable["Unique Values"] = dataset[ColumnName].value_counts().index
        freqTable["Frequency"] = dataset[ColumnName].value_counts().values
        freqTable["Relative Frequency"] = (freqTable["Frequency"]/len(dataset[ColumnName].value_counts()))
        freqTable["Cusum"] = freqTable["Relative Frequency"].cumsum()
        return freqTable

    # Descriptive Function
    def Descriptive_Table(dataset,quan):
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","IQR","1.5_Rule",
                                    "Lesser_range","Greater_range","Min","Max"],columns=quan)
        for ColumnName in quan:
            descriptive[ColumnName]["Mean"] = dataset[ColumnName].mean()
            descriptive[ColumnName]["Median"] = dataset[ColumnName].median()
            descriptive[ColumnName]["Mode"] = dataset[ColumnName].mode()[0]
            descriptive[ColumnName]["Q1:25%"] = dataset.describe()[ColumnName]["25%"]
            descriptive[ColumnName]["Q2:50%"] = dataset.describe()[ColumnName]["50%"]
            descriptive[ColumnName]["Q3:75%"] = dataset.describe()[ColumnName]["75%"]
            descriptive[ColumnName]["99%"] = np.percentile(dataset[ColumnName],99)
            descriptive[ColumnName]["Q4:100%"] = dataset.describe()[ColumnName]["max"]
            descriptive[ColumnName]["IQR"] = descriptive[ColumnName]["Q3:75%"]-descriptive[ColumnName]["Q1:25%"]
            descriptive[ColumnName]["1.5_Rule"] = 1.5* descriptive[ColumnName]["IQR"]
            descriptive[ColumnName]["Lesser_range"] = descriptive[ColumnName]["Q1:25%"]-descriptive[ColumnName]["1.5_Rule"]
            descriptive[ColumnName]["Greater_range"] = descriptive[ColumnName]["Q3:75%"]+descriptive[ColumnName]["1.5_Rule"]
            descriptive[ColumnName]["Min"] = dataset[ColumnName].min()
            descriptive[ColumnName]["Max"] = dataset[ColumnName].max()
        return descriptive

    # Outliers function
    def Outlier_Columns(descriptive,quan):
        Lesser_outlier = []
        Greater_outlier = []
        for ColumnName in quan:
            if descriptive[ColumnName]["Min"]<descriptive[ColumnName]["Lesser_range"]:
                Lesser_outlier.append(ColumnName)
            if descriptive[ColumnName]["Max"]>descriptive[ColumnName]["Greater_range"]:
                Greater_outlier.append(ColumnName)
        return Lesser_outlier,Greater_outlier

    # Outlier handling function
    def Replace_Outliers(Lesser_outlier,Greater_outlier,descriptive,dataset):
        for ColumnName in Lesser_outlier:
            dataset[ColumnName][dataset[ColumnName]<descriptive[ColumnName]["Lesser_range"]]=descriptive[ColumnName]["Lesser_range"]
        for ColumnName in Greater_outlier:
            dataset[ColumnName][dataset[ColumnName]>descriptive[ColumnName]["Greater_range"]]=descriptive[ColumnName]["Greater_range"]

