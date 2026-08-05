def add_citation(answer, chunks):
    """
    답변 끝에 출처를 추가하는 함수
    """

    sources = get_sources(chunks)

    answer += "\n\n출처\n"

    for source in sources:
        answer += f"- {source}\n"

    return answer


def get_sources(chunks):
    """
    중복 없이 출처 목록만 추출
    """

    sources = []

    for chunk in chunks:

        if chunk["source"] not in sources:
            sources.append(chunk["source"])

    return sources