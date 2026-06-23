"""
report_loop.py — goal loop that drafts a weekly metrics report until it's "done".
We added an iteration cap, a token budget, and error handling per the safety
checklist. Planning to run this unattended every Monday 6am via cron.
"""
import logging
from llm import ask_model, last_call_tokens

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("report_loop")

MAX_ITERS = 25
TOKEN_BUDGET = 200_000


def build_prompt(metrics, draft):
    return f"""You are our analyst. Here are this week's metrics:
{metrics}

Current draft of the report:
{draft if draft else "(none yet)"}

Improve the report. When you are fully satisfied that the report is complete and
publication-ready, reply with the report text followed by the token DONE on its
own line. Otherwise reply with your improved draft.
"""


def generate_report(metrics):
    draft = ""
    tokens_used = 0
    for i in range(MAX_ITERS):
        try:
            out = ask_model(build_prompt(metrics, draft))
        except Exception:
            log.exception("model call failed on iter %s, retrying", i)
            continue
        tokens_used += last_call_tokens()
        if tokens_used > TOKEN_BUDGET:
            log.warning("token budget exceeded, returning current draft")
            return draft
        if out.strip().endswith("DONE"):
            log.info("model reported DONE on iter %s", i)
            return out.rsplit("DONE", 1)[0].strip()
        draft = out
    log.info("hit MAX_ITERS, returning last draft")
    return draft


def main():
    metrics = load_this_weeks_metrics()  # noqa: F821
    report = generate_report(metrics)
    publish_to_confluence(report)  # noqa: F821


if __name__ == "__main__":
    main()
