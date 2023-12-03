from fastapi import FastAPI
from router.router import usuario

app = FastAPI()

# @app.get("/")
# def root():
#     return "Hola soy FastAPI"

app.include_router(usuario)