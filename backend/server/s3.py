import json
import os
from typing import List

import boto3
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]


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

    def get_file_content(self, fname: str,
                         authorized_extensions: List[str]) -> str:
        """Get the content of a file"""
        file_extension = fname.split(".")[-1].lower()

        if file_extension not in authorized_extensions:
            raise HTTPException(
                status_code=400,
                detail=
                f"File extension not supported: `{file_extension}`. Authorized extensions: {authorized_extensions}",
            )

        try:
            response = self.client.get_object(Bucket=self.bucket_name,
                                              Key=self.path + fname)
        except self.client.exceptions.NoSuchKey:
            raise HTTPException(
                status_code=404,
                detail="File not found",
            )

        if file_extension == "json":
            return json.loads(response["Body"].read().decode("utf-8"))

        if file_extension in IMAGE_EXTENSIONS:
            image_bytes = response["Body"].read()
            media_type = f"image/{file_extension}"

            return image_bytes, media_type

        raise HTTPException(
            status_code=400,
            detail=
            f"File extension not supported: {file_extension}. Authorized extensions: {authorized_extensions}",
        )
