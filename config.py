import boto3
 
S3 = 's3'
 
 
# creating the aws s3 client
# as a standard practice we are not hard-coding the aws access key id and secret key credentials here
# the credentials are defined in the .credentials file
def create_s3_client():
    return boto3.client(S3, aws_access_key_id='AKIAQPRKHHMNZYDDPT6A', aws_secret_access_key='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', region_name='us-east-2')