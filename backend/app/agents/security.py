from groq import AsyncGroq
from ..config import settings

client = AsyncGroq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are a specialized security code reviewer. Analyze the provided code diff for security vulnerabilities.

Focus on:
- Hardcoded secrets, API keys, or passwords
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Insecure authentication or authorization
- Path traversal attacks
- Server-side request forgery (SSRF)
- Sensitive data exposure
- Improper error handling that leaks information
- Insecure direct object references

Respond in this exact format:

## Security Review
**Severity**: [LOW | MEDIUM | HIGH]

### Issues Found
[List each issue with a brief explanation. If none, write "No security issues detected."]

### Recommendations
[Specific, actionable fixes for each issue found. If none, write "No action required."]"""


async def run_security_agent(diff: str, pr_context: dict) -> tuple[str, str]:
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"PR: {pr_context.get('title', 'N/A')}\nAuthor: {pr_context.get('author', 'N/A')}\n\nDiff:\n```diff\n{diff[:8000]}\n```"}
        ],
        max_tokens=1024,
    )

    content = response.choices[0].message.content
    severity = "low"
    if "**Severity**: HIGH" in content:
        severity = "high"
    elif "**Severity**: MEDIUM" in content:
        severity = "medium"

    return content, severity
