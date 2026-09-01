# RNN, LSTM, Attention

순차 데이터를 처리하는 RNN과 LSTM의 구조를 확인하고, Attention의 기본 연산을 직접 구현한 실습입니다.

## 학습 내용

- `nn.RNN`의 입력/출력 및 Hidden State shape 확인
- `nn.LSTM`의 Hidden State와 Cell State 확인
- Forget/Input/Output Gate를 선형층과 활성함수로 직접 계산
- Query, Key, Value를 이용한 Attention Score 및 Softmax 가중치 계산

## 파일

- `RNN.py` : RNN 입력과 출력 shape 확인
- `LSTM.py` : LSTM과 Gate 연산 실습
- `Attention.py` : Q·K·V 기반 Attention 연산
- `All.ipynb` : 관련 내용을 Notebook으로 정리한 실습

각 모듈을 바로 사용하는 것과 내부 연산을 나눠 구현하는 방식을 함께 사용해 구조를 이해하는 데 초점을 맞췄습니다.
