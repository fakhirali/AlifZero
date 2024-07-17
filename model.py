import torch
from transformers import BertConfig, BertModel
from torch import nn

configuration = BertConfig(vocab_size=15,
                           hidden_size=64,
                           num_hidden_layers=3,
                           num_attention_heads=2,
                           intermediate_size=64,
                           max_position_embeddings=65
                           )

representation_model = BertModel(configuration)


class ValueModel(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(ValueModel, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, 1)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = self.layer2(x)
        return self.tanh(x)


value_model = ValueModel(64, 64)
