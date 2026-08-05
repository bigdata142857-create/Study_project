from transformers import BertTokenizer, BertModel
import torch
import torch.nn.functional as F

# 텍스트 문장을 컴퓨터가 알기 쉽게, 바뀐 숫자를 고차원 벡터로 변환
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

sentences = [
    "I love deep learning.",
    "I want my job.",
    "The weather is very bad today."
]

inputs = tokenizer(
    sentences,
    padding=True, # 패딩 하면 안되는 거 아닌 가 하지만
    truncation=True, # 모델이 수용할 수 있는 최대 길이(보통 512단어)를 넘으면 뒷부분을 잘라냄
    return_tensors="pt"
)

#  메모리를 절약하고 속도를 높이기 위해 컴퓨터에게 역전파(기대값 계산을 위한 그라디언트)를 하지 말라고 명령
with torch.no_grad():
    outputs = model(**inputs) # last_hidden_state 정보가 들어가져 있는 상태로 출력

# CLS 토큰만 사용
cls_embeddings = outputs.last_hidden_state[:, 0]
print(cls_embeddings.shape)

scores = F.cosine_similarity(
    cls_embeddings.unsqueeze(1),
    cls_embeddings.unsqueeze(0),
    dim=2
)
print(scores)
