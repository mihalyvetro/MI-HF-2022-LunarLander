import numpy as np
from lunar_lander_agent_base import LunarLanderAgentBase


class LunarLanderAgent(LunarLanderAgentBase):
    def __init__(self, observation_space, action_space, n_iterations):
        super(LunarLanderAgent, self).__init__(observation_space, action_space, n_iterations)

    def step(self, state):
        state_quantized = self.quantize_state(self.observation_space, state)
        if not self.test and np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(self.env_action_space)   # Explore action space
        else:
            action = np.argmax(self.q_table[state_quantized])  # Exploit learned values

        self.iteration += 1
        return action
