import sys
# basic libraries
import pandas as pd
#SQL library
from sqlalchemy import create_engine
# NLP
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
nltk.download(['punkt', 'wordnet'])
# Machine Learning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
# pickle to store model
import pickle


def load_data(database_filepath):
    """
    Load disaster dateset from SQLite & split dataset into messages and categories 
    
    Input: database_filepath: path of SQLite database file of processed dataset
    Return: X: Message part of disaster_message dataframe
        y: category part of disaster_message dataframe
        categories: names of categories, columns of y
    """
    # Load SQLite dataset
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql_table('disaster_messages', engine)

    # split dataset and return message, categories, and column names
    X = df['message']
    y = df.iloc[:, 4:]
    category_names = y.columns.tolist()

    return X, y, category_names


def tokenize(text):
    """
    Clean and tokenize the message
    
    Input: text: the message for tokenization(X from load_data)
    Return: clean_tokens: token list of message
    """
    # remove non-numerical non-character types and tokenize text
    tokens = word_tokenize(re.sub(r"[^a-zA-Z0-9]", " ", text.lower()))

    # Instantiate lemmatizer and stemmer
    wnl = WordNetLemmatizer()
    ps = PorterStemmer()

    # lemmatize tokens of nouns and verbs and stemming
    clean_tokens = []
    for tok in tokens:
        clean_tok = wnl.lemmatize(tok)
        clean_tok = wnl.lemmatize(clean_tok, 'v')
        clean_tok = ps.stem(clean_tok)
        clean_tokens.append(clean_tok.strip())

    return clean_tokens


def build_model():
    """
    Builds the pipeline of NLP + Classification, Tf-Idf as message 
    transformation and AdaBoost+MultiOutputClassifier as 
    classification model, along with GridSearchCV strategy
    
    Return: model: machine learning model described above
    """
    # parameter set for GridSearchCV
    parameters = {
        'tfidf__max_df': (0.9, 1.0),
        'tfidf__ngram_range': ((1, 1), (1, 3))
    }

    # pipeline containing Tf-Idf and AdaBoost
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(tokenizer=tokenize)),
        ('clf', MultiOutputClassifier(AdaBoostClassifier(n_estimators=100, random_state=42)))
    ])

    # Instantiate GridSearchCV
    model = GridSearchCV(pipeline, param_grid=parameters)

    return model


def evaluate_model(model, X_test, Y_test, category_names):
    """
    Evaluate model performance and print metrics of validation
    
    Input:model: classification model from build_model()
        X_test: test set of X(messages)
        Y_test: test set of y(categories)
        category_names: names of message categories(categories column names)
    """
    # print metrics of classification for each column
    Y_pred = pd.DataFrame(model.predict(X_test), columns=category_names)
    print("Classification Accuracy")
    for i in range(36):
        print("Category Name: ",category_names[i])
        print(classification_report(Y_test.iloc[:, i], Y_pred.iloc[:, i]))


def save_model(model, model_filepath):
    """
    Save classification model to pickle file
    
    Input:model: validated classification model
        model_filepath: specified storage path
    """
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database ' \
              'as the first argument and the filepath of the pickle file to ' \
              'save the model to as the second argument. \n\nExample: python ' \
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
