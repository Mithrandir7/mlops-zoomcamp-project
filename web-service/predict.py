import pickle

from flask import Flask, request, jsonify
import configparser
import mlflow




def read_config():
    config = configparser.ConfigParser()
    config.read('./config.config')
    best_run_id = config['DEFAULT']['best_run_id']
    dv_full_path = config['DEFAULT']['dv_full_path']
    artifact_uri = config['DEFAULT']['artifact_uri']
    tracking_server_host = config['DEFAULT']['tracking_server_host']
    return best_run_id, dv_full_path, artifact_uri, tracking_server_host

best_run_id, dv_full_path, artifact_uri, tracking_server_host = read_config()

if tracking_server_host == '':
    logged_model = f'runs:/{best_run_id}/model'
else:
    logged_model = f'{artifact_uri}/model'

model = mlflow.pyfunc.load_model(logged_model)


def prepare_features(house):
    features = {}
    features['City_Area'] = house['City'] + '_' + house['Area Locality']
    features['Tenant Preferred'] = house['Tenant Preferred']
    features['BHK'] = house['BHK']
    features['Size'] = house['Size']
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': best_run_id
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)