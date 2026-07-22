from collections import defaultdict, Counter
corpus = [
    "나는 새벽에 잠을 잔다",
    "나는 새벽에 운동을 한다",
    "나는 새벽에 커피를 마신다",
    "나는 아침에 밥을 먹는다"
]

# Trigram에 저장
trigram = defaultdict(list)
#print(trigram)
N = 3

for setence in corpus:
    words = setence.split()

    for wordss in range(len(words) - N +1):
        input_words = tuple(words[wordss:wordss + N-1])
        output_words = words[wordss + N-1]
        trigram[input_words].append(output_words)

# Counter을 활용한 등장 빈도
for key, value in trigram.items():
    count = Counter(value)
    print(f"{key}: {count}")


# 예측을 한다면?
def predict(words):
    words = tuple(words)
    if words in trigram:
        count = Counter(trigram[tuple(words)])
        total = sum(count.values())
        for word, freq in count.items():
            print(f'{word}: {freq/total:.2f}')
        # 이 다음은 확률로 단어를 예측
        real_prediction = count.most_common(1)[0][0]
        return real_prediction

predict(["나는","새벽에"])