# 문장 설정
import numpy as np
source = ['김치','는','맛있어요']
target = ['Kimchi','is','delicious']

# Q, K, V 설정
Q = np.array([
    [1.0, 0.3], # 김치
    [0.2, 1.0], # 는
    [0.4, 0.8]  # 맛있어요
])

K = np.array([
    [1.0, 0.2], # Kimchi
    [0.1, 0.9], # is
    [0.1, 1.0]  # delicious
])

V = np.array([
    [10,1],
    [9,7],
    [7,5]
])
# scores 계산 (Attenion score)
scores = Q @ K.T
#print(scores)

# scaling
d_k = K.shape[1]
scaled_score = scores / np.sqrt(d_k)
#print(scaled_score)

# softmax 함수
def softmax(x):
    exp = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp / np.sum(exp, axis=1, keepdims=True)

# ouput 가중치
weights = softmax(scaled_score)
print(weights)

# 이걸 실제 v 값과 결합
output = weights @ V
print(output)

# 실제 연관 값
print("\n===== Attention =====")

for i, tgt in enumerate(target):
    print(f"\n[{tgt}]")

    for j, src in enumerate(source):
        print(f"{src} : {weights[i,j]:.3f}")