import boto3


s3_client = boto3.client('s3')
avatars = s3_client.Bucket('fs-test')