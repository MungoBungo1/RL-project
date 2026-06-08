
ACTIONS [
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

        
    def get_state(self):
        pass

    def get_q_values(self):
        pass

    def choose_action(self):
        pass
    
    def get_reward(self):
        pass

    def update_q_table(self):
        pass

    def execture_action(self):
        pass

    def update(self):
        pass

    def save_q_table(self):
        pass

    def load_q_table(self):
        pass