from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
# 문장 생성
sentences = [
    "Transformer는 Self-Attention을 사용한다.",
    "Attention은 Query, Key, Value를 계산한다.",
    "Attention Score를 계산한다.",
    "Softmax를 적용한다.",
    "BERT는 Encoder만 사용한다.",
    "Masked LM을 사용한다."
]

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# 통과 기준을 정해준다
threads_hold = 0.5

# 담을거
chunks = []

# 
current_chunk = [sentences[0]]

# 임베딩~
embeddings = model.encode(sentences)

# 유사도 계산
for i in range(len(sentences)-1):
    score = cosine_similarity(
        [embeddings[i]],
        [embeddings[i+1]] # 리스트를 하나 더 씌우는 이유는 
    )[0][0]

    # 유사도가 내가 정한 기준보다 높다면
    if score >= threads_hold:
        current_chunk.append(sentences[i+1])

    # 기존에 있던 문장과 비슷하지 않다면 새로운 청크로 생성
    # 그 전에 있던 것들은 비슷하니 하나의 청크로 생성
    else:
        chunks.append(current_chunk)
        current_chunk = [sentences[i+1]]

chunks.append(current_chunk)

# 출력
for i, chunk in enumerate(chunks,1):

    print(f"\nChunk {i}")
    print("-"*30)

    for sentence in chunk:
        print(sentence)


