# -*- coding: utf-8 -*-
"""sentiment analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oZbyYL0tmWd6koAA7PUqoT-c7M3KC7jn
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

df.head()

df.info()

df.describe().T

df.nunique()

df.count()

"""cleaning the dataset"""

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

bag=[]
for i in range(0,1000):
  review = re.sub('[^a-zA-Z]',' ',df['Review'][i])
  review = review.lower()
  review = review.split()
  all_stopwords = stopwords.words('english')
  all_stopwords.remove('not')
  ps = PorterStemmer()
  review = [ps.stem(word) for word in review if word not in set(all_stopwords)]
  review = ' '.join(review)
  bag.append(review)

bag

"""creating model for the cleaned dataset
ie; after stemming without altering meaning of the words.
"""

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=1500)
X  = cv.fit_transform(bag).toarray()
y = df.iloc[:,-1].values

print(X)

print(y)

"""splitting dataset into training set and test set"""

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.8,random_state=1)

"""training the Naive Bayes model on the trainging set"""

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train,y_train)

"""predicting the test results"""

y_pred = classifier.predict(X_test)

y_pred

results = np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1)

results

"""making the confusion matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test,y_pred)
print(cm)

ac=accuracy_score(y_test,y_pred)
print(ac)

"""testing with manual interpretation """

new_review = 'I hate this restaurant so much'
# new_review = 'I love this restaurant so much'
new_review = re.sub('[^a-zA-Z]', ' ', new_review)
new_review = new_review.lower()
new_review = new_review.split()
ps = PorterStemmer()
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')
new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
new_review = ' '.join(new_review)
new_corpus = [new_review]
new_X_test = cv.transform(new_corpus).toarray()
new_y_pred = classifier.predict(new_X_test)
print(new_y_pred)



