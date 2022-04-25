#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 20:28:33 2022

@author: Anna
"""

"""
TO DO:
- run again when preprocessed completely
- change the dataset to the "preprocessed 1000"
- split according to the lab
- add subsets by gender
"""
#%% call setup file

import runpy
runpy.run_path(path_name = '/0_setup.py')

# imports sys, sklearn, numpy, os, matplotlib, pathlib
# checks versions, sets wd, sets random.seed 42, specifies plots
# defines function save_fig()

#%% necessary packages
import pandas as pd
#%% read in data

# read csv file (current version, excahnge later)
# taken from file 1, but still missing imputing and normalization -> see file 1.1 and 1.2
PISA_raw_1000 = pd.read_csv("/My Drive/PISA_Revisited/data/PISA_raw_1000.csv")

#%% new split
from sklearn.model_selection import train_test_split

X=PISA_raw_1000.drop(columns=["read_score"])
y=PISA_raw_1000["read_score"]
y=y.to_frame()


X_train, X_test_val_1_val_2, y_train, y_test_val_1_val_2 = train_test_split(X, y, test_size=3/10, random_state=42)
X_test_val_1,X_val_2, y_test_val_1, y_val_2= train_test_split(X_test_val_1_val_2,y_test_val_1_val_2, test_size=1/3, random_state=42)
X_test, y_test, X_val_1, y_val_1 = train_test_split(X_test_val_1, y_test_val_1, test_size=1/2, random_state=42)


X_test.to_csv("data/X_test.csv")
y_test.to_csv("data/y_test.csv")
X_train.to_csv("data/X_train.csv")
y_train.to_scv("data/y_train.csv")

X_val_1.to_csv("data/X_val_1.csv")
y_val_1.to_csv("data/y_val_1.csv")
X_val_2.to_csv("data/X_val_2.csv")
y_val_2.to_scv("data/y_val_2.csv")





