import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

async def review_pr(diff: str) -> dict:
    prompt = f'''You are a senior engineer doing a code review in a fun roast style.
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

Respond with JSON only. No extra text. No markdown backticks.'''

    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    response_text = response.choices[0].message.content.strip()
    return json.loads(response_text)