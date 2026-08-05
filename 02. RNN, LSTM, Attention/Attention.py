# Attention 코드
import torch

Q = torch.randn(1,4)
K = torch.randn(3,4)
V = torch.randn(3,5)

# 점수를 계산
score = torch.matmul(Q,K.T)

# 가중치 계산
weights = torch.softmax(score, dim = -1)

# 출력
output = torch.matmul(weights,V)

print(output)