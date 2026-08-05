from openai import OpenAI


client = OpenAI(
    api_key="YOUR_API_KEY"
)


def generate_answer(
    question,
    retrieved_documents
):


    # =================================
    # 1. 검색된 Context 생성
    # =================================

    context = ""


    for doc in retrieved_documents:

        context += (
            doc["parent"]["text"]
            + "\n\n"
        )



    # =================================
    # 2. Prompt 생성
    # =================================

    prompt = f"""

너는 회사 내부 문서를 기반으로 답변하는 AI Assistant이다.

반드시 아래 Context 안의 정보만 사용해서 답변해라.

Context:
{context}


Question:
{question}


Answer:

"""



    # =================================
    # 3. LLM 호출
    # =================================

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role":"system",
                "content":
                "너는 문서 기반 QA 시스템이다."
            },

            {
                "role":"user",
                "content":prompt
            }

        ],

        temperature=0

    )


    answer = response.choices[0].message.content


    return answer