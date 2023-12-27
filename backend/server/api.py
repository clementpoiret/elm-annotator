import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response

from .s3 import S3

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/", tags=["Root"])
async def main():
    """Root of the API"""
    return HTMLResponse("""
    <html>
        <head>
            <title>Elm Annotator Backend</title>
        </head>
        <body>
            <div style="text-align: center; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h1 style="font-size: 5rem; font-family: sans-serif;">
                    Hey yo! This is the Elm Annotator Backend.
                </h1>
                <p>There is nothing to show here, this is just the root of the API.</p>
            </div>
        </body>
    </html>
        """)


@app.get("/samples")
async def list_observation_sets(
    path: Optional[str] = None,
    only_folders: Optional[bool] = True,
):
    """List all data samples in the bucket or in a specific path"""
    s3 = S3(path=path)
    return {"data": s3.list_files(only_folders=only_folders)}


@app.get("/file")
async def get_file_content(
    path: Optional[str] = None,
    fname: Optional[str] = None,
):
    """Get the content of a file"""
    s3 = S3(path=path)
    return {
        "data": s3.get_file_content(fname=fname, authorized_extensions=["json"])
    }


@app.get(
    "/image",
    responses={200: {
        "content": {
            "image/png": {}
        }
    }},
    response_class=Response,
)
async def get_image_content(
    path: Optional[str] = None,
    fname: Optional[str] = None,
):
    """Get the content of a file"""
    s3 = S3(path=path)

    image_bytes, media_type = s3.get_file_content(
        fname=fname, authorized_extensions=IMAGE_EXTENSIONS)

    return Response(content=image_bytes, media_type=media_type)
