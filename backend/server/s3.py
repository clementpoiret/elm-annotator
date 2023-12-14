import os

import boto3
from dotenv import load_dotenv

load_dotenv()


class S3:
    """Class to handle S3 bucket operations"""

    def __init__(self, path):
        self.bucket_name = os.getenv("AWS_BUCKET_NAME")
        self.path = path

        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION_NAME"),
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
        )

    def list_files(self, only_folders: bool = False) -> list:
        """List all files in the bucket or in a specific path"""
        paginator = self.client.get_paginator("list_objects_v2")

        if only_folders:
            prefix = self.path if self.path else ""
            response_iterator = paginator.paginate(Bucket=self.bucket_name,
                                                   Prefix=prefix,
                                                   Delimiter="/")
            return [
                prefix["Prefix"].replace("/", "")
                for prefix in response_iterator.search("CommonPrefixes")
            ]

        prefix = self.path + "/" if self.path else ""
        response_iterator = paginator.paginate(Bucket=self.bucket_name,
                                               Prefix=prefix)
        return [
            content["Key"] for content in response_iterator.search("Contents")
        ]
