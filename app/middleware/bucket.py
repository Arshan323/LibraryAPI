import os
import boto3
from dotenv import load_dotenv
load_dotenv()

liara_endpoint = os.getenv("Liara_endpoint")
liara_secret_key = os.getenv("Liara_secret_key")
liara_access_key = os.getenv("Liara_access_key")
liara_bucket_name = os.getenv("Liara_bucket_name")

s3 = boto3.client(
    "s3",
    endpoint_url=liara_endpoint,
    aws_access_key_id=liara_access_key,
    aws_secret_access_key=liara_secret_key,
)

def upload_file(file, file_name):
    try:
        s3.upload_fileobj(file.file, liara_bucket_name, file_name)
        return f"{liara_endpoint}/{liara_bucket_name}/{file_name}"
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    with open("C:/Users/Arshan/Desktop/practice_fast_api/libraryApi/app/s3bucket.py",'rb') as file:
        upload_file(file=file,file_name="use_cloud")

def delete_file(file_name):
    try:
        s3.delete_object(Bucket=liara_bucket_name, Key=file_name)
        return f"File {file_name} deleted successfully."
    except Exception as e:
        print(f"Error deleting file: {e}")


"""
cmd
cp ..\filename .adressmainfile
"""

