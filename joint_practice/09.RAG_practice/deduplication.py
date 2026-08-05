def remove_duplicates(chunks):

    seen = set()

    result = []

    for chunk in chunks:

        if chunk["text"] in seen:
            continue

        seen.add(chunk["text"])

        result.append(chunk)

    return result