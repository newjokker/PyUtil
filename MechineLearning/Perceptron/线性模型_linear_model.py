# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import Perceptron


iris = load_iris()

X = iris.data[:,(2,3)]  # length width
Y = iris.target.astype(np.int) # iris setosa

per_clf = Perceptron(random_state=42)
per_clf.fit(X, Y)
y_pred = per_clf.predict([[5.1, 2.5]])

print(y_pred)








