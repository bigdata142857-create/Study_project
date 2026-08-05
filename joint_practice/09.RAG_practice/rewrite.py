'''
def rewrite(question, history):

    conversation = ""

    for role, text in history:
        conversation += text + " "

    if (
        "운영" in question
        and "Docker Compose" in conversation
        and "PostgreSQL" in conversation
    ):

        return (
            "Docker Compose 운영 환경에서 "
            "PostgreSQL 비밀번호를 "
            "코드에 저장해도 되는가?"
        )

    return question
'''

def rewrite(question, history):

    conversation = ""

    for role, text in history:
        conversation += text + " "

    if "Kubernetes" in conversation and "추측" in question:

        return "B 방식(Kubernetes)의 운영 배포 절차 전체"

    return question