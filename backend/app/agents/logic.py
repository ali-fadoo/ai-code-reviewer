import google.generativeai as genai
from ..config import settings

genai.configure(api_key=settings.google_api_key)

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
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )
    prompt = f"PR: {pr_context.get('title', 'N/A')}\nAuthor: {pr_context.get('author', 'N/A')}\n\nDiff:\n```diff\n{diff[:8000]}\n```"
    response = await model.generate_content_async(prompt)

    content = response.text
    severity = "low"
    if "**Severity**: HIGH" in content:
        severity = "high"
    elif "**Severity**: MEDIUM" in content:
        severity = "medium"

    return content, severity
