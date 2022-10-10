import numpy as np
# np.random.seed(0)


# The resolution of the observation space
# The four variables of the observation space, from left to right:
#   0: X component of the vector pointing to the middle of the platform from the lander
#   1: Y component of the vector pointing to the middle of the platform from the lander
#   2: X component of the velocity vector of the lander
#   3: Y component of the velocity vector of the lander
OBSERVATION_SPACE_RESOLUTION = [None, None, None, None]  # TODO


class LunarLanderAgentBase:
    def __init__(self, observation_space, action_space, n_iterations):
        self.observation_space = observation_space
        self.q_table = np.zeros([*OBSERVATION_SPACE_RESOLUTION, len(action_space)])
        self.env_action_space = action_space
        self.n_iterations = n_iterations

        self.epsilon = 1.
        self.iteration = 0
        self.test = False

    @staticmethod
    def quantize_state(observation_space, state):
        pass  # TODO

    def epoch_end(self, epoch_reward_sum):
        pass  # TODO

    def learn(self, old_state, action, new_state, reward):
        pass  # TODO

    def train_end(self):
        # ... TODO
        self.q_table = None  # TODO
        self.test = True
