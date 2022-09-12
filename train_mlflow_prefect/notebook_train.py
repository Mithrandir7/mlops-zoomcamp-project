#!/usr/bin/env python
# coding: utf-8



# Previously created environment in Anaconda console with conda create -n mlops-zoomcamp-project python=3.8
get_ipython().system('conda activate mlops-zoomcamp-project')



# Sanity check that the environment is active
import os
print (os.environ['CONDA_DEFAULT_ENV'])




get_ipython().system('mlflow --version')


get_ipython().run_line_magic('cd', 'mlflow')



get_ipython().system('dir')



get_ipython().system('python preprocess_data.py --raw_data_path ../data --dest_path ../output')




get_ipython().run_line_magic('cd', '../output')




#Question 2: How many files saved to output folder?

import os
print(len([name for name in os.listdir('.') if os.path.isfile(name)]))


# In[54]:


get_ipython().run_line_magic('cd', '..')


# In[55]:


# Added this in train.py right before rf = RandomForestRegressor(max_depth=10, random_state=0)
#    mlflow.set_tracking_uri("sqlite:///mlflow.db")
#    mlflow.set_experiment("nyc-taxi-experiment")
#    mlflow.sklearn.autolog()
#    with mlflow.start_run():

get_ipython().system('python mlflow/train.py')


# In[56]:


# Question 3: How many parameters are automatically logged by MLflow?

# I executed mlflow ui --backend-store-uri sqlite:///mlflow.db to open mlflow in http://127.0.0.1:5000 and
# checked the parameters of the last run, which were 17


# In[57]:


# Question 4: In addition to backend-store-uri, what else do you need to pass to properly configure the server?

# I run in Anaconda console: mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns


# In[58]:


# I enclosed the RandomForestRegressor with: with mlflow.start_run():
# and logged the parameters as well as the rmse metric at the last line of the block

get_ipython().system('python mlflow/hpo.py')


# In[59]:


# Question 5: What's the best validation RMSE that you got?

# 6.628


# In[60]:


get_ipython().system('python mlflow/register_model.py')


# In[67]:


# Retrieve the run id associated with the registered best model

import mlflow
from mlflow.tracking import MlflowClient
TRACKING_SERVER_HOST = os.getenv('TRACKING_SERVER_HOST', '')
if TRACKING_SERVER_HOST != '':    
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
else:
    mlflow.set_tracking_uri("http://127.0.0.1:5000")

#mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("house-rent-experiment")

client = MlflowClient()
mlflow_model = client.get_latest_versions("house-rent-regressor", stages=["None"])[0]
run_id_best_model = mlflow_model.run_id
print(run_id_best_model)


# In[68]:


# Question 6: What is the test RMSE of the best model?

mlflow.get_run(run_id_best_model).data.metrics['test_rmse']


# In[69]:


model_version = mlflow_model.version
new_stage = "Staging"
client.transition_model_version_stage(
    name="house-rent-regressor",
    version=model_version,
    stage=new_stage,
    archive_existing_versions=False
)

from datetime import datetime

date = datetime.today().date()
client.update_model_version(
    name="house-rent-regressor",
    version=model_version,
    description=f"The model version {model_version} was transitioned to {new_stage} on {date}"
)


# In[ ]:




