from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import secrets

app = FastAPI()


@app.get("/authorize")
def authorize(client_id: str, redirect_uri: str, response_type: str = "code"):
            
    authorisation_code = secrets.token_urlsafe(16)
    return RedirectResponse(url=f"{redirect_uri}?code={authorisation_code}")


