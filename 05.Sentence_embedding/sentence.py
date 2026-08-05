from sentence_transformers import SentenceTransformer
from sentence_transformers import util

# 문장 임베딩 모델 로드
model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "I love deep learning.",
    "I wants my job.",
    "The weather is very bad today."
]

# 문장을 벡터로 변환한다
embeddings = model.encode(sentences)
print(embeddings)
print(embeddings.shape)

# 문장을 비교해서 봐보자
scores = util.cos_sim(embeddings, embeddings)
print(scores)

# 출력 결과
'''
[[-0.0654618  -0.12699102  0.06834731 ...  0.1163775  -0.02332213
  -0.0277988 ]
 [-0.05738625  0.02293091 -0.01819707 ...  0.00367104 -0.02191665
  -0.03991161]
 [ 0.02638642  0.10650676  0.15908116 ... -0.01864982 -0.10648838
   0.08511531]]

# 문장 비교 결과
tensor([[ 1.0000,  0.3114, -0.0549],
        [ 0.3114,  1.0000,  0.0303],
        [-0.0549,  0.0303,  1.0000]])
'''

#