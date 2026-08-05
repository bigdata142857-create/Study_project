def reorder(chunks):

    chunks.sort(
        key=lambda x:x["score"],
        reverse=True
    )

    return chunks