

# 하나의 문서를 준비해보자
text = """
Transformer는 Self-Attention을 사용한다.
Self-Attention은 Query, Key, Value를 계산한다.
Attention Score를 계산한다.
Softmax를 적용한다.
BERT는 Encoder만 사용한다.
GPT는 Decoder만 사용한다.
"""

# 문장을 리스트로 만들자
sentences = [
    s.strip() # 진짜 또 다른 공백이 있을까봐 strip
    for s in text.strip().split('\n') # \n 없애기 위해서 strip
    if s.strip() # if 문을 굳이 쓰는 이유는 진짜 글이 있는 지 확인하기 위함
]

print(sentences)

chunk_size = 3
overlap = 1

chunks = []

step = chunk_size - overlap

for start in range(0, len(sentences), step):
    chunk = sentences[start:start + chunk_size]

    if chunk:
        chunks.append(chunk)

for i, chunk in enumerate(chunks, 1):
    print(f"\nChunk {i}")
    print("-" * 30)
    print("\n".join(chunk))

