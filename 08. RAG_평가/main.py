from load_document import load_document
from chunking import create_parent_child
from embedding import build_child_embeddings

from retrieval import parent_child_retrieval
from multi_hop import multi_hop_retrieval

from llm import generate_answer



# =====================================================
# Retrieval 선택
# =====================================================

USE_MULTI_HOP = True


retrieval_fn = (
    multi_hop_retrieval
    if USE_MULTI_HOP
    else parent_child_retrieval
)



# =====================================================
# 1. 문서 Load
# =====================================================

document_folder = (
    r"C:\Users\NT551_11TH\Desktop\exem_study\08. RAG_평가\documents"
)


documents = load_document(document_folder)



# =====================================================
# 2. Parent / Child 생성
# =====================================================

parent_chunks, child_chunks = create_parent_child(
    documents
)


print(
    f"Parent : {len(parent_chunks)}"
)

print(
    f"Child : {len(child_chunks)}"
)



# =====================================================
# 3. Embedding 생성
# =====================================================

model, child_embeddings = build_child_embeddings(
    child_chunks
)



# =====================================================
# 4. 질문 입력
# =====================================================

question = input(
    "\n질문을 입력하세요 : "
)



# =====================================================
# 5. Retrieval
# =====================================================

results = retrieval_fn(

    question,

    model,

    child_embeddings,

    child_chunks,

    parent_chunks,

    top_k=3

)



# =====================================================
# 6. LLM 답변 생성
# =====================================================

answer = generate_answer(

    question,

    results

)



# =====================================================
# 7. 결과 출력
# =====================================================

print("\n" + "="*80)

print("질문")

print(question)


print("\n답변")

print(answer)


print("="*80)