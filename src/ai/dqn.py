import torch.nn as nn
import torch.nn.functional as F
from src.ai.config import num_actions

# totalCharacterMass, maxCharacterMass, playerCount, blobCount


class DQN(nn.Module):
    def __init__(self, div_rows, div_cols):
        super().__init__()

        self.fc1 = nn.Linear(in_features=div_rows *
                             div_cols*4 + 1, out_features=24)
        self.fc2 = nn.Linear(in_features=24, out_features=32)
        self.out = nn.Linear(in_features=32, out_features=num_actions)

    def forward(self, t):
        t = t.flatten(start_dim=1)
        t = F.relu(self.fc1(t))
        t = F.relu(self.fc2(t))
        t = self.out(t)
        return t
