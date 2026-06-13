# testing webhook
from fastapi import FastAPI
from app.routers import webhook

app = FastAPI(title='PR Roaster')
app.include_router(webhook.router)

@app.get('/')
def health():
    return {'status': 'PR Roaster is running'}
