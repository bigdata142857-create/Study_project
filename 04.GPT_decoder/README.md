# GPT Decoder Block

GPT 계열 모델의 기본 단위인 Decoder Block을 PyTorch 모듈로 구성하며 구조를 학습한 실습입니다.

## 구현 내용

- `nn.MultiheadAttention`을 이용한 Self-Attention
- Residual Connection
- Layer Normalization
- Feed Forward Network(GELU)
- Attention Mask를 전달받는 Decoder forward 흐름

## 파일

- `GPT.py` : Self-Attention → Residual/Norm → FFN → Residual/Norm 순서의 Decoder Block

완성된 GPT 모델을 학습하는 것이 아니라, Decoder 내부에서 입력이 어떤 연산 순서로 전달되는지 이해하는 데 초점을 맞춘 코드입니다.
