from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl
from sqlmodel import Field, Session, SQLModel, create_engine, select

import secrets

app = FastAPI()

class Client(SQLModel, table=True):
    client_id: int | None = Field(default=None, primary_key=True)
    client_secret: str = Field(index=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class ClientRegistrationRequest(BaseModel):
    client_name: str
    redirect_uri: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register")
def register_client(data: ClientRegistrationRequest):
            
    authorisation_code = secrets.token_urlsafe(32)
    return RedirectResponse(url=f"{redirect_uri}?code={authorisation_code}")


@app.get("/authorize")
def authorize(client_id: str, redirect_uri: HttpUrl, response_type: str = Query("code")):
            
    authorisation_code = secrets.token_urlsafe(32)
    return RedirectResponse(url=f"{redirect_uri}?code={authorisation_code}")


