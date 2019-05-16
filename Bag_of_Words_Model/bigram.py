__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Smith, Steven", "Tinker, Paul",
               "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

# Modular function to apply decision tree classifier
def DT_classifier(X, Y, numFold):
    
    # Intilization of the figure
    myFig = plt.figure(figsize=[12,10])
    
    # Stratified K-Folds cross-validator
    cv = StratifiedKFold(n_splits=numFold,random_state=None, shuffle=False)
    
    # Initialization of the decision tree classifier
    classifier = tree.DecisionTreeClassifier()
    
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
    
    i = 1
    for train, test in cv.split(X, Y):
        X_train, X_test, Y_train, Y_test = X[train], X[test], Y[train], Y[test]
        probas_ = classifier.fit(X_train, Y_train).predict_proba(X_test)
        fpr, tpr, thresholds = roc_curve(Y_test, probas_[:, 1])
        tprs.append(interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        plt.plot(fpr, tpr, lw=1, color='black', alpha=0.5,
                 label='ROC fold %d (AUC = %0.3f)' % (i, roc_auc))
        print("Iteration ongoing inside DT method - KFold step: ", i)
        i += 1
        
    plt.plot([0,1],[0,1],linestyle = '--',lw = 1, alpha=0.5, color = 'black')
    
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, color='black',
             label=r'Mean ROC (AUC = %0.3f)' % (mean_auc),
             lw=2, alpha=0.8)
    
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate', fontsize=18, weight='bold')
    plt.ylabel('True Positive Rate', fontsize=18, weight='bold')
    plt.title('Receiver Operating Characteristic (ROC) Curve\nDecision Tree with Bigram Model', fontsize=20, fontweight='bold')
    plt.legend(loc="lower right",fontsize=14)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.show()
    
    fileName = 'Decision_Tree_ROC_' + str(numFold) + '_Fold.eps'
    # Saving the figure
    myFig.savefig(fileName, format='eps', dpi=1200)
    
    # Statistical measurement of the model
    results = cross_validate(estimator=classifier,
                             X=X_test,
                             y=Y_test,
                             cv=cv,
                             scoring=scoring)
    print("Decision Tree Classifier results\n", results)

# Modular function to apply decision tree classifier
def RF_classifier(X, Y, numFold):
    
    # Intilization of the figure
    myFig = plt.figure(figsize=[12,10])
    
    # Stratified K-Folds cross-validator
    cv = StratifiedKFold(n_splits=numFold,random_state=None, shuffle=False)
    
    # Initialization of the random forest classifier
    classifier = RandomForestRegressor(n_estimators = 100, random_state = 0)
    
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
    
    i = 1
    for train, test in cv.split(X, Y):
        X_train, X_test, Y_train, Y_test = X[train], X[test], Y[train], Y[test]
        probas_ = classifier.fit(X_train, Y_train).predict_proba(X_test)
        fpr, tpr, thresholds = roc_curve(Y_test, probas_[:, 1])
        tprs.append(interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        plt.plot(fpr, tpr, lw=1, color='black', alpha=0.5,
                 label='ROC fold %d (AUC = %0.3f)' % (i, roc_auc))
        print("Iteration ongoing inside RF method - KFold step: ", i)
        i += 1
        
    plt.plot([0,1],[0,1],linestyle = '--',lw = 1, alpha=0.5, color = 'black')
    
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, color='black',
             label=r'Mean ROC (AUC = %0.3f)' % (mean_auc),
             lw=2, alpha=0.8)
    
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate', fontsize=18, weight='bold')
    plt.ylabel('True Positive Rate', fontsize=18, weight='bold')
    plt.title('Receiver Operating Characteristic (ROC) Curve\nRandom Forest with Bigram Model', fontsize=20, fontweight='bold')
    plt.legend(loc="lower right",fontsize=14)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.show()
    
    fileName = 'Random_Forest_ROC_' + str(numFold) + '_Fold.eps'
    # Saving the figure
    myFig.savefig(fileName, format='eps', dpi=1200)
    
    # Statistical measurement of the model
    results = cross_validate(estimator=classifier,
                             X=X_test,
                             y=Y_test,
                             cv=cv,
                             scoring=scoring)
    print("Random Forest Classifier results\n", results)


# Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold, cross_validate
from scipy import interp
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score

from sklearn import tree
from sklearn.ensemble import RandomForestRegressor

#importing the data set
dataset = pd.read_csv('Dataset/master_dataset.csv', sep='\t')
print(dataset.head())

# Compute the length of the dataset
totalRecords = len(dataset.index)

# One Hot Encode the TLD column
df = dataset.copy(deep=True)
df = df[['TLD']]
df = pd.get_dummies(df,prefix=['TLD'])

# Concating the dataframe to main dataframe
dataset = pd.concat([dataset, df], axis=1)
dataset = dataset.drop(columns=['TLD'])
del df # clearing the memory

# Processing the domain names (text)
import re
corpus = []
for i in range(0,totalRecords):
    domains = re.sub('[.]', ' ', dataset['domain'][i])
    domains = domains.lower()
    domains = domains.split()
    domains = ' '.join(domains)
    corpus.append(domains)
    
# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(analyzer='char', ngram_range=(2, 2)) #bigram initialization
X = cv.fit_transform(corpus).toarray()  # X obtains the corups
Y_class = dataset.iloc[:,dataset.columns.get_loc("class")].values
Y_family = dataset.iloc[:,dataset.columns.get_loc("family_id")].values

# Drop two Y columns from the dataset as well as the domain string column from the dataset
dataset = dataset.drop(columns=['class', 'family_id', 'domain'])

# Concat and create the X properly for the last time
X_temp = dataset.iloc[:,:].values
X = np.column_stack([X, X_temp])

# Clear the memories
del dataset
del X_temp
del corpus

print("Data are processed, ready for classification.")

# Intializing the scoring metrics
scoring = {'accuracy' : make_scorer(accuracy_score),
           'precision' : make_scorer(precision_score),
           'recall' : make_scorer(recall_score), 
           'f1_score' : make_scorer(f1_score)}

# Calling the decision tree classifier for binary classification with
# 5-fold cross validation
DT_classifier(X, Y_class, 5)

# Calling the random forest classifier for binary classification with
# 5-fold cross validation
RF_classifier(X, Y_class, 5)