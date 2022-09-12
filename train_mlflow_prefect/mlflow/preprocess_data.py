import argparse
import os
import pickle

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split


def dump_pickle(obj, filename):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)

def prepare_train_cv_test(filename: str, train_size, validation_size):
    df = read_dataframe(filename)
    test_size=round(1 - train_size - validation_size, 2)
    X_train = df.drop(columns='Rent')
    labels = df['Rent']
    X, X_test, y, y_test = train_test_split(X_train,labels,test_size=round(test_size,2),train_size=round(1-test_size,2))
    X_train, X_cv, y_train, y_cv = train_test_split(X,y,test_size = round(validation_size/(1-test_size),2),train_size=round(train_size/(1-test_size),2))
    X_train_joined = X_train.join(y_train)
    X_cv_joined = X_cv.join(y_cv)
    X_test_joined = X_test.join(y_test)
    return X_train_joined, X_cv_joined, X_test_joined
    


def read_dataframe(filename: str):
    df = pd.read_csv(filename)
    df['Posted On'] =  pd.to_datetime(df['Posted On'])
    df = df[(df.Rent <= 211000)]

    categorical = ['City', 'Area Locality', 'Tenant Preferred']
    df[categorical] = df[categorical].astype(str)

    return df


def preprocess(df: pd.DataFrame, dv: DictVectorizer, fit_dv: bool = False):
    df['City_Area'] = df['City'] + '_' + df['Area Locality']
    categorical = ['City_Area', 'Tenant Preferred']
    numerical = ['BHK', 'Size']
    dicts = df[categorical + numerical].to_dict(orient='records')
    if fit_dv:
        X = dv.fit_transform(dicts)
    else:
        X = dv.transform(dicts)
    return X, dv


def run(raw_data_path: str, dest_path: str, dataset: str = "green"):
       
    src_path = os.path.join(raw_data_path, 'House_Rent_Dataset.csv')
    
    df_train, df_valid, df_test = prepare_train_cv_test(src_path, 0.6, 0.2)

    # extract the target
    target = 'Rent'
    y_train = df_train[target].values
    y_valid = df_valid[target].values
    y_test = df_test[target].values

    # fit the dictvectorizer and preprocess data
    dv = DictVectorizer()
    X_train, dv = preprocess(df_train, dv, fit_dv=True)
    X_valid, _ = preprocess(df_valid, dv, fit_dv=False)
    X_test, _ = preprocess(df_test, dv, fit_dv=False)

    # create dest_path folder unless it already exists
    os.makedirs(dest_path, exist_ok=True)

    # save dictvectorizer and datasets
    dump_pickle(dv, os.path.join(dest_path, "dv.pkl"))
    dump_pickle((X_train, y_train), os.path.join(dest_path, "train.pkl"))
    dump_pickle((X_valid, y_valid), os.path.join(dest_path, "valid.pkl"))
    dump_pickle((X_test, y_test), os.path.join(dest_path, "test.pkl"))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_data_path",
        help="the location where the raw House Rent data was saved"
    )
    parser.add_argument(
        "--dest_path",
        help="the location where the resulting files will be saved."
    )
    args = parser.parse_args()

    run(args.raw_data_path, args.dest_path)
