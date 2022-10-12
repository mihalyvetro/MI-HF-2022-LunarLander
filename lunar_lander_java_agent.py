import subprocess

from communication_master import CommunicationMaster

java_path = ''  # TODO

classname = 'StudentCodeBinder'
filename = 'StudentCodeBinder.java'

java_exec_path = f'{java_path}java'
javac_exec_path = f'{java_path}javac'


class LunarLanderJavaAgent:
    def __init__(self, observation_space, action_space, n_iterations):
        # compile student code
        return_code = subprocess.call([javac_exec_path, "-J-Xss64m", "-J-Xmx4g", filename])
        if return_code != 0:
            raise Exception("** Compilation failed. Testing aborted **")

        # create the object performing the communications between the programs
        self.cm = CommunicationMaster()
        
        # exec student code binder
        exec_command = [java_exec_path, "-Xss16m", "-Xmx500m", classname,
                        self.cm.pipe_to_slave_path, self.cm.pipe_from_slave_path]

        # run student code
        student_process = subprocess.Popen(exec_command, stdout=None, stdin=None, stderr=None, text=True)

        # send a message to student code and wait for the answer
        init_msg = 'observation_space\n' + \
                   str(observation_space).replace('],', '\n').replace(']', '').replace('[', '') + \
                   '\naction_space\n'\
                   + str(action_space).replace(']', '').replace('[', '') + \
                   '\nn_iterations\n' + \
                   str(n_iterations)
        lines = self.cm.get_answer(init_msg)

    def step(self, state):
        msg = 'step\n' + str(state).replace('(', '').replace(')', '')
        action_string = self.cm.get_answer(msg)
        action = int(action_string[0])
        return action

    def learn(self, old_state, action, new_state, reward):
        msg = 'learn\n' + \
              str(old_state).replace('(', '').replace(')', '') + '\n' + \
              str(action) + '\n' + \
              str(new_state).replace('(', '').replace(')', '') + '\n' + \
              str(reward)
        ack = self.cm.get_answer(msg)
        return

    def epoch_end(self, epoch_reward_sum):
        msg = 'epoch_end\n' + \
              str(epoch_reward_sum)
        ack = self.cm.get_answer(msg)
        return

    def train_end(self):
        msg = 'train_end'
        ack = self.cm.get_answer(msg)
        return

    def __del__(self):
        self.cm.get_answer("exit")
