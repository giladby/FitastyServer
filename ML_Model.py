import pickle
from Utils import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from Macros import *
from Main import model_mutex, samples_mutex, training_model_mutex


def save_model(model):
    error = False
    try:
        with model_mutex:
            create_path_if_needed(model_file_path)
            with open(model_file_path, 'wb') as file:
                pickle.dump(model, file)
    except:
        error = True
    return error

def try_to_load_model():
    error = False
    model = None
    try:
        with model_mutex:
            with open(model_file_path, 'rb') as file:
                model = pickle.load(file)
    except:
        error = True
    return error, model

def load_model():
    error = False
    model = None
    if is_file_exist(model_file_path):
        error, model = try_to_load_model()
    return error, model

def read_samples_data():
    error = False
    data = None
    try:
        with samples_mutex:
            data = pd.read_csv(samples_file_path)
    except:
        error = True
    return error, data

def create_model():
    return LogisticRegression(max_iter=10000)

def scale_train_and_test(x_train, x_test):
    scaler = MinMaxScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    return x_train_scaled, x_test_scaled

def get_train_and_test():
    error, users_data = read_samples_data()
    x_train, x_test, y_train, y_test = None, None, None, None
    if not error:
        x = users_data.loc[:, users_data.columns != ingredient_label].to_numpy()
        y = users_data[ingredient_label].to_numpy()
        x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                            test_size=0.2,
                                                            random_state=1)
        x_train, x_test = scale_train_and_test(x_train, x_test)
    return error, x_train, x_test, y_train, y_test


def get_accuracy(model, x_test, y_test):
    y_pred = model.predict(x_test)
    return accuracy_score(y_test, y_pred)

def train_model():
    error = False
    if not training_model_mutex.locked():
        with training_model_mutex:
            error, x_train, x_test, y_train, y_test = get_train_and_test()
            if not error:
                model = create_model()
                model.fit(x_train, y_train)
                accuracy = get_accuracy(model, x_test, y_test)
                print(f'accuracy = {accuracy}')
                error = save_model(model)
    return error

def filter_featured_row(featured_row, model):
    elements_to_remove = len(featured_row) - model.n_features_in_
    return featured_row[:-elements_to_remove]

def create_proba_dict(model, featured_row):
    predicted_proba = model.predict_proba([featured_row])[0]
    labels = model.classes_
    return dict(zip(labels, predicted_proba))

def get_probabilities(featured_row):
    proba_dict = {}
    error, model = load_model()
    if not error and model:
        featured_row = filter_featured_row(featured_row, model)
        proba_dict = create_proba_dict(model, featured_row)
    return error, proba_dict

