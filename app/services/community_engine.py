import re

SUSPICIOUS_KEYWORDS = [
    "spam", "arnaque", "scam", "fraude", "phishing", "dangereux",
    "suspect", "malveillant", "malware", "virus", "pirate"
]

SUSPICIOUS_PATTERNS = [
    r"http[s]?://[^ ]+",          # liens
    r"\b\d{10,16}\b",             # numéros suspects (cartes, etc.)
    r"(\+?\d{7,15})",             # numéros internationaux
]

def detect_spam_scam_toxicity(messages):
    """
    Retourne un score de risque (0 à 1).
    0 = aucun risque
    1 = risque élevé
    """

    text = " ".join(messages).lower()
    score = 0

    # --- Détection basée sur les mots clés ---
    for word in SUSPICIOUS_KEYWORDS:
        if word in text:
            score += 0.15

    # --- Détection de liens ou patterns suspects ---
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text):
            score += 0.25

    # Clamp final score
    return min(1.0, score)
# =========================================================
# MODELES DE CONTEXTE
# =========================================================

class MessageContext:
    def __init__(self, text: str):
        self.text = text.lower()


class ConversationContext:
    def __init__(self, recent_messages, esg_challenge_participations=0, contact_priority=0.0):
        self.recent_messages = recent_messages
        self.esg_challenge_participations = esg_challenge_participations
        self.contact_priority = contact_priority


# =========================================================
# FONCTIONS AOQ
# =========================================================

def compute_sq(conversation: ConversationContext) -> float:
    """Safety Score : inverse du risque détecté."""
    raw_risk = detect_spam_scam_toxicity(conversation.recent_messages)
    return round(1 - raw_risk, 3)


def compute_cq(conversation: ConversationContext) -> float:
    """Community/ESG Score."""
    text = " ".join(conversation.recent_messages).lower()
    
    esg_signals = ["co2", "esg", "écologie", "ecologie", "environnement", "développement durable"]
    count = sum(1 for w in esg_signals if w in text)

    challenge_score = min(1.0, conversation.esg_challenge_participations / 10)

    final = (0.6 * challenge_score) + (0.4 * min(1.0, count / 5))
    return round(final, 3)


def compute_pq(last_message: MessageContext, context: ConversationContext) -> float:
    """Priority/Urgency Score."""
    urgent_words = ["urgent", "vite", "rapidement", "immédiat", "besoin maintenant"]
    text = last_message.text

    urgency = 1.0 if any(w in text for w in urgent_words) else 0.3
    role_priority = min(1.0, context.contact_priority)

    return round((0.6 * urgency) + (0.4 * role_priority), 3)


def compute_eq(conversation: ConversationContext) -> float:
    """Engagement Quality (simple version)."""
    msg_count = len(conversation.recent_messages)
    engagement = min(1.0, msg_count / 20)
    return round(engagement, 3)


def compute_aoq_community(context: ConversationContext, last_message: str) -> dict:
    """AOQ final : combinaison SQ + CQ + PQ + EQ."""
    msg = MessageContext(last_message)

    sq = compute_sq(context)
    cq = compute_cq(context)
    pq = compute_pq(msg, context)
    eq = compute_eq(context)

    final = round((0.25 * sq) + (0.25 * cq) + (0.25 * pq) + (0.25 * eq), 3)

    return {
        "SQ": sq,
        "CQ": cq,
        "PQ": pq,
        "EQ": eq,
        "AOQ_Community_Score": final
    }
