import os

import boto3
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class S3:
    """Class to handle S3 bucket operations"""

    def __init__(self, path):
        self.bucket_name = os.getenv("AWS_BUCKET_NAME")
        self.path = path

        if path and not path.endswith("/"):
            self.path += "/"

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
        prefix = self.path if self.path else ""

        if only_folders:
            response_iterator = paginator.paginate(Bucket=self.bucket_name,
                                                   Prefix=prefix,
                                                   Delimiter="/")

            if next(iter(response_iterator.search("CommonPrefixes"))) is None:
                raise HTTPException(
                    status_code=404,
                    detail="No folders found",
                )

            return [
                p["Prefix"].replace(prefix, "")
                for p in response_iterator.search("CommonPrefixes")
            ]

        response_iterator = paginator.paginate(Bucket=self.bucket_name,
                                               Prefix=prefix)

        if next(iter(response_iterator.search("Contents"))) is None:
            raise HTTPException(
                status_code=404,
                detail="No files found",
            )

        return [
            content["Key"].replace(prefix, "")
            for content in response_iterator.search("Contents")
        ]
