#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 16:11:16 2022

@author: Jo
"""

#%% packages

from matplotlib.pyplot import xticks, yticks
import pandas as pd

#%% evaluation of the best model (ridge tuned) on the test set

X_test = pd.read_csv("data/X_test.csv")
y_test = pd.read_csv("data/y_test.csv")

# check dimensions -> dimensions should be 205 columns in X and 1 in y
def drop_first_entry(df):
    df.drop(df.columns[[0]], axis = 1, inplace = True)

drop_first_entry(X_test)
drop_first_entry(y_test)

# evaluate the best model on the test set... see the final score!
# load the best model
import joblib
final_model = joblib.load("models/final_ridge_model.pkl")

# prediction for X_test
y_pred = final_model.predict(X_test)

# save predictions as csv
# y_pred_values = pd.DataFrame(y_pred)
# y_pred_values.to_csv("data/y_pred.csv")

# evaluate
lin_reg_mse = mean_squared_error(y_test, y_pred)
lin_reg_rmse = np.sqrt(lin_reg_mse)
print(lin_reg_rmse)
 # result: 69.0934592678894


#%% plotting predicted vs. actual values


y_test = pd.read_csv('/Volumes/GoogleDrive-106144065181021449893/Meine Ablage/Data/y_test.csv')
y_pred = pd.read_csv('/Volumes/GoogleDrive-106144065181021449893/Meine Ablage/Data/y_pred.csv')

drop_first_entry(y_pred)
drop_first_entry(y_test)

merged = []
merged["y_test"] = y_test

y_pred["y_test"] = y_test

#Matplotlib Version (incomplete)
# plt.figure(figsize=(10,10))
# plt.scatter(y_test, y_pred, c='crimson', alpha=0.2)
# plt.yscale('log')
# plt.xscale('log')

# p1 = max(max(y_pred), max(y_test)
# p2 = min(min(y_pred), min(y_test)
# plt.plot([p1, p2], [p1, p2], 'red')
# plt.xlabel('True Values', fontsize=15)
# plt.ylabel('Predicted Values', fontsize=15)
# plt.xticks(ticks=500, 100000)
# plt.yticks(ticks=500, 10000)
# plt.axis('equal')
# plt.title('Scatterplot of Predicted and True Values',fontdict={'fontsize': 20})
# plt.show()

#Seaborn Version (better)
scatter = sns.lmplot(x = '0', y = 'y_test' , data = y_pred, scatter_kws={'alpha':0.2}, line_kws={'color': 'red'})
scatter.set(yticklabels=[]) 
scatter.set(xticklabels=[]) 
plt.title('Scatterplot of Predicted and True Values')
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.show()
plt.savefig('seaborn_pred.png',dpi='400')


#%% fit model on boys and girls subset and check feature importance to find the best predictors

# read in boys and girls subsets
X_female = pd.read_csv("data/X_female.csv")
y_female = pd.read_csv("data/y_female.csv")

X_male = pd.read_csv("data/X_male.csv")
y_male = pd.read_csv("data/y_male.csv")

# if needed, drop first entries
def drop_first_entry(df):
    df.drop(df.columns[[0]], axis = 1, inplace = True)

drop_first_entry(X_female)
drop_first_entry(y_female)
drop_first_entry(X_male)
drop_first_entry(y_male)


import joblib
final_model = joblib.load("models/final_ridge_model.pkl")

####################################

# fit the model to girls
final_model.fit(X_female, y_female)

# choose ridge regression as a step in the model pipeline and get coefficients
coefficients = final_model.named_steps['ridge'].coef_

# reshape row to column and get feature names
coefficients = coefficients.reshape(-1, 1)
feature_names = X_female.columns

# generate dataframe combining coefficients and column names
predictors = pd.DataFrame(coefficients, feature_names)
zipped = list(zip(feature_names, coefficients))
predictors = pd.DataFrame(zipped, columns=["feature", "coefficient"])

# sort by the absolute value of coefficients
predictors = predictors.sort_values('coefficient', ascending=False, key=abs)

# filter out country-ID's (we are interested in individual features of students)
predictors_female = predictors[predictors["feature"].str.contains("CNTRYID")==False]

# save as csv
predictors_female.to_csv("data/predictors_female.csv")


#####################################

# fit the model to boys
final_model.fit(X_male, y_male)

# choose ridge regression as a step in the model pipeline to get coefficients
coefficients = final_model.named_steps['ridge'].coef_

# reshape row to column and get feature names
coefficients = coefficients.reshape(-1, 1)
feature_names = X_male.columns

# generate dataframe combining coefficients and column names
predictors = pd.DataFrame(coefficients, feature_names)
zipped = list(zip(feature_names, coefficients))
predictors = pd.DataFrame(zipped, columns=["feature", "coefficient"])

# sort by the absolute value of coefficients
predictors = predictors.sort_values('coefficient', ascending=False, key=abs)

# filter out country-ID's (we are interested in individual features of students)
predictors_male = predictors[predictors["feature"].str.contains("CNTRYID")==False]

# save as csv
predictors_male.to_csv("data/predictors_male.csv")



#%% for interpretation purposes: display predictors of genders together

PISA_prepared = pd.read_csv("data/PISA_prepared.csv")
PISA_prepared.drop(PISA_prepared.columns[[0]], axis = 1, inplace = True)
X = PISA_prepared.drop(columns=["read_score"])
y = PISA_prepared["read_score"]
y = y.to_frame()

# fit the model to all students
final_model.fit(X, y)

# choose ridge regression as a step in the model pipeline and get coefficients
coefficients = final_model.named_steps['ridge'].coef_

# reshape row to column and get feature names
coefficients = coefficients.reshape(-1, 1)
feature_names = X.columns

# generate dataframe combining coefficients and column names
predictors = pd.DataFrame(coefficients, feature_names)
zipped = list(zip(feature_names, coefficients))
predictors = pd.DataFrame(zipped, columns=["feature", "coefficient"])

# sort by the absolute value of coefficients
predictors = predictors.sort_values('coefficient', ascending=False, key=abs)

# filter out country-ID's (we are interested in individual features of students)
predictors_all = predictors[predictors["feature"].str.contains("CNTRYID")==False]

# save as csv
predictors_all.to_csv("data/predictors_all.csv")





