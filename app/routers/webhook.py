from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import os
import json
from dotenv import load_dotenv
from app.services.github import get_pr_diff, post_pr_comment
from app.services.claude import review_pr
from app.database import SessionLocal, Review

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
        
        print('Sending to AI for review...')
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
        
        # Save to database
        db = SessionLocal()
        db_review = Review(
            repo=repo,
            pr_number=pr_number,
            roast_score=review['roast_score'],
            summary=review['summary'],
            critical=json.dumps(review['critical']),
            warnings=json.dumps(review['warnings']),
            suggestions=json.dumps(review['suggestions'])
        )
        db.add(db_review)
        db.commit()
        db.close()
        print('Review saved to database!')
        
        return {'message': 'Review posted and saved successfully'}
    
    return {'message': 'Event ignored'}

@router.get('/reviews')
def get_reviews():
    db = SessionLocal()
    reviews = db.query(Review).order_by(Review.created_at.desc()).all()
    db.close()
    return [
        {
            'id': r.id,
            'repo': r.repo,
            'pr_number': r.pr_number,
            'roast_score': r.roast_score,
            'summary': r.summary,
            'critical': json.loads(r.critical),
            'warnings': json.loads(r.warnings),
            'suggestions': json.loads(r.suggestions),
            'created_at': r.created_at
        }
        for r in reviews
    ]