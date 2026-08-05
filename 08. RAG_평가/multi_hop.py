from retrieval import parent_child_retrieval



def multi_hop_retrieval(
    question,
    model,
    child_embeddings,
    child_chunks,
    parent_chunks,
    top_k=3
):

    """
    Multi-hop Retrieval

    1-hop:
        질문 → 관련 Child 검색

    2-hop:
        검색된 Child 문맥 추가 → 재검색

    """

    # ============================
    # 1-Hop Retrieval
    # ============================

    first_results = parent_child_retrieval(
        question,
        model,
        child_embeddings,
        child_chunks,
        parent_chunks,
        top_k=top_k
    )


    # ============================
    # 2-Hop Query 생성
    # ============================

    second_query = question


    for result in first_results:

        parent = result["parent"]

        second_query += "\n"

        second_query += parent["text"][:500]



    # ============================
    # 2-Hop Retrieval
    # ============================

    second_results = parent_child_retrieval(
        second_query,
        model,
        child_embeddings,
        child_chunks,
        parent_chunks,
        top_k=top_k
    )



    # ============================
    # 결과 병합
    # ============================

    merged = {}



    for result in first_results:

        parent_id = result["parent"]["parent_id"]

        merged[parent_id] = result



    for result in second_results:

        parent_id = result["parent"]["parent_id"]


        if parent_id not in merged:

            merged[parent_id] = result


        else:

            if result["score"] > merged[parent_id]["score"]:

                merged[parent_id] = result



    # ============================
    # 최종 정렬
    # ============================

    final_results = sorted(
        merged.values(),
        key=lambda x: x["score"],
        reverse=True
    )


    return final_results[:top_k]