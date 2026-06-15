from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import webhook
from app.database import create_tables

app = FastAPI(title='PR Roaster')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(webhook.router)

@app.get('/')
def health():
    return {'status': 'PR Roaster is running'}