MIN_EVIDENCE_SCORE = 0.35

def evidence_score(chunks):
    if not chunks:
        return 0.0
    scores = [c.get("score", 0.0) for c in chunks]
    return sum(scores) / len(scores)

def has_sufficient_evidence(chunks):
    return evidence_score(chunks) >= MIN_EVIDENCE_SCORE
