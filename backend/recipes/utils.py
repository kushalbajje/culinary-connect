import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from culinary_connect import settings

def upload_to_s3(file, file_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    try:
        
        # Set additional upload parameters, including Content-Disposition and Content-Type
        s3.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_name,
            ExtraArgs={
                'ContentDisposition': 'inline',
            }
        )
        
        # Return the URL of the uploaded file
        return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"
    
    except NoCredentialsError:
        return "Credentials not available. Check your AWS credentials."
    
    except ClientError as e:
        return f"Failed to upload to S3: {e.response['Error']['Message']}"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
