import pickle
import random

from Utils import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
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
    x_train = scaler.fit_transform(x_train)
    if x_test is not None:
        x_test = scaler.transform(x_test)
    return x_train, x_test

def shuffle_samples(users_data):
    x = users_data.loc[:, users_data.columns != ingredient_label].to_numpy()
    y = users_data[ingredient_label].to_numpy()
    zipped = list(zip(x, y))
    random.shuffle(zipped)
    x_train, y_train = zip(*zipped)
    return np.array(x_train), np.array(y_train)

def get_train_and_test(users_data, to_accuracy):
    x_train, y_train = shuffle_samples(users_data)
    x_test, y_test = None, None
    if to_accuracy:
        x_train, x_test, y_train, y_test = train_test_split(x_train, y_train,
                                                            test_size=0.2,
                                                            random_state=1)
    x_train, x_test = scale_train_and_test(x_train, x_test)
    return x_train, x_test, y_train, y_test

def create_proba_dict(model, featured_row):
    predicted_proba = model.predict_proba([featured_row])[0]
    labels = model.classes_
    return dict(zip(labels, predicted_proba))

def get_accuracy(to_accuracy, accuracy_percent, model, x_test, y_test):
    result = None
    if to_accuracy:
        total_correct = 0
        size = len(x_test)
        percent_amount = round(size * accuracy_percent / 100)
        for x, y in zip(x_test, y_test):
            proba_dict = create_proba_dict(model, x)
            proba_tuple = [(key, proba_dict[key]) for key in proba_dict]
            proba_tuple = sorted(proba_tuple, key=lambda item: item[1], reverse=True)
            proba_filtered_dict = dict(proba_tuple[:percent_amount])
            total_correct += 1 if y in proba_filtered_dict else 0
        result = total_correct / size
    return result

def train_model(accuracy, accuracy_percent):
    error = False
    result = None
    if not training_model_mutex.locked():
        with training_model_mutex:
            error, users_data = read_samples_data()
            error = error or len(users_data) == 0
            if not error:
                x_train, x_test, y_train, y_test = get_train_and_test(users_data, accuracy)
                model = create_model()
                model.fit(x_train, y_train)
                result = get_accuracy(accuracy, accuracy_percent, model, x_test, y_test)
                error = save_model(model)
    return error, result

def filter_featured_row(featured_row, model):
    elements_to_remove = len(featured_row) - model.n_features_in_
    return featured_row[:-elements_to_remove]

def get_probabilities(featured_row):
    proba_dict = {}
    error, model = load_model()
    if not error and model:
        featured_row = filter_featured_row(featured_row, model)
        proba_dict = create_proba_dict(model, featured_row)
    return error, proba_dict

