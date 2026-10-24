
from datetime import datetime, timezone
from uuid import uuid4

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    StartSessionContent,
    EndSessionContent,
    chat_protocol_spec,
)


agent = Agent(
    name="proofpath_coordinator",
    seed="proofpath-coordinator-agent-seed-2026",
    port=8000,
    mailbox=True,
)

chat_proto = Protocol(spec=chat_protocol_spec)


def make_reply(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[
            TextContent(type="text", text=text),
            EndSessionContent(type="end-session"),
        ],
    )


def build_response(user_text: str) -> str:
    text = user_text.lower()

    # Damaged delivery case
    if any(word in text for word in [
        "damaged", "broken", "defective", "damaged order"
    ]):
        return (
            "PROOFPATH AI - DAMAGED DELIVERY REVIEW\n\n"
            "Evidence checklist:\n"
            "1. Order invoice or order confirmation\n"
            "2. Photos showing the damage\n"
            "3. Delivery date and order number\n"
            "4. Seller or customer-support messages\n"
            "5. Any refund or replacement policy\n\n"
            "Next steps:\n"
            "- Keep the original packaging if available.\n"
            "- Save photos and seller communications.\n"
            "- Check the seller's actual return/refund policy.\n"
            "- Prepare a clear refund or replacement request.\n\n"
            "To review your case further, tell me:\n"
            "1. When was the order delivered?\n"
            "2. Have you contacted the seller?\n"
            "3. Do you have the refund policy?\n\n"
            "I can suggest next steps, but I cannot guarantee "
            "a refund or confirm eligibility without the relevant terms."
        )

    # Warranty case
    if any(word in text for word in [
        "warranty", "guarantee", "repair claim"
    ]):
        return (
            "PROOFPATH AI - WARRANTY EVIDENCE CHECK\n\n"
            "Useful documents may include:\n"
            "1. Purchase invoice\n"
            "2. Warranty card or warranty terms\n"
            "3. Product serial number or model\n"
            "4. Photos or video showing the fault\n"
            "5. Previous service records or support messages\n\n"
            "Next step: check the warranty period, exclusions, "
            "and claim procedure in the actual warranty terms.\n\n"
            "Tell me the product, purchase date, and problem. "
            "You can also share the relevant warranty wording "
            "for a more specific checklist."
        )

    # Complaint case
    if any(word in text for word in [
        "complaint", "service issue", "service problem"
    ]):
        return (
            "PROOFPATH AI - COMPLAINT REVIEW\n\n"
            "Please gather:\n"
            "1. A short description of the problem\n"
            "2. Date the issue occurred\n"
            "3. Invoice, booking, or reference number\n"
            "4. Previous complaint or ticket number\n"
            "5. Emails, messages, photos, or other evidence\n"
            "6. The outcome you want from the service provider\n\n"
            "Tell me what happened, when you contacted the provider, "
            "and what response you received. I will help identify "
            "missing details and suggest a practical next step."
        )

    # Refund case
    if "refund" in text or "return" in text:
        return (
            "PROOFPATH AI - REFUND REVIEW\n\n"
            "Useful evidence:\n"
            "1. Invoice or order confirmation\n"
            "2. Order and delivery dates\n"
            "3. Reason for requesting a refund\n"
            "4. Relevant photos or screenshots\n"
            "5. Seller's refund/return policy\n"
            "6. Messages exchanged with the seller\n\n"
            "Tell me why you need the refund, when you received "
            "the order, and whether you contacted the seller. "
            "I can help prepare a clear request based on your details."
        )

    # General fallback
    return (
        "Welcome to ProofPath AI!\n\n"
        "I help organize evidence for refunds, warranty claims, "
        "damaged deliveries, and service complaints.\n\n"
        "To get started, tell me:\n"
        "1. What happened?\n"
        "2. When did it happen?\n"
        "3. What evidence or documents do you have?\n"
        "4. What outcome are you seeking?\n\n"
        "I will help identify missing information and suggest "
        "practical next steps."
    )


@chat_proto.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Received chat from {sender}")

    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id,
        ),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            continue

        if isinstance(item, TextContent):
            user_text = item.text.strip()
            ctx.logger.info(f"Processing user request: {user_text}")

            response = build_response(user_text)
            await ctx.send(sender, make_reply(response))


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(
    ctx: Context,
    sender: str,
    msg: ChatAcknowledgement,
):
    ctx.logger.info(f"Chat acknowledgement received from {sender}")


agent.include(chat_proto, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
