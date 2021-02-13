import torch
import math
from pygame.math import Vector2
from src.ai.config import num_actions
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FIELD_WIDTH, FIELD_HEIGHT
from src.ai.config import div_rows, div_cols
from src.blob import Blob
from src.character import Character
from src.helpers import Helpers
from src.camera import Camera


class CellFeatures:
    def __init__(self):
        self.blobCount = 0
        self.playerCount = 0
        self.maxCharacterMass = 0
        self.totalCharacterMass = 0

    def __repr__(self):
        return "({a}, {b}, {c}, {d})".format(a=self.blobCount, b=self.playerCount, c=self.maxCharacterMass, d=self.totalCharacterMass)

    def toArray(self):
        return [self.blobCount, self.playerCount, self.maxCharacterMass, self.totalCharacterMass]


class EnvManager():
    def __init__(self, device):
        self.device = device
        # self.env.reset()
        self.current_screen = None
        self.done = False

        self.action_directions = []
        angle_delta = 2*math.pi / num_actions
        for i in range(num_actions):
            angle = i * angle_delta
            x = math.cos(angle)
            y = math.sin(angle)
            self.action_directions.append(Vector2(x, y))

        self.cell_width = SCREEN_WIDTH / div_cols
        self.cell_height = SCREEN_HEIGHT / div_rows

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

    def object_is_in_cell(self, obj, cell_i, cell_j, controller):
        pos = Helpers.world_space_to_screen_space(obj.position)
        radius = obj.size * Camera.zoom
        rect_x = self.cell_width * cell_j
        rect_y = self.cell_height * cell_i
        return Helpers.circle_intersects_rect(pos.x, pos.y,
                                              radius, rect_x, rect_y, self.cell_width, self.cell_height)

    def get_state(self, app, controller):
        state = [[CellFeatures() for j in range(div_cols)]
                 for i in range(div_rows)]

        for obj in app.objects:
            # Don't count the current character
            if controller.character == obj:
                continue

            for i in range(div_rows):
                for j in range(div_cols):
                    if self.object_is_in_cell(obj, i, j, controller):
                        if type(obj) is Blob:
                            state[i][j].blobCount += 1
                        elif type(obj) is Character:
                            state[i][j].playerCount += 1
                            state[i][j].totalCharacterMass += obj.size
                            state[i][j].maxCharacterMass = max(
                                state[i][j].maxCharacterMass, obj.size)

        stateArray = [state[i][j].toArray() for j in range(div_cols)
                      for i in range(div_rows)]
        return torch.tensor([stateArray], device=self.device, dtype=torch.float32)

    def get_action_direction(self, action):
        actionIndex = action.item()
        return self.action_directions[actionIndex]
