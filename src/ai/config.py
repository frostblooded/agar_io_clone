import torch

batch_size = 256
gamma = 0.999
eps_start = 1
eps_end = 0.01
eps_decay = 0.001
target_update_period = 60
memory_size = 100000
lr = 0.001
num_episodes = 1000
num_actions = 8
div_rows = 3
div_cols = 3
