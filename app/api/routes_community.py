from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.community_engine import (
    compute_sq,
    compute_cq,
    compute_pq,
    compute_eq,
    compute_aoq_community,
    MessageContext,
    ConversationContext,
)

router = APIRouter()


# ----------------------
# Models d'entrée
# ----------------------
class MessageInput(BaseModel):
    text: str
    sender: str


class ConversationInput(BaseModel):
    messages: List[str]
    esg_challenge_participations: int = 0
    contact_priority: float = 0.0


# ----------------------
# Routes
# ----------------------
@router.post("/sq")
def get_sq(payload: ConversationInput):
    ctx = ConversationContext(
        recent_messages=payload.messages,
        esg_challenge_participations=payload.esg_challenge_participations,
        contact_priority=payload.contact_priority,
    )
    return {"SQ": compute_sq(ctx)}


@router.post("/cq")
def get_cq(payload: ConversationInput):
    ctx = ConversationContext(
        recent_messages=payload.messages,
        esg_challenge_participations=payload.esg_challenge_participations,
        contact_priority=payload.contact_priority,
    )
    return {"CQ": compute_cq(ctx)}


@router.post("/pq")
def get_pq(payload: MessageInput):
    msg = MessageContext(payload.text)
    ctx = ConversationContext(recent_messages=[payload.text])
    return {"PQ": compute_pq(msg, ctx)}


@router.post("/aoq")
def get_aoq(payload: ConversationInput):
    ctx = ConversationContext(
        recent_messages=payload.messages,
        esg_challenge_participations=payload.esg_challenge_participations,
        contact_priority=payload.contact_priority,
    )

    last_msg = payload.messages[-1] if payload.messages else ""

    return compute_aoq_community(ctx, last_msg)
