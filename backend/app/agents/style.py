import anthropic
from ..config import settings

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are a specialized code quality and style reviewer. Analyze the provided code diff for maintainability and quality issues.

Focus on:
- Overly complex functions (high cyclomatic complexity)
- Code duplication and missed abstraction opportunities
- Poor naming (unclear variables, functions, classes)
- Missing or inadequate documentation for public APIs
- Deeply nested control flow
- Functions doing too many things (single responsibility)
- Dead code or unused variables
- Inconsistent patterns with the surrounding codebase

Respond in this exact format:

## Style Review
**Severity**: [LOW | MEDIUM | HIGH]

### Issues Found
[List each issue with a brief explanation. If none, write "No style issues detected."]

### Recommendations
[Specific, actionable improvements. If none, write "No action required."]"""


async def run_style_agent(diff: str, pr_context: dict) -> tuple[str, str]:
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"PR: {pr_context.get('title', 'N/A')}\nAuthor: {pr_context.get('author', 'N/A')}\n\nDiff:\n```diff\n{diff[:8000]}\n```"
        }]
    )

    content = response.content[0].text
    severity = "low"
    if "**Severity**: HIGH" in content:
        severity = "high"
    elif "**Severity**: MEDIUM" in content:
        severity = "medium"

    return content, severity
