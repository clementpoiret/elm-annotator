from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .s3 import S3

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


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


@app.get("/samples", tags=["Data samples"])
async def list_observation_sets(
    path: str = None,
    only_folders: bool = True,
):
    """List all data samples in the bucket or in a specific path"""
    s3 = S3(path=path)
    return {"data": s3.list_files(only_folders=only_folders)}
