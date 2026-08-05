import numpy as np

# Query (한국어)
Q = np.array([
    [1.0, 0.0],   # 나는
    [0.0, 1.0],   # 물을
    [1.0, 1.0]    # 좋아한다
])

# Key (영어)
K = np.array([
    [1.0, 0.2],   # I
    [0.2, 1.0],   # love
    [1.0, 1.0]    # AI
])

V = np.array([
    [10, 1],
    [5, 8],
    [9, 9]
])

# score 계산
scores = Q @ K.T

# Scaling
d_k = K.shape[1]
scaled_score = scores / np.sqrt(d_k)

# Softmax
def softmax(x):
    e = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e / np.sum(e, axis=1, keepdims=True)

weights = softmax(scaled_score)

# output
output = weights @ V

print(f'scores: {scores}')
print(f'Attention_weights: {weights}')
print(f'output: {output}')
