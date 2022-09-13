import os
import configparser
import shutil

# If using aws for experiment tracking and model registry fill in with the public DNS of the EC2 instance, else leave it ""
TRACKING_SERVER_HOST = "ec2-34-245-157-41.eu-west-1.compute.amazonaws.com" # fill in with the public DNS of the EC2 instance or leave it ""
TRACKING_SERVER_HOST = ""
# If using aws for experiment tracking and model registry fill with your aws profile, else leave it ""
AWS_PROFILE = "mlops-zoomcamp-project"
AWS_PROFILE = ""

# More info in these links
# https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/02-experiment-tracking/mlflow_on_aws.md
# https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html
# https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html#cli-configure-profiles-create

os.environ["AWS_PROFILE"] = AWS_PROFILE

config = configparser.ConfigParser()
config['DEFAULT'] = {"TRACKING_SERVER_HOST": TRACKING_SERVER_HOST, "AWS_PROFILE": AWS_PROFILE}

with open('./config.config', 'w') as configfile:
    config.write(configfile)

print("Config initialized")