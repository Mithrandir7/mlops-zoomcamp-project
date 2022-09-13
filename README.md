# ML Ops Zoomcamp Project: House Rent Prediction

## Problem Statement

The problem consists in predicting the rent price of houses or apartments in India. The dataset used is from kaggle https://www.kaggle.com/datasets/iamsouravbanerjee/house-rent-prediction-dataset, it contains several features of the houses like the number of bedrooms, hall and kitchen (it comes in a single metric, BHK), the size in square feet, City, City area and type of tenant preferred by the owner or agent.

## Dataset

I performed Exploratory Data Analysis. The dataset (as with many with prices) is skewed, there are few expensive houses/apartments and many with low prices, which gives a right-skewed distribution. Similar to the course, I plotted the distribution of the prices at 99%, 98% and 95% percentiles, deciding to filter houses/apartments that are expensive that the 98% percentile.

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
Then, in web-service directory execute

```
pip install pipenv
```
And then either one of (the first installs the packages in Pipfile.lock and the second the ones in Pipfile but they are mostly the same)
```
pipenv sync
pipenv install
```

Double check just in case that scikit-learn version is 1.1.2 and that prefect is 2.0b5

## Running the project

To run the project

0. First of all, theres a notebook in notebooks/EDA.ipynb in which I performed Exploratory Data Analysis mentioned previously. You can check to understand the logic of the filtering of the dataset.
1. The first thing is to check init_config.py, there are two variables:
    * **TRACKING_SERVER_HOST** to put the public dns of the EC2 instance for the mlflow tracking and model registry, ie "ec2-34-247-111-41.eu-west-1.compute.amazonaws.com" . Take notice that from time to time that public dns changes from time to time, if the server does not connect, double check in AWS console. If you want to run mlflow local, leave it with ""
    * **AWS_PROFILE** name of thw AWS profile, profiles are a way of authentication, instead of using credentiales explicitly. You can install aws cli to do aws configure ``` pip install aws cli ``` .If you want to run mlflow local, leave it with ""
    
    More info of how to configure a remote tracking server in aws as I did and an aws profile in these links
    
       https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/02-experiment-tracking/mlflow_on_aws.md
       https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html
       https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html#cli-configure-profiles-create
2. Execute the script ``` run_init_config.sh ``` (note that you may have to chmod +x the .sh scripts) to initialize the configuration of these variables
3. Then cd into **train_mlflow_prefect** , and depending of if you run the **experiment tracking and model registry** server local or in the cloud:
    * **Local**: execute ``` run_tracking_server.sh ``` and then in another terminal, execute ``` run_train.sh ```
    * **On AWS (cloud)**: Connect to your EC2 instance, then execute 
    ``` mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://DB_USER:DB_PASSWORD@DB_ENDPOINT:5432/DB_NAME --default-artifact-root s3://S3_BUCKET_NAME ```
    then check the server is up going to ``` http://<EC2_PUBLIC_DNS>:5000 ```
    more on this here: https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/02-experiment-tracking/mlflow_on_aws.md
    Then, execute ``` run_train.sh ```
4. The above step will train the model, with hyperparameter optimization, pick the best model, register it in the model registry, promote it to staging. Also, the model.pkl and config.config file is copied to **web-service** folder for the next steps.
5. For **Workflow orchestration**, you can execute prefect orion start in a terminal and in another terminal, execute ``` run_prefect_deploy.sh ``` , it will make a schedule to train the model every 15th of any month, at 2 am UTC-3.
6. Next, for **Model deployment**, cd into **web-services** . 
    * There, you can execute in a terminal ``` python predict.py ``` and in another one ``` python test.py ``` . predict.py will pull the best model from aws s3 in case the variable **TRACKING_SERVER_HOST** in step 1 is set, or from the local mlrun artifact location otherwise.

    * Also, there is a Dockerfile to containerize and deploy to any cloud where Docker is accepted,       for example AWS. For that, execute in a terminal ``` docker build -t house-rent-prediction-service:v1 . ``` to build the Docker image and then ``` docker run -it --rm -p 9696:9696  house-rent-prediction-service:v1 ``` , and in another terminal execute ``` python test_web_service.py ``` verify that it is working. Note that in this case, the model is loaded from **model.pkl** that was copied in step 3 since from inside the docker image it is difficult and also not suggested to access aws credentials, which are needed to pull the artifacts from S3. This is solved by passing the model binary (which includes the dictionary vectorizer and the model itself).
7. **Last but not least, remember to stop/delete all the resources that you used in AWS in case you run it with the cloud, that is, ec2 instances, rds databases, s3 buckets and maybe another thing which I don't remember. When working with AWS it is useful to check the cost explorer https://us-east-1.console.aws.amazon.com/cost-management/home?region=eu-west-1#/dashboard and set up billing alarms at different levels of billing https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html#turning_on_billing_metrics**
