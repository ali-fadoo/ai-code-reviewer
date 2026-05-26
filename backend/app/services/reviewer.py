import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from ..agents.security import run_security_agent
from ..agents.logic import run_logic_agent
from ..agents.style import run_style_agent
from ..agents.synthesizer import run_synthesizer
from ..services.github import get_installation_token, get_pr_diff, post_review_comment
from ..models import Review


async def process_pull_request(payload: dict, db: AsyncSession) -> None:
    pr = payload["pull_request"]
    repo = payload["repository"]["full_name"]
    installation_id = payload["installation"]["id"]

    pr_context = {
        "title": pr["title"],
        "author": pr["user"]["login"],
    }

    token = await get_installation_token(installation_id)
    diff = await get_pr_diff(repo, pr["number"], token)

    security_result, logic_result, style_result = await asyncio.gather(
        run_security_agent(diff, pr_context),
        run_logic_agent(diff, pr_context),
        run_style_agent(diff, pr_context),
    )

    security_review, security_severity = security_result
    logic_review, logic_severity = logic_result
    style_review, style_severity = style_result

    severity_rank = {"low": 0, "medium": 1, "high": 2}
    overall_severity = max(
        [security_severity, logic_severity, style_severity],
        key=lambda s: severity_rank[s],
    )

    final_review = await run_synthesizer(
        security_review, logic_review, style_review, pr_context
    )

    await post_review_comment(repo, pr["number"], final_review, token)

    review = Review(
        pr_number=pr["number"],
        repo_full_name=repo,
        pr_title=pr["title"],
        pr_url=pr["html_url"],
        pr_author=pr["user"]["login"],
        security_review=security_review,
        logic_review=logic_review,
        style_review=style_review,
        final_review=final_review,
        severity=overall_severity,
        status="completed",
    )
    db.add(review)
    await db.commit()
