import os


#os.environ["TRACKING_SERVER_HOST"] = "ec2-54-154-60-154.eu-west-1.compute.amazonaws.com" # fill in with the public DNS of the EC2 instance

os.environ["AWS_PROFILE"] = "mlops-zoomcamp-project"
print("Environment variables loaded")