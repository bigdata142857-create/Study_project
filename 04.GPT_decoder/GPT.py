import torch.nn as nn


class Decoder(nn.Module):
    """GPT decoder block 구조를 학습하기 위한 간단한 구현."""

    def __init__(self, d_model: int = 16):
        super().__init__()

        self.attention = nn.MultiheadAttention(
            embed_dim=d_model,
            num_heads=4,
            batch_first=True,
        )

        self.norm1 = nn.LayerNorm(d_model)

        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Linear(d_model * 4, d_model),
        )

        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        attention_output, _ = self.attention(
            x,
            x,
            x,
            attn_mask=mask,
        )

        x = self.norm1(x + attention_output)
        ffn_output = self.ffn(x)
        x = self.norm2(x + ffn_output)

        return x
