from tkinter import *
from PIL import Image, ImageTk

from lunar_lander_env import Environment
from lunar_lander_agent import LunarLanderAgent
from lunar_lander_java_agent import LunarLanderJavaAgent
from lunar_lander_user_agent import LunarLanderUserAgent


class LunarLanderGUI:
    def __init__(self, agent, n_iterations, env: Environment,
                 env_scaler=4, train_update_interval=50, test_update_interval=200):
        self.env = env
        self.state = self.env.reset()
        self.observation = None

        self.env_scaler = env_scaler
        self.train_update_interval = train_update_interval
        self.test_update_interval = test_update_interval
        self.draw_epoch_interval = 5000
        self.print_epoch_interval = 200

        self.agent = agent

        self.test = False
        self.n_iterations = n_iterations
        self.iteration = 0
        self.epoch = 0
        self.epoch_iteration = 0
        self.epoch_reward_sum = 0
        self.best_epoch_reward_sum = -1000

        self.platform_visual_thickness = 2

        self.window = Tk()
        self.window.resizable(False, False)
        # self.window.wm_attributes("-topmost", 1)
        self.window.title("Lunar Lander v1.0")

        self.canvas = Canvas(self.window,
                             width=self.env.map_size.x * env_scaler,
                             height=self.env.map_size.y * env_scaler,
                             highlightthickness=0, bg="black")
        # self.canvas.pack()
        self.canvas.grid(column=0, row=1, columnspan=40)
        self.lunar_lander_img = None
        self.lunar_lander_draw_id = None
        self.main_exhaust_img = None
        self.main_exhaust_draw_id = None
        self.left_exhaust_img = None
        self.left_exhaust_draw_id = None
        self.right_exhaust_img = None
        self.right_exhaust_draw_id = None
        self.platform_draw_id = None
        # self.canvas.focus_set()
        self.window.after(1000, self.loop())
        self.window.mainloop()

    def draw(self):
        # self.canvas.delete('all')
        info = self.observation[3]
        lander = info['lander']
        lander_x = int(lander['pos'].x * self.env_scaler)
        lander_y = int(lander['pos'].y * self.env_scaler)
        lander_size = int(lander['size'] * self.env_scaler)
        platform = info['platform']
        platform_x = int(platform['pos'].x * self.env_scaler)
        platform_y = int(platform['pos'].y * self.env_scaler)
        platform_size = int(platform['size'] * self.env_scaler)
        platform_thickness = self.platform_visual_thickness * self.env_scaler

        if self.lunar_lander_draw_id is None:
            loaded_image = (Image.open("lander_sprite.png"))
            loaded_image = loaded_image.resize((lander_size * 2, lander_size * 2), Image.ANTIALIAS)
            self.lunar_lander_img = ImageTk.PhotoImage(loaded_image)
            self.lunar_lander_draw_id = self.canvas.create_image(lander_x - lander_size,
                                                                 lander_y - lander_size,
                                                                 anchor=NW,
                                                                 image=self.lunar_lander_img)
            exhaust_image = (Image.open("exhaust_sprite.png"))
            main_exhaust_image = exhaust_image.resize((lander_size // 2, lander_size), Image.ANTIALIAS)
            self.main_exhaust_img = ImageTk.PhotoImage(main_exhaust_image)
            self.main_exhaust_draw_id = self.canvas.create_image(lander_x - (lander_size // 4),
                                                                 lander_y + (lander_size // 2),
                                                                 anchor=NW,
                                                                 image=self.main_exhaust_img)
            left_exhaust_image = exhaust_image.resize((lander_size // 4, lander_size // 2), Image.ANTIALIAS)
            left_exhaust_image = left_exhaust_image.rotate(270, Image.NEAREST, expand=True)
            self.left_exhaust_img = ImageTk.PhotoImage(left_exhaust_image)
            self.left_exhaust_draw_id = self.canvas.create_image(lander_x - lander_size,
                                                                 lander_y,
                                                                 anchor=NW,
                                                                 image=self.left_exhaust_img)
            right_exhaust_image = exhaust_image.resize((lander_size // 4, lander_size // 2), Image.ANTIALIAS)
            right_exhaust_image = right_exhaust_image.rotate(90, Image.NEAREST, expand=True)
            self.right_exhaust_img = ImageTk.PhotoImage(right_exhaust_image)
            self.right_exhaust_draw_id = self.canvas.create_image(lander_x + (lander_size // 2),
                                                                  lander_y,
                                                                  anchor=NW,
                                                                  image=self.right_exhaust_img)
        else:
            self.canvas.moveto(self.lunar_lander_draw_id,
                               lander_x - lander_size, lander_y - lander_size)
            self.canvas.moveto(self.main_exhaust_draw_id,
                               lander_x - (lander_size // 4), lander_y + (lander_size // 2))
            self.canvas.moveto(self.left_exhaust_draw_id,
                               lander_x - lander_size, lander_y)
            self.canvas.moveto(self.right_exhaust_draw_id,
                               lander_x + (lander_size // 2), lander_y)

        self.canvas.itemconfig(self.main_exhaust_draw_id, state='normal' if lander['main_engine'] else 'hidden')
        self.canvas.itemconfig(self.left_exhaust_draw_id, state='normal' if lander['left_engine'] else 'hidden')
        self.canvas.itemconfig(self.right_exhaust_draw_id, state='normal' if lander['right_engine'] else 'hidden')

        if self.platform_draw_id is None:
            self.platform_draw_id = self.canvas.create_rectangle(platform_x - platform_size,
                                                                 platform_y - platform_thickness,
                                                                 platform_x + platform_size,
                                                                 platform_y + platform_thickness,
                                                                 fill="grey")
        else:
            self.canvas.moveto(self.platform_draw_id,
                               platform_x - platform_size, platform_y - platform_thickness)

    def loop(self):
        if not self.test:
            action = self.agent.step(self.state)
            self.observation = self.env.step(action)
            next_state, reward, done, info = self.observation
            self.agent.learn(self.state, action, next_state, reward)

            self.state = next_state

            self.epoch_iteration += 1
            self.epoch_reward_sum += reward
            self.iteration += 1

            if (self.epoch % self.draw_epoch_interval) == 0:
                self.draw()
                call_latency = self.train_update_interval
            elif self.iteration < self.n_iterations:
                call_latency = 0
            else:
                self.test = True
                self.agent.train_end()
                call_latency = self.test_update_interval

            if done or self.iteration >= self.n_iterations:
                if (self.epoch % self.print_epoch_interval) == 0 or self.iteration >= self.n_iterations:
                    print('\nEpoch:', self.epoch)
                    print('Iteration: {} ({:.02f}%)'.format(self.iteration, 100 * self.iteration / self.n_iterations))
                    print('Aggregate reward:', self.epoch_reward_sum)

                self.agent.epoch_end(self.epoch_reward_sum)
                self.state = self.env.reset()
                self.epoch_reward_sum = 0
                self.epoch_iteration = 0
                self.epoch += 1

        else:
            action = self.agent.step(self.state)
            self.observation = self.env.step(action)
            next_state, reward, done, info = self.observation
            self.state = next_state

            self.epoch_iteration += 1
            self.epoch_reward_sum += reward

            if done:
                print('\nAggregate test reward:', self.epoch_reward_sum)
                self.state = self.env.reset()
                self.epoch_reward_sum = 0
                self.epoch_iteration = 0

            self.draw()
            call_latency = self.test_update_interval

        self.window.after(call_latency, self.loop)


if __name__ == "__main__":
    env_scaler = 4

    random_velocity_range = [[-1, 1],
                             [1, 5]]

    env = Environment(random_velocity_range=random_velocity_range)

    n_iterations = int(1e6)

    # python
    # agent = LunarLanderAgent(observation_space=env.observation_space,
    #                          action_space=env.action_space,
    #                          n_iterations=n_iterations)

    # java
    # agent = LunarLanderJavaAgent(observation_space=env.observation_space,
    #                              action_space=env.action_space,
    #                              n_iterations=n_iterations)

    # user
    # agent = LunarLanderUserAgent(observation_space=env.observation_space,
    #                              action_space=env.action_space,
    #                              n_iterations=n_iterations)

    gui = LunarLanderGUI(agent=agent,
                         n_iterations=n_iterations,
                         env=env,
                         env_scaler=env_scaler,
                         train_update_interval=25,
                         test_update_interval=50)
