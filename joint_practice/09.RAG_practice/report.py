from datetime import datetime


def token_count(chunks):
    return sum(len(chunk["text"].split()) for chunk in chunks)


def save_report(
    question,
    rewrite_query,
    retrieved,
    filtered,
    deduplicated,
    compressed,
    answer,
    sources,
    grounding_result,
    guardrail_result,
    removed_chunks,
    retrieval_reason,
    memory_policy,
    failure_analysis,
):

    with open("report.md", "w", encoding="utf-8") as f:

        f.write("# RAG Pipeline Report\n\n")

        f.write(f"생성 시간 : {datetime.now()}\n\n")

        # -------------------------------------------------
        f.write("## Query Rewrite 결과\n\n")

        f.write("|현재 질문|Rewrite 결과|\n")
        f.write("|---|---|\n")
        f.write(f"|{question}|{rewrite_query}|\n\n")

        # -------------------------------------------------
        f.write("## Post-retrieval 결과표\n\n")

        f.write("|단계|Chunk 개수|Token 수|\n")
        f.write("|---|---:|---:|\n")
        f.write(f"|Retrieval|{len(retrieved)}|{token_count(retrieved)}|\n")
        f.write(f"|Filtering|{len(filtered)}|{token_count(filtered)}|\n")
        f.write(f"|Deduplication|{len(deduplicated)}|{token_count(deduplicated)}|\n")
        f.write(f"|Compression|{len(compressed)}|{token_count(compressed)}|\n\n")

        # -------------------------------------------------
        f.write("## Filtering 결과\n\n")

        if removed_chunks:

            f.write("|제거된 Chunk|제거 이유|\n")
            f.write("|---|---|\n")

            for item in removed_chunks:
                f.write(f"|{item['chunk']['text']}|{item['reason']}|\n")

        else:
            f.write("제거된 Chunk 없음\n")

        f.write("\n")

        # -------------------------------------------------
        f.write("## Context 구성표\n\n")

        for chunk in compressed:
            f.write(f"- {chunk['text']}\n")

        f.write("\n")

        # -------------------------------------------------
        f.write("## Grounding 결과\n\n")

        f.write("|문서|결과|\n")
        f.write("|---|---|\n")

        for source, result in grounding_result:
            f.write(f"|{source}|{result}|\n")

        f.write("\n")

        # -------------------------------------------------
        f.write("## Citation\n\n")

        for source in sources:
            f.write(f"- {source}\n")

        f.write("\n")

        # -------------------------------------------------
        f.write("## Guardrail 결과\n\n")

        if guardrail_result:
            f.write("허용\n\n")
        else:
            f.write("차단\n\n")

        # -------------------------------------------------
        f.write("## Memory 정책\n\n")

        f.write("|항목|내용|\n")
        f.write("|---|---|\n")

        for key, value in memory_policy.items():
            f.write(f"|{key}|{value}|\n")

        f.write("\n")

        # -------------------------------------------------
        f.write("## Adaptive Retrieval 정책\n\n")

        f.write(retrieval_reason + "\n\n")

        # -------------------------------------------------
        f.write("## 실패 분석\n\n")

        if failure_analysis:

            for item in failure_analysis:
                f.write(f"- {item}\n")

        else:
            f.write("실패 없음\n")

        f.write("\n")

        # -------------------------------------------------
        f.write("## 최종 답변\n\n")

        f.write(answer)