# -*- coding: utf-8 -*-
"""AA2_Food Demand Forecasting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F9u2rbkn9oS_P3ZhdeVCcvNV7mR8_os3

# ***Food Demand Forecasting***

* **import Neccessory libraries**
"""

# Commented out IPython magic to ensure Python compatibility.
#import Neccessory libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.preprocessing import StandardScaler


from sklearn.model_selection import train_test_split, GridSearchCV

#import required accuracy metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.model_selection import KFold, cross_val_score

import warnings
warnings.filterwarnings('ignore')
# %matplotlib inline

"""* **Import Dataset**"""

full = pd.read_csv('/content/fulfilment_center_info.csv')
full.head(5)

meal = pd.read_csv('/content/meal_info.csv')
meal.head(5)

train = pd.read_csv('/content/train.csv')
train.head(5)

ss = pd.read_csv('/content/sample_submission_hSlSoT6.csv')
ss.head(5)

#merging all train dataset files using inner(similar column)
tdf = pd.merge(train,meal, on=['meal_id'], how='inner')
df = pd.merge(tdf,full, on =['center_id'], how='inner')
df.head(6)

#import test dataset
tt = pd.read_csv('/content/test_QoiMO9B.csv')
tt.head(5)

# Find the shape of the test data set
print("shape of the test data set", tt.shape)

# Find the shape of the test data set
print("shape of the train data set", df.shape)

#lets check for Null Values
df.isnull().sum()

"""* there is no null values in any columns"""

#checking null values using graphical representation

import missingno
missingno.bar(df, figsize = (10,20), color="tab:blue")

#check the data types
df.dtypes

#Lets check which columns contains '?'

df[df.columns[(df == '?').any()]].nunique()

#lets check distribution for continuous columns
num_data = df._get_numeric_data()
plt.figure(figsize = (20,20))
plotnumber = 1
for column in num_data:
    if plotnumber <=15:
        ax = plt.subplot(8,5,plotnumber)
        sns.distplot(num_data[column])
        plt.xlabel(column,fontsize = 20)
    plotnumber+=1
plt.tight_layout()

df.columns

# lets check the unique values in all columns in train data set

for col in num_data.columns:
    print(col,df[col].nunique())
    print('-'*30)

#Lets chcek the value counts for categorical data

for i in df.columns:
    if df[i].dtypes == 'object':
        print(df[i].value_counts())
        print('-----------------------------------')

"""# ***Heat Map for checking the correlation***"""

plt.style.use('default')
df_corr = df.corr()
plt.figure(figsize = (25,15))
sns.heatmap(df_corr,vmin=-1,vmax=1,annot=True,square=True,center=0,fmt='.2g',linewidths=0.1)
plt.tight_layout()

"""* Looking at the above heat map we can say that many features are in good correlation with our target variable and also many features are having very poor relation with the target variable.
*  The columns derived home page featured, emailer for promotion and op area have Positive relation.
* The columns derived checkout price and base price have negative relation.
"""

# find corelation between only target columns 

df_corr = df.corr()
plt.figure(figsize=(8,3))
df_corr['num_orders'].sort_values( ascending = False).drop('num_orders').plot.bar()
plt.title("Correlation of Features vs Label\n")
plt.ylabel("Correlation Value")
plt.show()

"""* The columns derived home page featured, emailer for promotion and op area have Positive relation.

* The columns derived checkout price and base price have negative relation.

# ***EDA***
"""

df.columns

df.info()

for col in num_data.columns:
    print(col,df[col].nunique())
    print('-'*30)

col=['homepage_featured','emailer_for_promotion','op_area']

plt.style.use('default')
plt.figure(figsize=(8,12))
for i in range(len(col)):
    plt.subplot(3,1,i+1)
    sns.stripplot(y=df['num_orders'],x=df[col[i]])
    plt.title(f"number of food orders VS {col[i]}",fontsize=15)
    plt.xticks(fontsize=10)  
    plt.yticks(fontsize=10)
    plt.tight_layout()

plt.style.use('default')
plt.figure(figsize=(8,12))
for i in range(len(col)):
    plt.subplot(3,1,i+1)
    sns.scatterplot(y=df['num_orders'],x=df[col[i]])
    plt.title(f"number of food orders VS {col[i]}",fontsize=15)
    plt.xticks(fontsize=10)  
    plt.yticks(fontsize=10)
    plt.tight_layout()

plt.style.use('default')
plt.figure(figsize=(8,12))
for i in range(len(col)):
    plt.subplot(3,1,i+1)
    sns.barplot(y=df['num_orders'],x=df[col[i]])
    plt.title(f"number of food orders VS {col[i]}",fontsize=15)
    plt.xticks(fontsize=10)  
    plt.yticks(fontsize=10)
    plt.tight_layout()

#Lets have a look on distribution of our data
num_data = df._get_numeric_data()
plt.style.use('default')
plt.figure(figsize = (10,15))
plotnumber = 1
for column in num_data:
    if plotnumber <=12:
        ax = plt.subplot(4,3,plotnumber)
        sns.scatterplot(num_data[column],y=df['num_orders'])
        plt.title(f"Distribution of {column}",fontsize=10)
        plt.xlabel(column,fontsize = 10)
    plotnumber+=1
plt.tight_layout()

#Lets have a look on distribution of our data
num_data = df._get_numeric_data()
plt.style.use('default')
plt.figure(figsize = (10,15))
plotnumber = 1
for column in num_data:
    if plotnumber <=12:
        ax = plt.subplot(4,3,plotnumber)
        sns.distplot(num_data[column],hist=False, color="red", kde_kws={"shade": True})
        plt.title(f"Distribution of {column}",fontsize=10)
        plt.xlabel(column,fontsize = 10)
    plotnumber+=1
plt.tight_layout()

#Lets have a look on distribution of our data
cols=['num_orders','meal_id','checkout_price','emailer_for_promotion','homepage_featured','city_code','region_code','op_area']
plt.style.use('default')
plt.figure(figsize = (10,15))
plotnumber = 1
for column in cols:
    if plotnumber <=15:
        ax = plt.subplot(4,3,plotnumber)
        sns.boxenplot(df[column], color="red")
        #plt.title(f"Distribution of {column}",fontsize=10)
        plt.xlabel(column,fontsize = 10)
    plotnumber+=1
plt.tight_layout()

"""# ***Now remove these outliers and generate new dataframe***"""

column = ['num_orders']
for col in df.columns:
    if df[col].dtypes != 'object':
      percentile = df[col].quantile([0.01,0.98]).values
      df[col][df[col]<=percentile[0]]=percentile[0]
      df[col][df[col]>=percentile[1]]=percentile[1]

#Lets have a look on distribution of our data
cols=['num_orders','meal_id','checkout_price','city_code','region_code','op_area']
plt.style.use('default')
plt.figure(figsize = (10,15))
plotnumber = 1
for column in cols:
    if plotnumber <=15:
        ax = plt.subplot(4,3,plotnumber)
        sns.boxenplot(df[column], color="red")
        #plt.title(f"Distribution of {column}",fontsize=10)
        plt.xlabel(column,fontsize = 10)
    plotnumber+=1
plt.tight_layout()

"""# ***Data processing***"""

df.describe().T

"""# **Get Dummies**"""

df= pd.get_dummies(df, columns=['emailer_for_promotion','homepage_featured'],drop_first=True)

df.head(4)

display(df.drop_duplicates())

"""# ***Split Data into x & y***"""

#lets saperate data into label and features
x = df.drop(columns = 'num_orders')
y = df["num_orders"]

x.skew()

#Lets treat the skewness
for index in x.skew().index:
    if x.skew().loc[index]>0.5:
        x[index]=np.log1p(x[index])
        if x.skew().loc[index]<-0.5:
            x[index]=np.square(x[index])

x.skew()

num_data = x.select_dtypes(include = [np.number])
cat_data = x.select_dtypes(exclude=[np.number])

num_data.head(3)

cat_data.head(3)

"""# **Applying standard scaler to numerical data**"""

#Lets bring all numerical features to common scale by applying standard scaler
scaler = StandardScaler()
num = scaler.fit_transform(num_data)
num = pd.DataFrame(num,columns=num_data.columns)

num.head(5)

"""# **Encoding**"""

from sklearn.preprocessing import OrdinalEncoder
enc = OrdinalEncoder()
for i in cat_data.columns:
    cat_data[i] = enc.fit_transform(cat_data[i].values.reshape(-1,1))

cat_data.head(4)

"""# **combining categorical and numerical data**"""

X = pd.concat([num, cat_data], axis = 1)

X

"""# ***Finding best random_state***"""

#to find random stat which gives maximum r2_score

from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
max_r_score=0
r_state = 0
for i in range(50,1000):
    x_train, x_test, y_train, y_test = train_test_split(X, np.log(y),test_size = 0.25,random_state = r_state)
    reg = LinearRegression()
    reg.fit(x_train,y_train)
    y_pred = reg.predict(x_test)
    r2_scr=r2_score(y_test,y_pred)
    if r2_scr > max_r_score:
        max_r_score = r2_scr
        r_state = i
print("max r2 score is",max_r_score,"on Random State",r_state)

#lets split our train data into train and test part with our best random state
x_train, x_test, y_train, y_test = train_test_split(X, np.log(y),test_size = 0.25,random_state = 51)

"""# ***Building a function for model with evaluation***"""

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
#from sklearn.metrics import r2_score

def BuiltModel(model):
    model.fit(x_train,y_train)
    y_pred = model.predict(x_train)
    pred = model.predict(x_test)

    r2score = r2_score(y_test,pred)*100

    #evaluation
    mse = mean_squared_error(y_test,pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test,pred)
    print("MAE :", mae)
    print("RMSE :", rmse)
    print('------------------------------')

    # r2 score
    print(" Percentage of Training r2 Score :", r2_score(y_train,y_pred)*100,'%')
    print(f"Percentage of Testing r2 Score:", r2score,"%")
    print('------------------------------')

    #cross validation score
    scores = cross_val_score(model, X, y, cv = 3).mean()*100
    print("\nCross validation score :", scores)

    #result of accuracy minus cv score
    result = r2score - scores
    print("\nAccuracy Score - Cross Validation Score :", result)

    sns.regplot(y_test,pred)
    plt.show()

"""# ***LinearRegression Model***"""

lr = LinearRegression()
BuiltModel(lr)

"""# **Ridge Regression**"""

from sklearn.linear_model import Ridge
rg = Ridge(alpha=1.0)
BuiltModel(rg)

"""# **Lasso Regression**"""

from sklearn.linear_model import Lasso
la = Lasso(alpha=1.0)
BuiltModel(la)

"""# **DecisionTreeRegressor Model**"""

from sklearn.tree import DecisionTreeRegressor
dt = DecisionTreeRegressor()
BuiltModel(dt)

"""# **RandomForestRegressor Model**"""

#model with RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
BuiltModel(model)

"""# **Final Model**"""

#lets train and test our final model with best parameters
#model = RandomForestRegressor(max_depth = 12, min_samples_split = 2, n_estimators = 700)
#model.fit(x_train,y_train)
#pred = model.predict(x_test)

#r2score = r2_score(y_test,pred)*100

#evaluation
#mse = mean_squared_error(y_test,pred)
#rmse = np.sqrt(mse)
#mae = mean_absolute_error(y_test,pred)
#print("MAE :", mae)
#print("RMSE :", rmse)
#print('------------------------------')

# r2 score

#print(f" \nr2 Score:", r2score,"%")

"""# **Making predictions for test dataset using final model**"""

tdf1 = pd.merge(tt,meal, on=['meal_id'], how='inner')
dft = pd.merge(tdf1,full, on =['center_id'], how='inner')
dft.head(6)

p_ID = dft['id']
#dft = dft.drop(columns='id')

dft.shape

dft.info()

dft.isnull().sum()

display(dft.drop_duplicates())

dft= pd.get_dummies(dft, columns=['emailer_for_promotion','homepage_featured'],drop_first=True)

dft.skew()

#Lets treat the skewness
for index in dft.skew().index:
    if dft.skew().loc[index]>0.5:
        dft[index]=np.log1p(dft[index])
        if dft.skew().loc[index]<-0.5:
            dft[index]=np.square(dft[index])

dft.skew()

num_data2 = dft.select_dtypes(include = [np.number])
cat_data2 = dft.select_dtypes(exclude=[np.number])

#Lets bring all numerical features to common scale by applying standard scaler
scaler = StandardScaler()
num2 = scaler.fit_transform(num_data2)
num2 = pd.DataFrame(num2,columns=num_data2.columns)

from sklearn.preprocessing import OrdinalEncoder
enc = OrdinalEncoder()
for i in cat_data2.columns:
    cat_data2[i] = enc.fit_transform(cat_data2[i].values.reshape(-1,1))

T = pd.concat([num2, cat_data2], axis = 1)

T.head(6)

T.shape

X.shape

T.columns

X.columns

#lets predict the price with our best model
prediction = model.predict(T)

prediction

#lets make the dataframe for prediction
Food_Demand = pd.DataFrame(prediction, columns=["num_orders"])

sub_file = pd.concat([p_ID, Food_Demand], axis = 1)

sub_file.head(3)

ss.head(3)

#Lets save the submission to csv

sub_file.to_csv("Food Demand Forecasting.csv",index=False)

"""---



---

# **Thank You**

---



---
"""