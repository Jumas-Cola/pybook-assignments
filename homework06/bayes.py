from sklearn.naive_bayes import GaussianNB  # MultinomialNB
import numpy as np


class NaiveBayesClassifier:

    def __init__(self, alpha=None):
        self.model = GaussianNB()  # MultinomialNB()

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        return self.model.fit(X, y)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        return self.model.predict(X)

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        return self.model.score(X_test, y_test)


x = np.array([[-3, 7], [1, 5], [1, 2], [-2, 0], [2, 3], [-4, 0],
              [-1, 1], [1, 1], [-2, 2], [2, 7], [-4, 1], [-2, 7]])
Y = np.array([3, 3, 3, 3, 4, 3, 3, 4, 3, 4, 4, 4])

model = NaiveBayesClassifier()
model.fit(x, Y)

# Predict Output
predicted = model.predict([[1, 2], [3, 4]])
print(predicted)
