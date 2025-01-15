"""Upload a frame from the webcam to an AWS S3 bucket."""

import subprocess
from datetime import datetime
from dotenv import load_dotenv

import boto3
from boto3.s3.transfer import S3UploadFailedError
from botocore.exceptions import ClientError

WEBCAM_DEVICE = "/dev/v4l/by-id/usb-046d_C270_HD_WEBCAM_E0A13D10-video-index0"
BUCKET_NAME = "karwoski"

def capture_webcam_image(filename: str) -> None:
    """capture image and save to local file."""
    ffmpeg_command = [
        "ffmpeg",
        "-loglevel", "error", # make logging less verbose
        "-y",  # Overwrite output file if it exists
        "-f", "v4l2",  # Input format
        "-i", WEBCAM_DEVICE,
        "-ss", "2",  # skip 2 secs, webcam takes ~11 frames to warm up
        "-frames:v", "1",  # Capture 1 frame
        filename
    ]
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Image captured successfully to {filename}.")
        return filename
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while capturing the image: {e}")

def upload_webcam_image_to_s3(filename: str) -> None:
  s3_resource = boto3.resource("s3")
  bucket = s3_resource.Bucket(BUCKET_NAME)
  obj = bucket.Object(filename)
  try:
      obj.upload_file(filename)
      print(f"Image uploaded successfully to S3 bucket {BUCKET_NAME}.")
  except S3UploadFailedError as e:
      print(f"Couldn't upload file {filename} to {bucket.name}.")
      print(f"\t{e}")

    

def main():
    # set API keys
    load_dotenv("/home/blake/repo/porch-detect/.env")
    image_filename = f"webcam_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    capture_webcam_image(filename=image_filename)
    upload_webcam_image_to_s3(image_filename)


if __name__ == "__main__":
    main()