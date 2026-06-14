from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import os
import json
from dotenv import load_dotenv
from app.services.github import get_pr_diff, post_pr_comment
from app.services.claude import review_pr

load_dotenv()

router = APIRouter()

WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

@router.post('/webhook')
async def webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get('X-Hub-Signature-256', '')
    
    expected = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=401, detail='Invalid signature')
    
    data = json.loads(payload)
    event = request.headers.get('X-GitHub-Event', '')
    
    if event == 'pull_request' and data.get('action') == 'opened':
        pr_number = data['pull_request']['number']
        repo = data['repository']['full_name']
        
        print(f'PR #{pr_number} opened on {repo}')
        print('Fetching diff...')
        
        diff = await get_pr_diff(repo, pr_number, GITHUB_TOKEN)
        
        print('Sending to Claude...')
        review = await review_pr(diff)
        
        comment = f'''## PR Roaster Review

**Roast Score: {review['roast_score']}/100**

_{review['summary']}_

### Critical Issues
{chr(10).join(f'- {i}' for i in review['critical'])}

### Warnings
{chr(10).join(f'- {i}' for i in review['warnings'])}

### Suggestions
{chr(10).join(f'- {i}' for i in review['suggestions'])}

---
Powered by PR Roaster'''
        
        await post_pr_comment(repo, pr_number, comment, GITHUB_TOKEN)
        print('Review posted!')
        
        return {'message': 'Review posted successfully'}
    
    return {'message': 'Event ignored'}
