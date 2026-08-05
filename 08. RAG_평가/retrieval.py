from sentence_transformers import util


def parent_child_retrieval(
    question,
    model,
    child_embeddings,
    child_chunks,
    parent_chunks,
    top_k=3
):


    question_embedding = model.encode(
        question,
        convert_to_tensor=True
    )


    scores = util.cos_sim(
        question_embedding,
        child_embeddings
    )[0]


    top_indices = scores.topk(
        k=min(top_k, len(child_chunks))
    ).indices.tolist()



    results = []


    for idx in top_indices:


        child = child_chunks[idx]


        parent_id = child["parent_id"]


        results.append({

            "score":
                round(scores[idx].item(),4),

            "child":
                child,

            "parent":
                parent_chunks[parent_id]

        })


    return results