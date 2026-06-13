from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')

def verify_signature(payload: bytes, signature: str) -> bool:
    expected = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@router.post('/webhook')
async def webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get('X-Hub-Signature-256', '')
    if not verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail='Invalid signature')
    data = await request.json()
    event = request.headers.get('X-GitHub-Event', '')
    if event == 'pull_request':
        action = data.get('action')
        pr_number = data['pull_request']['number']
        repo = data['repository']['full_name']
        print(f'PR #{pr_number} {action} on {repo}')
        return {'message': f'PR #{pr_number} {action} received'}
    return {'message': 'Event ignored'}
