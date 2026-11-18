MODEL_VERSION = "stub-v0"

# Skor = peluang gagal bayar (0 sampai 1)
AUTO_APPROVE_MAX = 0.30   # skor <= ini -> langsung disetujui
AUTO_REJECT_MIN = 0.70    # skor >= ini -> langsung ditolak
                          # di antaranya -> masuk antrean credit analyst

def predict_risk(data: dict) -> float:
    """PENGGANTI SEMENTARA. Ganti isinya dengan model ML asli dari tim."""
    score = 0.2 + data["installment_rate"] / 100 + 0.05 * data["num_existing_credits"]
    return round(min(max(score, 0.0), 1.0), 4)

def decide_status(score: float) -> str:
    if score <= AUTO_APPROVE_MAX:
        return "auto_approved"
    if score >= AUTO_REJECT_MIN:
        return "auto_rejected"
    return "pending_review"