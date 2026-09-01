# Statistical NLP - N-gram

통계 기반 NLP의 기본 아이디어를 이해하기 위해 N-gram을 직접 구현한 실습입니다.

## 학습 내용

- 문장을 토큰 단위로 분리
- Trigram(N=3) 생성
- `defaultdict`, `Counter`를 활용한 빈도 저장
- 앞의 두 단어를 기준으로 다음 단어 빈도 계산 및 예측

## 파일

- `ngram.py` : Trigram 생성과 다음 단어 예측 실습
- `통계_NLP_Ngram.ipynb` : 동일 주제의 Notebook 실습

## 실행

```bash
python ngram.py
```

라이브러리 기반 언어 모델을 사용하기 전에, 문맥의 빈도를 이용해 다음 단어를 예측하는 통계적 언어 모델의 원리를 확인하는 데 목적을 두었습니다.
