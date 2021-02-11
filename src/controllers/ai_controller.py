import pygame
from pygame.math import Vector2
import torch
import torch.optim as optim
import torch.nn.functional as F

from src import constants
from src.blob import Blob

import sys

from src.ai import config
from src.ai.strategy import EpsilonGreedyStrategy
from src.ai.agent import Agent
from src.ai.experience import Experience, ReplayMemory, extract_tensors
from src.ai.dqn import DQN
from src.ai.qvalues import QValues
from src.ai.env_manager import EnvManager


class AIController:
    def __init__(self, character):
        self.character = character
        self.em = EnvManager(config.device)
        self.strategy = EpsilonGreedyStrategy(
            config.eps_start, config.eps_end, config.eps_decay)
        self.agent = Agent(self.strategy, config.num_actions, config.device)
        self.memory = ReplayMemory(config.memory_size)

        self.policy_net = DQN(
            config.div_rows, config.div_cols).to(config.device)
        self.target_net = DQN(
            config.div_rows, config.div_cols).to(config.device)

        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(
            params=self.policy_net.parameters(), lr=config.lr)

    def find_closest_blob(self, objects):
        closest_blob = None
        closest_dist = sys.float_info.max

        for obj in objects:
            if type(obj) is Blob:
                distance = (obj.position - self.character.position).length()

                if distance < closest_dist:
                    closest_dist = distance
                    closest_blob = obj

        return closest_blob

    def update(self, app):
        state = self.em.get_state()
        action = self.agent.select_action(state, self.policy_net)
        reward = self.em.take_action(action)
        next_state = self.em.get_state()
        self.memory.push(Experience(state, action, next_state, reward))

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

        closest_blob = self.find_closest_blob(app.objects)

        if closest_blob is None:
            return

        movement = (closest_blob.position -
                    self.character.position).normalize()
        self.character.position += movement * self.character.get_speed()
