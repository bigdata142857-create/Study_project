import time


def evaluate_retrieval(
    questions,
    retrieval_function,
    model,
    child_embeddings,
    child_chunks,
    parent_chunks,
    top_k=3
):

    hit = 0
    recall = 0
    mrr = 0

    total_time = 0

    for _, row in questions.iterrows():

        question = row["question"]

        # 정답 Section 제목
        answer_title = row["answer_title"]

        start = time.time()

        results = retrieval_function(
            question,
            model,
            child_embeddings,
            child_chunks,
            parent_chunks,
            top_k
        )

        end = time.time()

        total_time += end - start

        # 검색된 Parent 제목들
        retrieved_titles = [
            result["parent"]["title"]
            for result in results
        ]

        # Hit Rate
        if answer_title in retrieved_titles:
            hit += 1

        # Recall@k
        if answer_title in retrieved_titles:
            recall += 1

        # MRR
        if answer_title in retrieved_titles:
            rank = retrieved_titles.index(answer_title) + 1
            mrr += 1 / rank

    total = len(questions)

    return {

        "Hit Rate":
            round(hit / total, 4),

        f"Recall@{top_k}":
            round(recall / total, 4),

        "MRR":
            round(mrr / total, 4),

        "검색 호출 횟수":
            total,

        "평균 검색 시간(초)":
            round(total_time / total, 4)

    }