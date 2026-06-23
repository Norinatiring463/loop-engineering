"""
support_bot.py — polls our Zendesk queue and auto-drafts replies with an LLM.
Runs as a background worker on the ops box (systemd, restarts on crash).
"""
import time
import zendesk
from llm import ask_model

POLL_SECONDS = 300  # every 5 minutes


def handle_ticket(ticket):
    # Pull the whole ticket thread + all customer history into the prompt.
    history = zendesk.get_full_customer_history(ticket.requester_id)
    thread = zendesk.get_thread(ticket.id)

    prompt = f"""You are our support agent. Here is everything we know about
this customer and the full conversation. Write a reply that resolves their issue.

CUSTOMER HISTORY:
{history}

THREAD:
{thread}
"""
    reply = ask_model(prompt)

    # The model is good, so we just post whatever it writes.
    zendesk.post_reply(ticket.id, reply)
    zendesk.mark_solved(ticket.id)


def main():
    while True:
        new_tickets = zendesk.list_new_tickets()
        for ticket in new_tickets:
            try:
                handle_ticket(ticket)
            except Exception as e:
                # swallow and move on so the worker never dies
                pass
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
