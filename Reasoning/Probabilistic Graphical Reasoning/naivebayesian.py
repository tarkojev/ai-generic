#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

"""
Naive Bayes Classifier for Cervical and Breast Cancer Datasets
naive Bayes is a probabilistic classifier based on Bayes' theorem, the main difference is that it assumes independence between the features.
Data sets:
- Cervical Cancer Dataset: Contains various features related to cervical cancer diagnosis.
- Breast Cancer Dataset: Contains features related to breast cancer diagnosis.
The code performs the following scenario:
1. Load the datasets.
2. Analyze the datasets by computing prior probabilities and plotting correlation heatmaps.
3. Train a Gaussian Naive Bayes model on the datasets.
4. Evaluate the model using classification reports and confusion matrices.
"""

# Cervical cancer dataset column hardcoding is not needed because it has a header

# Hardcoded column names for the breast cancer dataset
FEATURES = [
    "radius", "texture", "perimeter", "area", "smoothness",
    "compactness", "concavity", "concave points", "symmetry",
    "fractal dimension"
]
# First the 10 'mean' measurements, then 'se', then 'worst'
BREAST_FEATURE_COLS = (
    [f"{feat}_mean" for feat in FEATURES]
  + [f"{feat}_se"   for feat in FEATURES]
  + [f"{feat}_worst" for feat in FEATURES]
)
BREAST_COLS = ["ID", "Class"] + BREAST_FEATURE_COLS


class NaiveBayesClassifier:
    def __init__(self, cervical_path, breast_path):
        self.cervical = pd.read_csv(cervical_path)                       # has header
        self.breast   = pd.read_csv(
            breast_path,
            header=None,
            names=BREAST_COLS
        )

        # Dissplay the first few rows of each dataset
        print("\nCervical Cancer Dataset head:")
        print(self.cervical.head())
        print("\nBreast Cancer Dataset head:")
        print(self.breast.head())

        # Display the shape of each dataset
        self._analyze_dataset(self.cervical, 'ca_cervix', 'Cervical Cancer')
        self._analyze_dataset(self.breast,   'Class',    'Breast Cancer',
                              drop_cols=["ID"])

        # Train and evaluate the model
        self._train_and_evaluate(self.breast,   'Class',    'Breast Cancer')
        self._train_and_evaluate(self.cervical, 'ca_cervix','Cervical Cancer')

    # Analyze the dataset shape and correlation
    def _analyze_dataset(self, df, target_col, title, drop_cols=None):
        df = df.copy()
        if drop_cols:
            df = df.drop(columns=drop_cols)
        
        # Prior probabilities are the relative frequencies of each class
        priors = df[target_col].value_counts(normalize=True)
        print(f"\n{title} priors:\n{priors}\n")

        # Correlation heatmap
        features = df.drop(columns=[target_col])
        corr = features.corr()
        plt.figure(figsize=(8,6))
        sns.heatmap(corr, cmap='coolwarm', square=True)
        plt.title(f"{title} Correlation Heatmap")
        plt.show()

    # Train and evaluate function
    def _train_and_evaluate(self, df, target_col, title):
        data = df.copy()
        # Drop ID if it’s still there
        if "ID" in data.columns:
            data = data.drop(columns=["ID"])

        # Handle missing values by replacing '?' with NaN and dropping rows with NaN
        data.replace('?', np.nan, inplace=True)
        data.dropna(inplace=True)

        X = data.drop(columns=[target_col])
        y = data[target_col]

        # Encode categorical labels if needed
        if y.dtype == 'object':
            y = y.map({v:i for i,v in enumerate(y.unique())})
            print(f"\n{title} encoded labels:\n{y.value_counts()}\n")

        # split, train, predict
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        model = GaussianNB()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Report
        print(f"\n{title} Classification Report:")
        print(classification_report(y_test, y_pred))

        # Confusion matrix display
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(5,4))
        sns.heatmap(
            cm, annot=True, fmt='d', cbar=False,
            xticklabels=np.unique(y), yticklabels=np.unique(y)
        )
        plt.title(f"{title} Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()


if __name__ == '__main__':
    # Setting the base directory and file paths
    base = os.path.dirname(__file__)
    cervical_csv = os.path.join(
        base,
        "data",
        "Cervical Cancer Behavior Risk",
        "sobar-72.csv",
    )
    breast_csv = os.path.join(
        base,
        "data",
        "Breast Cancer Wisconsin Diagnostic",
        "wdbc.data",
    )

    nb = NaiveBayesClassifier(cervical_csv, breast_csv)