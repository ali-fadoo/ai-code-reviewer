from groq import AsyncGroq
from ..config import settings

client = AsyncGroq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are a specialized logic and correctness code reviewer. Analyze the provided code diff for bugs and logical issues.

Focus on:
- Logical errors and incorrect assumptions
- Unhandled edge cases (null/undefined, empty collections, boundary values)
- Race conditions and concurrency issues
- Off-by-one errors
- Incorrect algorithm implementations
- Missing or incorrect error handling
- Resource leaks (unclosed files, connections, etc.)
- Incorrect data type usage

Respond in this exact format:

## Logic Review
**Severity**: [LOW | MEDIUM | HIGH]

### Issues Found
[List each issue with a brief explanation. If none, write "No logic issues detected."]

### Recommendations
[Specific, actionable fixes for each issue found. If none, write "No action required."]"""


async def run_logic_agent(diff: str, pr_context: dict) -> tuple[str, str]:
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
