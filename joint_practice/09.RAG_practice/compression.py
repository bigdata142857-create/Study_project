def compress_context(chunks):

    for chunk in chunks:

        chunk["token_before"] = len(chunk["text"].split())

    return chunks