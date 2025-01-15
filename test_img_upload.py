import io
import os
import uuid
import boto3
from boto3.s3.transfer import S3UploadFailedError
from botocore.exceptions import ClientError
import base64
from openai import OpenAI

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def encode_object(obj):
    return base64.b64encode(obj).decode("utf-8")
    
def fetch_obj_from_bucket(s3_client, key, bucket_name="karwoski"):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read()
    except Exception as err:
        print(f"Couldn't get object {key} from bucket {bucket_name}.")
        print(f"\t{err}")
        return

s3_client = boto3.client("s3")
obj = fetch_obj_from_bucket(s3_client, "two_boxes_porch.jpg")
base64_image = encode_object(obj)

# Path to your image
# image_path = "test.jpeg"

# Getting the base64 string
# base64_image = encode_image(image_path)
print("image len:", len(base64_image))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Is there anything on the porch in this image? If so, list the items.",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
)

print(response.choices[0])
