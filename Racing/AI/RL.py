import numpy as np
import math
import random

# Discretisation
CARDINAL_DIRS = 8
DISTANCE = 3
SPEED = 3

ACTIONS = [
    "Accelerate",
    "Brake",
    "TurnL",
    "TurnR"
]

# Training constants
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON_START = 1.0
EPSILON_END = 0.05
EPSILON_DECAY = 0.997
TRAINING_EPISODES = 2000

class RL:
    def __init__(self):
        self.q_table = {}
        self.epsilon = EPSILON_START
        self.episode = 0

    def get_state(self, car, checkpoints, current_colour_index, checkpoint_colour):
        # Find the next checkpoint
        current_colour = checkpoint_colour[current_colour_index]
        next_checkpoint = None
        closest_dist = float('inf')
        for cp in checkpoints:
            if cp.colour == current_colour:
                dx = cp.rect.center_x - car.center_x
                dy = cp.rect.center_y - car.center_y
                dist = math.sqrt(dx**2 + dy**2)
                if dist < closest_dist:
                    closest_dist = dist
                    next_checkpoint = cp
            if next_checkpoint is None:
                return (0, 0, 0)

        # Angle to next checkpoint relative to car's heading
        dx = next_checkpoint.rect.center_x - car.center_x
        dy = next_checkpoint.rect.center_y - car.center_y
        angle_to_cp = math.degrees(math.atan2(dy, dx))
        relative_angle = (angle_to_cp - car.angle) % 360
        if relative_angle > 180:
            relative_angle -= 360

        # Distance to next checkpoint
        distance = closest_dist

        # Speed from velocity components
        speed = math.sqrt(car.change_x**2 + car.change_y**2)

        print(f"Distance to next cp: {distance:.0f}")

        # Discretise each value
        angle_bin = int((relative_angle + 180) / 360 * CARDINAL_DIRS) % CARDINAL_DIRS
        distance_bin = min(int(distance / 250), DISTANCE - 1)
        speed_bin = speed_bin = min(int(speed / 5), SPEED - 1)

        return (angle_bin, distance_bin, speed_bin)

    def get_q_values(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(ACTIONS))
        return self.q_table[state]

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, len(ACTIONS) - 1)  # explore
        else:
            return int(np.argmax(self.get_q_values(state)))  # exploit
    
    def get_reward(self):
        pass

    def update_q_table(self, state, action, reward, next_state):
        current_q = self.get_q_values(state)[action]
        max_next_q = np.max(self.get_q_values(next_state))
        new_q = current_q + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def execture_action(self):
        pass

    def update(self):
        pass

    def save_q_table(self):
        pass

    def load_q_table(self):
        pass