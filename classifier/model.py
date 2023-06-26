from joblib import load, dump
import pandas as pd

# NLP imports
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

# Classification imports
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier, LogisticRegression


def prediction(job_title):
    with open('readme.txt', 'w') as f:
        f.write('Create a new text file!')

    model = load('classifier/model.joblib')
    pred_industry = model.predict(job_title)
    return pred_industry


def read_data():
    dataframe = pd.read_excel(
        r'/Users/rahul.madan/PycharmProjects/job_title_classification/uploaded_files/training/training_data.xlsx')
    return dataframe


def clean_text(text):
    """
        text: a string
        return: modified clean string
    """
    result = ""
    for token in simple_preprocess(text):
        if token not in STOPWORDS and len(token) >= 2:
            token = token.lower()  # lowercase text
            result += token + " "  # append to result
    return result


def clean_data(dataframe):
    cleanframe = dataframe.drop_duplicates(subset="job title")
    cleanframe['job title'] = cleanframe['job title'].map(clean_text)
    return cleanframe


def naive_bayes(test_split):
    dataframe = read_data()
    cleanframe = clean_data(dataframe)
    X = cleanframe['job title']
    y = cleanframe['industry']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(int(test_split) / 100), random_state=42)
    weights = compute_sample_weight("balanced", y_train)
    nb = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', MultinomialNB()), ])

    nb.fit(X_train, y_train, **{'clf__sample_weight': weights})

    y_pred = nb.predict(X_test)
    accuracy = round(accuracy_score(y_pred, y_test) * 100, 2)
    f1 = round(f1_score(y_pred, y_test, average='weighted') * 100, 2)
    dump(nb, 'model.joblib')
    return accuracy, f1


def linear_svm(test_split):
    dataframe = read_data()
    cleanframe = clean_data(dataframe)
    X = cleanframe['job title']
    y = cleanframe['industry']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(int(test_split) / 100), random_state=42)
    weights = compute_sample_weight("balanced", y_train)
    sgd = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf',
                     SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)), ])

    sgd.fit(X_train, y_train, **{'clf__sample_weight': weights})
    y_pred = sgd.predict(X_test)
    accuracy = round(accuracy_score(y_pred, y_test) * 100, 2)
    f1 = round(f1_score(y_pred, y_test, average='weighted') * 100, 2)
    dump(sgd, 'model.joblib')
    return accuracy, f1


def logistic_regression(test_split):
    dataframe = read_data()
    cleanframe = clean_data(dataframe)
    X = cleanframe['job title']
    y = cleanframe['industry']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(int(test_split) / 100), random_state=42)
    weights = compute_sample_weight("balanced", y_train)
    logreg = Pipeline([('vect', CountVectorizer()),
                       ('tfidf', TfidfTransformer()),
                       ('clf', LogisticRegression(n_jobs=1, C=1e5)),
                       ])
    logreg.fit(X_train, y_train, **{'clf__sample_weight': weights})

    y_pred = logreg.predict(X_test)
    accuracy = round(accuracy_score(y_pred, y_test) * 100, 2)
    f1 = round(f1_score(y_pred, y_test, average='weighted') * 100, 2)
    dump(logreg, 'model.joblib')
    return accuracy, f1
