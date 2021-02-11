import torch.nn as nn
import torch.nn.functional as F

# totalCharacterMass, maxCharacterMass, playerCount, blobCount


class DQN(nn.Module):
    def __init__(self, div_rows, div_cols):
        super().__init__()

        self.fc1 = nn.Linear(in_features=div_rows*div_cols*4, out_features=24)
        self.fc2 = nn.Linear(in_features=24, out_features=32)
        self.out = nn.Linear(in_features=32, out_features=8)

    def forward(self, t):
        print(t.shape)
        t = t.flatten(start_dim=1)
        print(t.shape)
        t = F.relu(self.fc1(t))
        t = F.relu(self.fc2(t))
        t = self.out(t)
        return t
