# Embedding

텍스트 토큰이 정수 ID를 거쳐 학습 가능한 벡터로 변환되는 과정을 확인한 실습입니다.

## 구현 내용

- 단어 사전을 직접 정의해 Token ID 생성
- Token ID를 Tensor로 변환
- PyTorch `nn.Embedding`을 이용해 저차원 Dense Vector 생성
- 입력 토큰 수와 Embedding Dimension에 따른 출력 shape 확인

## 파일

- `Embedding.py` : Token ID → Tensor → Embedding 변환 실습

Transformer와 문장 임베딩을 학습하기 전에, 모델이 텍스트를 벡터로 처리하는 가장 기본적인 단계를 직접 확인했습니다.
