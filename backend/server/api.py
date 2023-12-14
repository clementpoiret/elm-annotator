from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

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
                <img src="/public/404.gif" alt="404" />
            </div>
        </body>
    </html>
        """)
