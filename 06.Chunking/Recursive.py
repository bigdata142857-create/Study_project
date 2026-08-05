text = """
Transformer

Transformer는 Self-Attention을 사용한다.
Attention은 Query, Key, Value를 계산한다.

BERT

BERT는 Encoder만 사용한다.
Masked LM을 사용한다.
"""

# 나누는 최대한의 크기를 지정
max_size = 60

# 큰 단위에서 작은 단위로 구분하는 게 필요
separators = [
    "\n\n",   # 문단
    "\n",     # 줄
    " ",      # 단어
    ""        # 글자
]

def recursive_split(text, max_size, separators, level=0):

    # 현재 텍스트가 충분히 작으면 그대로 반환
    if len(text) <= max_size:
        return [text]

    # 더 이상 나눌 기준이 없으면 강제로 자르기
    if level >= len(separators):
        return [text[i:i+max_size] for i in range(0, len(text), max_size)]

    separator = separators[level]

    # 글자 단위
    if separator == "":
        pieces = list(text)
    else:
        pieces = text.split(separator)

    chunks = []

    for piece in pieces:

        piece = piece.strip()

        if not piece:
            continue

        # 너무 크면 한 단계 더 내려감
        if len(piece) > max_size:
            chunks.extend(
                recursive_split(
                    piece,
                    max_size,
                    separators,
                    level + 1
                )
            )

        else:
            chunks.append(piece)

    return chunks

chunks = recursive_split(
    text,
    max_size=60,
    separators=separators
)

for i, chunk in enumerate(chunks,1):
    print(f"\nChunk {i}")
    print("-" * 30)
    print(chunk)