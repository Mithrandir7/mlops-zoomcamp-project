# ML Ops Zoomcamp Project: House Rent Prediction

## Problem Statement

The problem consists in predicting the rent price of houses or apartments in India. The dataset used is from kaggle https://www.kaggle.com/datasets/iamsouravbanerjee/house-rent-prediction-dataset, it contains several features of the houses like the number of bedrooms, hall and kitchen (it comes in a single metric, BHK), the size in square feet, City, City area and type of tenant preferred by the owner or agent.

## Model

The model used is a RandomForestRegressor, whose hyperparameters are optimized.

## Setting up the environment

The project was developed in an Ubuntu VM in VirtualBox, with 8 GB of RAM, for executing the project maybe less are ok I think.

For setting up the environment, first, in the project repository root, create a conda environment with python 3.8, for example

```
conda create --name mlops-zoomcamp-project python=3.8
conda activate mlops-zoomcamp-project
```

Then install the requirements using either of (the last two are freezed requirements, the first will be enough I think)

```
pip install -r requirements.txt
pip install -r requirements_pipfreeze.txt
conda install --yes --file requirements_conda.txt
```





