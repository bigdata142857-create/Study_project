from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity

# Relevance
question = "Transformer는 어떤 구조인가?"

answer1 = """
Transformer는 Self Attention 기반의
Encoder Decoder 구조를 사용하는 모델이다.
"""

answer2 = """
Python은 1991년에 만들어진 프로그래밍 언어이다.
"""


texts = [
    question,
    answer1,
    answer2
]


vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(texts)


score1 = cosine_similarity(
    vectors[0],
    vectors[1]
)

score2 = cosine_similarity(
    vectors[0],
    vectors[2]
)


print(score1, score2)

# Correctness는?
ground_truth = """
이용현은 남성이고 나이는 26살이다.
"""

ai_answer = """
이용현의 나이는 34살이다.
"""

texts = [
    ground_truth,
    ai_answer
]


vectors = vectorizer.fit_transform(texts)


correctness = cosine_similarity(
    vectors[0],
    vectors[1]
)


print(correctness)

