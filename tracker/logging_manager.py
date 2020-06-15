import logging
import os
import time
from datetime import datetime

import boto3
from botocore.exceptions import ClientError


def upload_file_s3(file_name, bucket, object_name=None):
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_LOG_KEY']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_LOG_KEY']
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        logging.info('Attempting to Upload to S3')
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


class LoggingManager:
    def __init__(self):
        timestamp = time.time()
        date = datetime.fromtimestamp(timestamp)
        self.filename = "Web_application" + str(date).replace(" ", "_").replace("-", "_").replace(":", "_").replace(".",
                                                                                                                "_")
        logging.basicConfig(
            filename=self.filename,
            filemode='a',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)
        logging.info('Initializing Log File')
        upload_file_s3(self.filename, "webapplogger")