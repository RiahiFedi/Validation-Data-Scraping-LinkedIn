# -*- coding: utf-8 -*-
"""
Created on Mon May 24 16:00:29 2021

@author: fedir
"""

import pandas as pd
import plotly.express as px
from plotly.offline import plot
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
#%matplotlib inline
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import numpy as np
import imblearn
from collections import Counter
from tinydb import where
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from numpy import mean
from numpy import std

dataset = pd.read_csv('results_file_processed.csv')
dataset.info()

dataset['reaction'].value_counts().plot(kind='barh')
dfg = pd.DataFrame(dataset['reaction'].value_counts())
dfg['label'] = dfg.index
fig = px.bar(dfg, x= 'label', y ='reaction' )
plot(fig)

encoder_ = LabelEncoder()
for i in dataset:
    dataset[i]= encoder_.fit_transform(dataset[i])

X = dataset[['nbr_employees','work_field','region','current_job_duration','total_experience']]
X.info()
y = dataset['reaction']



oversample = SMOTE()
X, y = oversample.fit_resample(X, y)

                               

    
    
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 2)
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)

from sklearn.tree import DecisionTreeClassifier
dtree_model = DecisionTreeClassifier(max_depth = 20)

# evaluate model
scores = cross_val_score(dtree_model, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
# report performance
print('Accuracy: %.3f (%.3f)' % (mean(scores), std(scores)))


#Confusion matrix
cnf_matrix = confusion_matrix(y_test, dtree_predictions)
plt.imshow(cnf_matrix, cmap=plt.cm.Blues)

# calculate accuracy
from sklearn import metrics
print(metrics.accuracy_score(y_test, dtree_predictions))

#Receiver Operating Characteristic (ROC) Curves
y_pred_prob = dtree_model.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred_prob)

plt.plot(fpr, tpr)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.rcParams['font.size'] = 12
plt.title('ROC curve for diabetes classifier')
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.grid(True)