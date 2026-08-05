# LSTM 코드
import torch
import torch.nn as nn

x = torch.randn(1,5,10)

lstm = nn.LSTM(
    input_size = 10,
    hidden_size = 8,
    batch_first = True
)

output, (hidden, cell) = lstm(x)

print(output.shape) # (1,5,8)
print(hidden.shape) # (1,1,8)
print(cell.shape) # (1,1,8)

# Forget Gate 코드

# 현재 값 입력
x = torch.randn(1,8)

# 이전 hiiden state
h_prev = torch.randn(1,10)

# 이전 cell_state
c_prev = torch.randn(1,8)

# x와 h를 연결
combined = torch.cat((x,h_prev),dim = 1)

# Forget Gate용 가중치
forget_layer = nn.Linear(18,8)

# Forget Gate 계산
f_score = forget_layer(combined) # 출력은 8차원으로 됨
#print(f_score)

# 시그모이드 적용ㅎ서 값 0~1 사이로 변환
forget_gate = torch.sigmoid(f_score)

# 이전 cell_state에 적용
cell = forget_gate * c_prev
print(cell)

# Input Gate 코드

# 현재 값 입력
x = torch.randn(1,8)

# 이전 hiiden state
h_prev = torch.randn(1,10)

# 합쳐
combined = torch.cat((x,h_prev), dim = 1)

# Input Gate용 가중치
input_layer = nn.Linear(18,8)

# Input Gate 계산
input_gate = torch.sigmoid(input_layer(combined))

# 새로운 기억을 만들어
candidate_layer = nn.Linear(18,8)

# 새로운 기억 계산
candidate = torch.tanh(
    candidate_layer(combined)
)

# 완벽한 새로운 기억 생성
new_memory = input_gate * candidate

# 최종
cell = forget_gate * c_prev \
     + input_gate * candidate

print(cell)

# Output Gate

output_layer = nn.Linear(18,8)

output_gate = torch.sigmoid(
    output_layer(combined)
)

# Output Gate 적용
cell_tanh = torch.tanh(cell)

h_new = output_gate * cell_tanh

print(h_new)

