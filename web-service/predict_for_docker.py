import pickle

from flask import Flask, request, jsonify
import configparser
import mlflow
import os

with open('model.pkl', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)


def prepare_features(house):
    features = {}
    features['City_Area'] = house['City'] + '_' + house['Area Locality']
    features['Tenant Preferred'] = house['Tenant Preferred']
    features['BHK'] = house['BHK']
    features['Size'] = house['Size']
    return features


def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return float(preds[0])

app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():      
    house = request.get_json()

    features = prepare_features(house)
    pred = predict(features)

    result = {
        'rent': pred,
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)