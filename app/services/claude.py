import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

async def review_pr(diff: str) -> dict:
    message = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=1000,
        messages=[
            {
                'role': 'user',
                'content': f'''You are a senior engineer doing a code review in a fun roast style.
Review this PR diff and respond ONLY in this exact JSON format:
{{
    "roast_score": <number 0-100, 100 being worst code>,
    "summary": "<one line roast summary>",
    "critical": ["<critical issue 1>", "<critical issue 2>"],
    "warnings": ["<warning 1>", "<warning 2>"],
    "suggestions": ["<suggestion 1>", "<suggestion 2>"]
}}

PR Diff:
{diff}

Respond with JSON only. No extra text.'''
            }
        ]
    )
    
    import json
    response_text = message.content[0].text
    return json.loads(response_text)
