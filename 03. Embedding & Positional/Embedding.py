import torch
import torch.nn as nn

# 단어 사전을 미리 
word_book = {
    '나는':0,
    '밥을':1,
    '먹는다':2
}

# Embedding layer 만들기
embedding = nn.Embedding(
    num_embeddings = len(word_book),
    embedding_dim = 4
)

# 문장
sentence = ['나는','밥을','먹는다']

token_ids = [word_book[word] for word in sentence]

#print(token_ids)

# tensor 변환
x = torch.tensor(token_ids)
#print(x)

# Real embedding
embedded = embedding(x)
print(embedded.shape)
print(embedded)

