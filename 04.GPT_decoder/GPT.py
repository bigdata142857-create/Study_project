from torch import torch
import torch.nn as nn

# Decoder 블록이라는 새로운 신경망을 만들기 위해 
class Decoder(nn.Module):
    def _init__(self,d_model = 16):
        super._init__() # 처음 만들어질 때 한 번만 실행되는 부분

        # Multi head attetion
        self.attention = nn.MultiheadAttention(
            embed_dim = d_model, # 모델 전체의 차원 크기 입력 출력 텐서의 마지막 차원 크기가 됨
            num_heads = 4, # 어텐션 헤드의 개수
            batch_first = True # 생략
        )

        # 첫 번째 Layer Normalization
        self.norm1 = nn.LayerNorm(d_model)

        # Feed Forward Network
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(), # 복잡하고 꺾인 형태의 어려운 정답 그래프도 모델이 학습할 수 있도록 곡선(유연함)을 더해주는 장치
            nn.Linear(d_model * 4, d_model)
        )

        # 두 번째 Layer Normalization
        self.norm2 = nn.LayerNorm(d_model)

    # 입력이 들어왔을 때 실행되는 함수 Masked_Multihead_Attention
    def forward(self, x, mask):
        attention_output,_ = self.attention(
            x, x, x, # GPT 자체가 자기 자신을 참조하기에 Q, K, V가 아닌 다 x로 해도 괜찮다
            attn_mask = mask
        )

        # 2. Residual Connection
        x = x + attention_output

        # 3. Layer Normalization
        x = self.norm1(x)

        # 4. Feed Forward Network
        ffn_output = self.ffn(x)

        # 5. 다시 Residual Connection
        x = x + ffn_output 

        # 6. 다시 정규화
        x = self.norm2(x)

        return x # <- 이제 이 값이 Decoder2로 들어가게 된다.
