import keyboard


class LunarLanderUserAgent:
    def __init__(self, observation_space, action_space, n_iterations):
        pass

    def step(self, state):
        if keyboard.is_pressed('s'):
            return 1
        elif keyboard.is_pressed('d'):
            return 2
        elif keyboard.is_pressed('a'):
            return 3
        else:
            return 0

    def epoch_end(self, epoch_reward_sum):
        pass

    def learn(self, old_state, action, new_state, reward):
        pass

    def train_end(self):
        pass
