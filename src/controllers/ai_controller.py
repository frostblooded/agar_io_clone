import pygame
from pygame.math import Vector2
import torch
import torch.optim as optim
import torch.nn.functional as F

from src import constants
from src.blob import Blob
from src.painter import Painter
from src.camera import Camera

import sys

from src.ai import config
from src.ai.strategy import EpsilonGreedyStrategy, ExploitStrategy
from src.ai.agent import Agent
from src.ai.experience import Experience, ReplayMemory, extract_tensors
from src.ai.dqn import DQN
from src.ai.qvalues import QValues
from src.ai.env_manager import EnvManager
from src.ai.config import target_update_period


class AIController:
    def __init__(self, character, app):
        self.app = app
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.character = character
        self.em = EnvManager(self.device)

        if self.app.is_training_mode:
            self.strategy = EpsilonGreedyStrategy(
                config.eps_start, config.eps_end, config.eps_decay)
        else:
            self.strategy = ExploitStrategy()

        self.agent = Agent(self.strategy, config.num_actions, self.device)

        self.policy_net = DQN(
            config.div_rows, config.div_cols).to(self.device)

        self.frame_index = 0

        if self.app.is_training_mode:
            self.memory = ReplayMemory(config.memory_size)
            self.target_net = DQN(
                config.div_rows, config.div_cols).to(self.device)
            self.target_net.load_state_dict(self.policy_net.state_dict())
            self.target_net.eval()
            self.optimizer = optim.Adam(
                params=self.policy_net.parameters(), lr=config.lr)
            self.prev_state = None
            self.prev_action = None
            self.is_first_step = True

    def update(self):
        self.frame_index += 1

        if Camera.followed_character == self.character:
            print("Frame index: {}".format(self.frame_index))

        # start_time = pygame.time.get_ticks()
        current_state = self.em.get_state(self.app, self)
        # print("get_state(...) took {} milliseconds".format(
        # pygame.time.get_ticks() - start_time))

        action = self.agent.select_action(current_state, self.policy_net)
        direction = self.em.get_action_direction(action)
        self.character.position += direction * self.character.get_speed()

        if not self.app.is_training_mode:
            return

        # training
        if not self.is_first_step:
            reward = torch.tensor(
                [self.character.current_reward], device=self.device)
            self.memory.push(Experience(
                self.prev_state, self.prev_action, current_state, reward))

        self.prev_state = current_state
        self.prev_action = action
        self.is_first_step = False

        if self.memory.can_provide_sample(config.batch_size):
            experiences = self.memory.sample(config.batch_size)
            states, actions, rewards, next_states = extract_tensors(
                experiences)

            current_q_values = QValues.get_current(
                self.policy_net, states, actions)
            next_q_values = QValues.get_next(self.target_net, next_states)
            target_q_values = (next_q_values * config.gamma) + rewards

            loss = F.mse_loss(current_q_values, target_q_values.unsqueeze(1))
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        if self.frame_index % target_update_period == 0:
            if Camera.followed_character == self.character:
                print("Update target net")
            self.target_net.load_state_dict(self.policy_net.state_dict())

    def draw(self):
        if self.app.debug_mode:
            if Camera.followed_character == self.character:
                Painter.debug_draw_screen_cells(self.app, self)
