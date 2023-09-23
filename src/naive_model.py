import pandas
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

class NaiveModel:
    df_train: pandas.DataFrame
    df_test: pandas.DataFrame
    
    train_X: pandas.DataFrame
    train_y: pandas.DataFrame
    
    test_X: pandas.DataFrame
    test_y: pandas.DataFrame

    tf_vectorizer: CountVectorizer

    def __init__(self, df_train, df_test) -> None:
        self.df_train = df_train
        self.df_test = df_test

        self.tf_vectorizer = CountVectorizer()

    def prepare_train(self) -> None:
        self.train_X = self.df_train['description']
        self.train_y = self.df_train['category']

    def prepare_test(self) -> None:
        self.test_X = self.df_test['description']
        self.test_y = self.df_test['category']

    def train_model(self, X_train_tf) -> MultinomialNB:
        t = time()

        naive_bayes_classifier = MultinomialNB()
        naive_bayes_classifier.fit(X_train_tf, self.train_y)

        training_time = time() - t
        print("train time: %0.3fs" % training_time)
        return naive_bayes_classifier

    def init_train(self) -> MultinomialNB:
        X_train_tf = self.tf_vectorizer.fit_transform(self.train_X)
        
        return self.train_model(X_train_tf)

    def check_metric(self, model: MultinomialNB) -> None:
        t = time()
        self.prepare_test()
        X_test_tf = self.tf_vectorizer.transform(self.test_X)

        y_pred = model.predict(X_test_tf)

        test_time = time() - t
        print("test time:  %0.3fs" % test_time)

        score1 = metrics.accuracy_score(self.test_y, y_pred)
        print("accuracy:   %0.3f" % score1)

        print(metrics.classification_report(self.test_y, y_pred, target_names=['Positive', 'Negative']))

        print("confusion matrix:")
        print(metrics.confusion_matrix(self.test_y, y_pred))

        print('------------------------------')

    def get_model(self) -> MultinomialNB:
        model = self.init_train()
        self.check_metric(model)
        return model
