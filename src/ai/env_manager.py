import torch


class EnvManager():
    def __init__(self, device):
        self.device = device
        # self.env.reset()
        self.current_screen = None
        self.done = False

    def reset(self):
        self.env.reset()
        self.current_screen = None

    def close(self):
        self.env.close()

    def render(self, mode='human'):
        return self.env.render(mode)

    def num_actions_available(self):
        return self.env.action_space.n

    def take_action(self, action):
        # _, reward, self.done, _ = self.env.step(action.item())
        return torch.tensor([0], device=self.device)

    def just_starting(self):
        return self.current_screen is None

    def get_state(self):
        return torch.tensor([[[0.0, 0.0, 0.0, 0.0]] * 100], device=self.device)
