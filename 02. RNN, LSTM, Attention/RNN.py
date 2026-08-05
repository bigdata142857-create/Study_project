import torch
import torch.nn as nn

# 배치 크기, 문장 길이, 입력차원
x = torch.randn(1,5,10) # randn은 평균 0 표준편차 1인 난수 생성을 의미
#print(x)

rnn = nn.RNN(
    input_size = 10,
    hidden_size = 8,
    batch_first = True
)

output, hidden = rnn(x)
print(output.shape) # (1,5,8)
print(hidden.shape) # (1,1,8)
