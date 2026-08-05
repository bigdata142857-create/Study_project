def need_retrieval(question):

    keywords = [
        "Docker",
        "PostgreSQL",
        "FastAPI",
        "규정",
        "Kubernetes",
        "배포",
        "절차",
        "방식"
    ]

    for keyword in keywords:

        if keyword.lower() in question.lower():

            return True, "운영 배포 절차를 확인하기 위해 외부 문서 검색 수행"

    return False, "대화 이력만으로 답변 가능"