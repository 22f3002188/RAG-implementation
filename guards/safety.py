def check_minimum_evidence(chunks, min_chunks=2):
    if len(chunks) < min_chunks:
        return False
    return True
