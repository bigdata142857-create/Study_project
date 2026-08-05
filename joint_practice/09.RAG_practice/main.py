from rewrite import rewrite
from Retrieval import retrieve
from filter import filter_chunks
from deduplication import remove_duplicates
from compression import compress_context
from reordering import reorder
from citation import add_citation, get_sources
from grounding import grounding
from guardrail import guardrail
from Adaptive_Retrieval import need_retrieval
from report import save_report

# -------------------------------------------------
# 대화 이력 (실습 시나리오 2)
# -------------------------------------------------
history = [
    ("user", "A 방식과 B 방식의 차이를 알려줘."),
    ("assistant", "A 방식은 Docker Compose를 사용하고, B 방식은 Kubernetes를 사용합니다."),
    ("user", "그러면 두 번째 방식으로 운영 배포하는 절차는?"),
    ("assistant", "검색 결과에서는 일부 절차만 확인되었습니다.")
]

# -------------------------------------------------
# 사용자 질문
# -------------------------------------------------
question = input("질문 : ")

# -------------------------------------------------
# Query Rewrite
# -------------------------------------------------
query = rewrite(question, history)

print("Rewrite Query :", query)

# -------------------------------------------------
# Adaptive Retrieval
# -------------------------------------------------
need, retrieval_reason = need_retrieval(query)

if need:

    # -------------------------------------------------
    # Retrieval
    # -------------------------------------------------
    retrieved_chunks = retrieve(query)

    # -------------------------------------------------
    # Filtering
    # -------------------------------------------------
    filtered_chunks, removed_chunks = filter_chunks(retrieved_chunks)

    # -------------------------------------------------
    # Deduplication
    # -------------------------------------------------
    dedup_chunks = remove_duplicates(filtered_chunks)

    # -------------------------------------------------
    # Compression
    # -------------------------------------------------
    compressed_chunks = compress_context(dedup_chunks)

    # -------------------------------------------------
    # Reordering
    # -------------------------------------------------
    reordered_chunks = reorder(compressed_chunks)

    # -------------------------------------------------
    # Answer 생성
    # -------------------------------------------------
    answer = ""

    for chunk in reordered_chunks:
        answer += chunk["text"] + "\n"

    # -------------------------------------------------
    # Grounding
    # -------------------------------------------------
    ground = grounding(answer, reordered_chunks)

    # -------------------------------------------------
    # Citation
    # -------------------------------------------------
    answer = add_citation(answer, reordered_chunks)

    sources = get_sources(reordered_chunks)

    # -------------------------------------------------
    # Guardrail
    # -------------------------------------------------
    guard = guardrail(question)

    if guard:
        print(answer)
    else:
        print("확인되지 않은 내용을 추측하여 작성할 수 없습니다.")

    # -------------------------------------------------
    # Memory 정책
    # -------------------------------------------------
    memory_policy = {
        "저장된 대화 수": len(history),
        "Rewrite 사용": "O",
        "대화 요약": "X"
    }

    # -------------------------------------------------
    # 실패 분석
    # -------------------------------------------------
    failure_analysis = []

    if len(reordered_chunks) == 1:
        failure_analysis.append("검색 결과가 일부만 존재")

    if not guard:
        failure_analysis.append("추측 요청으로 생성 거부")

    if len(sources) == 0:
        failure_analysis.append("출처 없음")

    # -------------------------------------------------
    # Report 생성
    # -------------------------------------------------
    save_report(
        question=question,
        rewrite_query=query,
        retrieved=retrieved_chunks,
        filtered=filtered_chunks,
        deduplicated=dedup_chunks,
        compressed=compressed_chunks,
        answer=answer,
        sources=sources,
        grounding_result=ground,
        guardrail_result=guard,
        removed_chunks=removed_chunks,
        retrieval_reason=retrieval_reason,
        memory_policy=memory_policy,
        failure_analysis=failure_analysis,
    )

    print("\nreport.md 파일이 생성되었습니다.")

else:
    print("검색이 필요하지 않은 질문입니다.")