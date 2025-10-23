# job_parser.py
# Requires: openai (or use requests to OpenAI API)
# Purpose: create fit_score, missing_skills, summary and outreach suggestions


import os
import json
from typing import Dict
import openai


openai.api_key = os.environ.get('OPENAI_API_KEY')


PROMPT = """
You are an expert career coach. Given a user profile and a job description return a JSON with keys:
- fit_score (0-100)
- reasons (list of short reasons why fit)
- missing_skills (list)
- recommended_cv_changes (bullet points)
- outreach_targets (roles to search: e.g. 'hiring manager', 'team lead', 'recruiter')
Return only JSON.
"""


def analyze_job(profile: Dict, job: Dict) -> Dict:
prompt = PROMPT + "\n
USER PROFILE:\n" + json.dumps(profile) + "\n\nJOB:\n" + json.dumps(job)
resp = openai.ChatCompletion.create(
model='gpt-5-mini',
messages=[{'role':'user','content':prompt}],
max_tokens=600
)
text = resp['choices'][0]['message']['content']
return json.loads(text)


if __name__ == '__main__':
import sys
profile = json.load(open('context.json'))
job = json.loads(sys.stdin.read())
out = analyze_job(profile, job)
print(json.dumps(out, indent=2))