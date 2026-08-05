from collections import Counter, defaultdict
import math
documents = [
    "Python은 프로그래밍 언어이다.",
    "Python은 데이터 분석에 많이 사용된다.",
    "머신러닝은 데이터를 이용하여 학습한다.",
    "딥러닝은 인공신경망을 기반으로 한다.",
    "RNN은 순차 데이터를 처리한다.",
    "LSTM은 장기 의존성 문제를 해결한다.",
    "Attention은 중요한 정보에 집중한다.",
    "Transformer는 Attention만으로 구성된다.",
    "BERT는 양방향 Transformer 모델이다.",
    "GPT는 다음 단어를 예측하는 생성형 모델이다.",
    "TF-IDF는 문서 검색에 활용된다.",
    "N-gram은 단어의 연속성을 이용한다.",
    "Word2Vec은 단어를 벡터로 표현한다.",
    "자연어처리는 컴퓨터가 언어를 이해하는 기술이다.",
    "AI는 다양한 산업에서 활용된다."
]

# TF-IDF를 활용한..

# 먼저 토큰화
tokens = [doc.split() for doc in documents]

# 한 문서에 얼마나 많이 있는 지를 세야 하니 (TF)
tf = []
for doc in tokens:
    print(doc)
    count = Counter(doc)
    tf.append(count)
print(tf)

# 단어가 몇개의 문서에 등장하였는가? (DF)

df = defaultdict(int)

for doc in tokens:
    for word in set(doc): 
        df[word] += 1

# IDF 계산
N = len(documents)

idf = {}

for word, freq in df.items():
    idf[word] = math.log(N / freq)

