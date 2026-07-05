# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import classification_report

import warnings
warnings.filterwarnings('ignore')

def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed']) 
    plt.show() 
    

datafile1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"

data = pd.read_csv(datafile1)

print(data.head())

datafile2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'
X = pd.read_csv(datafile2)

print(X.head(100))

################### TASK 1

# Create a NumPy array from the column Class in data, by applying the method to_numpy() then assign it to the variable Y,make sure the output is a Pandas series (only one bracket df['name of column']).

Y = data['Class'].to_numpy()
print(Y.dtype)

#################  TASK 2

# Standardize the data in X then reassign it to the variable X using the transform provided below.

# students get this 
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X) 
print(X)

# We split the data into training and testing data using the function train_test_split. The training data is divided into validation data, a second set used for training data; then the models are trained and hyperparameters are selected using the function GridSearchCV.

################# TASK 3

# Use the function train_test_split to split the data X and Y into training and test data. Set the parameter test_size to 0.2 and random_state to 2. The training data and test data should be assigned to the following labels.

# X_train, X_test, Y_train, Y_test

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state = 2)

# we can see we only have 18 test samples.

Y_test.shape

################## TASK 4

# Create a logistic regression object then create a GridSearchCV object logreg_cv with cv = 10. Fit the object to find the best parameters from the dictionary parameters.

parameters ={'C':[0.01,0.1,1],
             'penalty':['l2'],
             'solver':['lbfgs']} # l1 lasso l2 ridge
             
lr=LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters, cv=10)
logreg_cv.fit(X_train, Y_train)            

# We output the GridSearchCV object for logistic regression. We display the best parameters using the data attribute best_params_ and the accuracy on the validation data using the data attribute best_score_.

print("tuned hyperparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_)

################# TASK 5

# Calculate the accuracy on the test data using the method score:

print("Logistic Regression test data accuracy :",logreg_cv.score(X_test, Y_test))

# Lets look at the confusion matrix:

yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

#      N   3   3
# True 
#      P   0   12
#          N    P
#         Predicted

# TN = 3, TP = 12, FP = 3, FN = 0 

# Examining the confusion matrix, we see that logistic regression can distinguish between the different classes. We see that the problem is false positives.

# Overview:

# True Postive - 12 (True label is landed, Predicted label is also landed)

# False Postive - 3 (True label is not landed, Predicted label is landed)

################ TASK 6

# Create a support vector machine object then create a GridSearchCV object svm_cv with cv = 10. Fit the object to find the best parameters from the dictionary parameters.

parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}
svm = SVC()

svm_cv = GridSearchCV(svm, parameters, cv= 10)
svm_cv.fit(X_train, Y_train)

print("tuned hyperparameters :(best parameters) ",svm_cv.best_params_)
print("accuracy :",svm_cv.best_score_)

################## TASK 7

# Calculate the accuracy on the test data using the method score:

print("SVM test data accuracy :",svm_cv.score(X_test, Y_test))

# We can plot the confusion matrix

yhat=svm_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

#      N   3   3
# True 
#      P   0   12
#          N    P
#         Predicted

# TN = 3, TP = 12, FP = 3, FN = 0 


################# TASK 8

# Create a decision tree classifier object then create a GridSearchCV object tree_cv with cv = 10. Fit the object to find the best parameters from the dictionary parameters.


parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}

tree = DecisionTreeClassifier()

tree_cv = GridSearchCV(tree, parameters, cv= 10)
tree_cv.fit(X_train, Y_train)

print("tuned hyperparameters :(best parameters) ",tree_cv.best_params_)
print("accuracy :",tree_cv.best_score_)

#################### TASK 9

# Calculate the accuracy of tree_cv on the test data using the method score:

print("Decision Tree accuracy on test set :",tree_cv.score(X_test, Y_test))

# We can plot the confusion matrix

yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

#      N   5   1
# True 
#      P   0   12
#          N    P
#         Predicted

# TN = 5, TP = 12, FP = 1, FN = 0 


########################### TASK 10

# Create a k nearest neighbors object then create a GridSearchCV object knn_cv with cv = 10. Fit the object to find the best parameters from the dictionary parameters.

parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}

KNN = KNeighborsClassifier()

knn_cv = GridSearchCV(KNN, parameters, cv= 10)
knn_cv.fit(X_train, Y_train)

print("tuned hyperparameters :(best parameters) ",knn_cv.best_params_)
print("accuracy :",knn_cv.best_score_)


##################### TASK 11

# Calculate the accuracy of knn_cv on the test data using the method score:

knn_cv.score(X_test, Y_test)

# We can plot the confusion matrix

yhat = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

#      N   3   3
# True 
#      P   0   12
#          N    P
#         Predicted

# TN = 3, TP = 12, FP = 3, FN = 0 

######################## TASK 12

# Find the method performs best:

print("Logistic Regression:")
yhat = logreg_cv.predict(X_test)
print(classification_report(Y_test, yhat))

print("SVM:")
yhat = svm_cv.predict(X_test)
print(classification_report(Y_test, yhat))

print("Decision Tree Classifier:")
yhat = tree_cv.predict(X_test)
print(classification_report(Y_test, yhat))

print("kNN:")
yhat = knn_cv.predict(X_test)
print(classification_report(Y_test, yhat))

# Logistic Regression:
              # precision    recall  f1-score   support

           # 0       1.00      0.50      0.67         6
           # 1       0.80      1.00      0.89        12

    # accuracy                           0.83        18
   # macro avg       0.90      0.75      0.78        18
# weighted avg       0.87      0.83      0.81        18

# SVM:
              # precision    recall  f1-score   support

           # 0       1.00      0.50      0.67         6
           # 1       0.80      1.00      0.89        12

    # accuracy                           0.83        18
   # macro avg       0.90      0.75      0.78        18
# weighted avg       0.87      0.83      0.81        18

# Decision Tree Classifier:
              # precision    recall  f1-score   support

           # 0       1.00      0.83      0.91         6
           # 1       0.92      1.00      0.96        12

    # accuracy                           0.94        18
   # macro avg       0.96      0.92      0.93        18
# weighted avg       0.95      0.94      0.94        18

# kNN:
              # precision    recall  f1-score   support

           # 0       1.00      0.50      0.67         6
           # 1       0.80      1.00      0.89        12

    # accuracy                           0.83        18
   # macro avg       0.90      0.75      0.78        18
# weighted avg       0.87      0.83      0.81        18

# Decision Tree Classifier performs better than the other three methods, but needs a few reruns to get the good result

