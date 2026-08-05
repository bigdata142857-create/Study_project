import torch
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 영어(Source) 문장
src = ["I", "love", "machine", "learning", "."]

# 한국어(Target) 문장
tgt = ["나는", "머신러닝을", "좋아한다", "."]

# 정규화되지 않은 Attention Score
scores = torch.tensor([
    [8.0, 2.0, 0.0, 0.0, 0.0],   # 나는 -> I
    [0.0, 0.0, 5.0, 7.0, 0.0],   # 머신러닝을 -> machine learning
    [2.0, 8.0, 0.0, 0.0, 0.0],   # 좋아한다 -> love
    [0.0, 0.0, 0.0, 0.0, 8.0]    # . -> .
])

# Softmax 적용
attention = torch.softmax(scores, dim=1)

# DataFrame으로 출력
df = pd.DataFrame(
    attention.numpy(),
    index=tgt,
    columns=src
)

print(df)


plt.figure(figsize=(8, 4))

plt.imshow(attention.numpy(), cmap="Blues")

# 축 이름
plt.xticks(range(len(src)), src)
plt.yticks(range(len(tgt)), tgt)

plt.xlabel("English")
plt.ylabel("Korean")
plt.title("Cross Attention")

# 각 칸에 Attention 값 표시
for i in range(attention.shape[0]):
    for j in range(attention.shape[1]):
        plt.text(
            j,
            i,
            f"{attention[i, j]:.2f}",
            ha="center",
            va="center",
            color="black"
        )

plt.colorbar(label="Attention Weight")
plt.tight_layout()
plt.show()