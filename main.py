from fastapi import FastAPI
import secrets

app = FastAPI()


@app.get("/authorize")
def authorize(client_id: str, redirect_uri: str, response_type: str = "code"):
            
    authorisation_code = secrets.token_urlsafe(16)
    return authorisation_code


