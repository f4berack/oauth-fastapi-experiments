from fastapi import FastAPI, Query, Depends
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl, BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select, Column
from typing import Annotated
from enum import Enum
from sqlalchemy import String

import secrets

class TokenEndpointAuthMethod(str, Enum):
    client_secret_basic = "client_secret_basic"
    client_secret_post = "client_secret_post"
    client_secret_jwt = "client_secret_jwt"
    private_key_jwt = "private_key_jwt"

class Client(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    redirect_uris: str = Field(
        default="[]",
        sa_column=Column("redirect_uris", String)
    )
    client_name: str = Field(index=True, unique=True, nullable=False)
    token_endpoint_auth_method: TokenEndpointAuthMethod  = Field(default=TokenEndpointAuthMethod.client_secret_basic)
    logo_uri: HttpUrl = Field(sa_column=Column(String, nullable=True))
    jwks_uri: HttpUrl = Field(sa_column=Column(String, nullable=True))


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register")
def register_client(client: Client, session: SessionDep) -> Client:
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@app.get("/authorize")
def authorize(client_id: str, redirect_uri: HttpUrl, response_type: str = Query("code")):
            
    authorisation_code = secrets.token_urlsafe(32)
    return RedirectResponse(url=f"{redirect_uri}?code={authorisation_code}")


