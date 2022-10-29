import time

import matplotlib.pyplot as plt

from lunar_lander_env import Environment
from lunar_lander_agent import LunarLanderAgent
from lunar_lander_java_agent import LunarLanderJavaAgent

# For plotting metrics
epoch_iterations_list = []
epoch_rewards_list = []
best_epoch_reward_sum = float('-inf')
best_epoch = 0

n_iterations = int(1e6)
iteration = 0
epoch = 0

print_epoch_interval = 2000

random_velocity_range = [[-1, 1],
                         [1, 5]]

env = Environment(random_velocity_range=random_velocity_range)

# python
agent = LunarLanderAgent(observation_space=env.observation_space,
                         action_space=env.action_space,
                         n_iterations=n_iterations)

# java
# agent = LunarLanderJavaAgent(observation_space=env.observation_space,
#                              action_space=env.action_space,
#                              n_iterations=n_iterations)

start_time = time.time()
while iteration < n_iterations:
    state = env.reset()

    epoch_iteration, epoch_reward_sum = 0, 0
    done = False

    while not done:
        action = agent.step(state)
        next_state, reward, done, info = env.step(action)
        agent.learn(state, action, next_state, reward)

        state = next_state

        epoch_iteration += 1
        epoch_reward_sum += reward

        iteration += 1

    if epoch_reward_sum > best_epoch_reward_sum:
        best_epoch_reward_sum = epoch_reward_sum
        best_epoch = epoch

    agent.epoch_end(epoch_reward_sum)

    if epoch % print_epoch_interval == 0:
        print('\nEpoch:', epoch)
        print('Iteration: {} ({:.02f}%)'.format(iteration, 100 * iteration / n_iterations))
        print(f'Best aggregate reward: {best_epoch_reward_sum:.2f}')

    epoch_iterations_list.append(epoch_iteration)
    epoch_rewards_list.append(epoch_reward_sum)

    epoch += 1

agent.train_end()

print('Training finished.\n')
print('Last 10 iterations:', epoch_iterations_list[-10:])
print('Last 10 aggregate rewards:', epoch_rewards_list[-10:])
print('Best aggregate reward:', best_epoch_reward_sum)
print('Best epoch:', best_epoch)
print('Training Duration: %.2f seconds' % (time.time() - start_time))
fig, ax = plt.subplots(1, 2)
ax[0].scatter(range(len(epoch_iterations_list)), epoch_iterations_list, label='Iterations')
ax[0].legend()
ax[1].scatter(range(len(epoch_rewards_list)), epoch_rewards_list, label='Aggregate rewards')
ax[1].legend()
plt.show()

print('Starting test.')

num_test_iterations = 10
reward_sum = 0

iteration_outcomes = dict()
for i in range(num_test_iterations):
    state = env.reset()
    done = False
    while not done:
        action = agent.step(state)
        state, reward, done, _ = env.step(action)

        reward_sum += reward
    try:
        iteration_outcomes[env.result] += 1
    except KeyError:
        iteration_outcomes[env.result] = 1

print('Iterations:', num_test_iterations)
print('Outcomes:')
print('\t' + '\n\t'.join([f"{key}: {iteration_outcomes[key]}" for key in sorted(iteration_outcomes.keys())]))
print(f'Aggregate test reward: {reward_sum:.2f}')
