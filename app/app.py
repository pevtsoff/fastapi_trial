from fastapi import FastAPI
from .api import router


app = FastAPI(
    title="FastAPI trial",
    description="My First FASTApi application with Oauth authentication",
    version="1.0.0.",
)
app.include_router(router)
