def filter_chunks(chunks):

    filtered = []
    removed = []

    threshold = 0.9

    for chunk in chunks:

        if chunk["score"] >= threshold:
            filtered.append(chunk)

        else:
            removed.append({
                "chunk": chunk,
                "reason": "Score Threshold 미만"
            })

    return filtered, removed