import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# test function
def add(a, b):
    return a + b

async def get_pr_diff(repo: str, pr_number: int, token: str) -> str:
    url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3.diff'
    }
    async with httpx.AsyncClient() as client:
        response = client.get(url, headers=headers)
        return response.text

async def post_pr_comment(repo: str, pr_number: int, comment: str, token: str):
    url = f'https://api.github.com/repos/{repo}/issues/{pr_number}/comments'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={'body': comment}, headers=headers)
        return response.json()
