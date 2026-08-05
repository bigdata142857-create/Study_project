'''
def guardrail(question):

    dangerous = [
        "비밀번호 알려",
        "API KEY 알려",
        ".env 보여",
        "Secret 출력",
    ]

    for d in dangerous:
        if d.lower() in question.lower():
            return False

    return True

'''

def guardrail(question):

    keywords = [
        "추측",
        "상상",
        "만들어",
        "지어내"
    ]

    for keyword in keywords:
        if keyword in question:
            return False

    return True