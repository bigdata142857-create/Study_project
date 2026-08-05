from sentence_transformers import SentenceTransformer


def build_child_embeddings(child_chunks):

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    texts = [chunk["text"] for chunk in child_chunks]

    embeddings = model.encode(
        texts,
        convert_to_tensor=True,
        show_progress_bar=True
    )

    return model, embeddings