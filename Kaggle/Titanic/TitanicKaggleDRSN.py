
'''
Author: David Rodrigo Sánchez Navarro
Date: 12:45 GMT-5, 2020/11/21 
'''


# Datasets
import pandas as pd

df_train = pd.read_csv(r'..\2_BD\train.csv', encoding='utf-8')
df_test = pd.read_csv(r'..\2_BD\test.csv', encoding='utf-8')


# Basic dataframe's information
df_train.shape
df_test.shape

df_train.info()
df_test.info()

df_train.head()
df_test.head()

df_train.describe()
df_test.describe()


# Appending
df_train['T'] = 1
df_test['T'] = 2
df_appended = df_train.append(df_test, ignore_index=True)


# New features
# Family size
df_appended['FamilySize'] = df_appended['SibSp'] + df_appended['Parch']

# Fare per family member
df_appended['FarePFM'] = df_appended['Fare']/(df_appended['FamilySize']+1)

# Titles
df_appended['Title'] = df_appended['Name'].str.extract('([A-Za-z]+)\.')
df_appended['Title'].unique()


# Variables categóricas
df_appended.drop(columns=['Ticket', 'Cabin', 'Name'], inplace=True)
df_appended = pd.get_dummies(df_appended, columns=['Pclass', 'Sex', 'Embarked', 'Title'], drop_first=True)


# Missing data 
df_appended.isna().sum()

import missingno as msno
msno.matrix(df_appended)

df_appended['Age'].fillna(df_appended['Age'].mean(), inplace=True) 
df_appended['Fare'].fillna(df_appended['Fare'].mean(), inplace=True)
df_appended['FarePFM'].fillna(df_appended['FarePFM'].mean(), inplace=True)


# Correlation
df_appended.drop(columns=['PassengerId', 'T']).corr()

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.figure(figsize=(20, 10))

mask = np.triu(np.ones_like(df_appended.drop(columns=['PassengerId', 'T']).corr(), dtype=bool))
cmap = sns.diverging_palette(230, 10, as_cmap=True)

heatmap = sns.heatmap(
    df_appended.drop(columns=['PassengerId', 'T']).corr(), 
    mask=mask, 
    cmap=cmap, 
    vmin=-1, 
    vmax=1, 
    center=0,  
    annot=False)

heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':14}, pad=10)


# Data split
from sklearn.model_selection import train_test_split

X = df_appended[df_appended['T']==1].drop(columns=['PassengerId', 'T', 'Survived']).values
y = df_appended[df_appended['T']==1]['Survived'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# np.isnan(X_train).any()
# np.isnan(y_train).any()
# np.isnan(X_test).any()
# np.isnan(y_test).any()


# Pipeline and models
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC 
from xgboost import XGBClassifier

import keras
from keras.wrappers.scikit_learn import KerasClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score 
from sklearn.model_selection import cross_validate
from sklearn import metrics


scores = dict()

models = {
    'KNN': [
        ('KNN', KNeighborsClassifier()), 
        {
            'KNN__n_neighbors': np.arange(1,51)
        }
    ],
    'LOGREG': [
        ('LOGREG', LogisticRegression()), 
        {
            'LOGREG__C': np.logspace(-5, 8, 15)
        }
    ],
    'DETREE': [
        ('DETREE', DecisionTreeClassifier()), 
        {
            'DETREE__max_depth': [3, None], 
            'DETREE__max_features': np.arange(1, 9), 
            'DETREE__min_samples_leaf': np.arange(1, 9), 
            'DETREE__criterion': ['gini', 'entropy']
        }
    ],
    'RDFOREST': [
        ('RDFOREST', RandomForestClassifier()),
        {
            'RDFOREST__max_depth': [3, None],
            'RDFOREST__criterion': ['gini', 'entropy'],
            'RDFOREST__min_samples_leaf': np.arange(1, 9),
            'RDFOREST__max_features': np.arange(1, 9)
        }
    ],
    'SVC': [
        ('SVC', SVC()),
        {
            'SVC__C':[1, 10, 100],
            'SVC__gamma':[0.1, 0.01]
        }
    ],
    'XGBC': [
        ('XGBC', XGBClassifier()),
        {
            'XGBC__max_depth': [2, 3, 5, 7, 10],
            'XGBC__n_estimators': [10, 100, 500]
        }
    ]
}

# for x, y in models.items():
#     print((x))

for name, items in models.items():
    print('Modelo {} en proceso...'.format(name))

    steps = [
        ('imputation', SimpleImputer(missing_values=np.nan, strategy='mean')),
        ('scaler', StandardScaler()),
        items[0]
    ]

    pipeline = Pipeline(steps)

    model = GridSearchCV(pipeline, param_grid=items[1], cv=5)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    scores[name] = (
        round(metrics.accuracy_score(y_test, y_pred), 6), 
        round(metrics.roc_auc_score(y_test, y_pred), 6)
        )
    
    print('Modelo {} analizado'.format(name))

print('Fin.')


# Neural Networks
def create_network():
    nnetwork = keras.models.Sequential()

    nnetwork.add(keras.layers.Dense(units=16, activation='relu', input_shape=(28,)))
    nnetwork.add(keras.layers.Dense(units=16, activation='relu'))
    nnetwork.add(keras.layers.Dense(units=1, activation='sigmoid'))

    nnetwork.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
        )
    
    return nnetwork

NNET = KerasClassifier(build_fn=create_network, epochs=150, batch_size=100, verbose=0)
NNET_CV = cross_validate(NNET, X_train, y_train, scoring={'ACC': 'accuracy', 'AUC': 'roc_auc'}, cv=5)

scores['NNET'] = (round(np.mean(NNET_CV['test_ACC']), 6), round(np.mean(NNET_CV['test_AUC']), 6))


# Best model
print('MODEL: (Accuracy, AUC)\n')
for model, score in scores.items():
    print(f'- {model}: {score}')

results = pd.DataFrame({'Model': scores.keys(), 'ACCURACY': [x for x, _ in scores.values()], 'AUC': [y for _, y in scores.values()]}).sort_values('AUC', ascending=False)
print('\n---> Best model (AUC): {}'.format(results.iloc[0,0]))


# Fit best model - Neural Network
X_TESTING = df_appended[df_appended['T']==2].drop(columns=['PassengerId', 'T', 'Survived']).values

NNET.fit(X, y)
y_pred_TESTING = [int(x[0]) for x in NNET.predict(X_TESTING)]

# Dataset to be sent
df_test['Survived'] = y_pred_TESTING
df_TESTING = df_test[['PassengerId', 'Survived']].astype({'Survived': int})
df_TESTING.to_csv(r'..\4_Output\TITANIC_PRED_4.csv', index=False)

