import random
from math import sqrt


class Vector(object):

    def __init__(self, x, y):
        super(Vector, self).__init__()
        self.x, self.y = x, y

    def __add__(self, vector):
        if isinstance(vector, self.__class__):
            return self.__class__(self.x + vector.x, self.y + vector.y)
        return super(Vector, self).__add__(vector)

    def __sub__(self, vector):
        if isinstance(vector, self.__class__):
            return self.__class__(self.x - vector.x, self.y - vector.y)
        return super(Vector, self).__sub__(vector)

    def __mul__(self, vector):
        if isinstance(vector, self.__class__):
            return self.__class__(self.x * vector.x, self.y * vector.y)
        return self.__class__(self.x * vector, self.y * vector)

    def __repr__(self):
        return "{0}, {1}".format(self.x, self.y)

    @property
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        _length = self.length
        self.x = self.x / _length
        self.y = self.y / _length


class Lander(object):
    size = 5.
    max_speed = 7.
    thrust_vector_main_engine = Vector(0., -0.4)
    thrust_vector_left_engine = Vector(0.2, 0.)
    thrust_vector_right_engine = Vector(-0.2, 0.)

    def __init__(self, pos, vel=None):
        self.pos = pos
        if vel is None:
            self.vel = Vector(0., 0.)
        else:
            self.vel = vel
        super(Lander, self).__init__()

    def step(self, force):
        self.vel = self.vel + force
        if self.vel.length > self.max_speed:
            self.vel.normalize()
            self.vel = self.vel * self.max_speed
        self.pos = self.pos + self.vel

    def check_collide(self, env):
        if (self.pos.x - self.size) < 0. or (self.pos.y - self.size) < 0.:
            return True
        if (self.pos.x + self.size) > env.map_size.x or (self.pos.y + self.size) > env.map_size.y:
            return True
        return False


class Platform(object):
    size = 20.

    def __init__(self, pos):
        self.pos = pos

    def vector_from_lander(self, lander: Lander):
        return self.pos - lander.pos


class Environment(object):
    map_size = Vector(300., 200.)
    platform_horisontal_pos_range = (Platform.size, map_size.x - Platform.size)
    lander_start_pos = Vector(map_size.x / 2., map_size.y / 10.)
    lander = Lander(pos=lander_start_pos)
    platform = Platform(pos=Vector(map_size.x / 2., map_size.y))
    gravity = Vector(0, 0.2)
    step_counter = 0
    done = False
    result = None

    def __init__(self, platform_pos=None, random_velocity_range=None):
        self.random_velocity_range = random_velocity_range
        self.reset(platform_pos=platform_pos)
        super(Environment, self).__init__()

    @property
    def action_space(self):
        # 0: Idle
        # 1: Fire main engine
        # 2: Fire left engine
        # 3: Fire right engine
        return [0, 1, 2, 3]

    @property
    def observation_space(self):
        return [
            [-self.map_size.x, self.map_size.x],        # Horizontal vector to the center of the platform
            [0, self.map_size.y],                       # Vertical vector to the center of the platform
            [-Lander.max_speed, Lander.max_speed],      # Horizontal velocity
            [-Lander.max_speed, Lander.max_speed]       # Vertical velocity
        ]

    @property
    def observation_space_size(self):
        return [s[1] - s[0] for s in self.observation_space]

    @property
    def state(self):
        vector_to_platform = self.platform.vector_from_lander(self.lander)
        return (round(vector_to_platform.x, 2), round(vector_to_platform.y, 2),
                round(self.lander.vel.x, 2), round(self.lander.vel.y, 2))

    def step(self, action):
        assert action in self.action_space

        reward = 0

        if not self.done:
            force = None
            if action == 0:
                force = self.gravity
            elif action == 1:
                force = self.gravity + Lander.thrust_vector_main_engine
                reward += -0.01
            elif action == 2:
                force = self.gravity + Lander.thrust_vector_left_engine
                reward += -0.01
            elif action == 3:
                force = self.gravity + Lander.thrust_vector_right_engine
                reward += -0.01

            prev_vector = self.platform.vector_from_lander(self.lander)
            self.lander.step(force)
            new_vector = self.platform.vector_from_lander(self.lander)

            if self.lander.check_collide(env=self):
                if (new_vector.y - self.lander.size) <= 0 and abs(new_vector.x) <= self.platform.size:
                    if self.lander.vel.length <= 2.:
                        reward += 100.
                        self.result = "landed"
                    elif self.lander.vel.length <= 4.:
                        reward += 10. + (40. - (self.lander.vel.length * 10.))
                        self.result = "landing_gear_crashed"
                    else:
                        reward += 10.
                        self.result = "crash_landing"
                else:
                    reward += -100.
                    self.result = "crash"
                self.done = True
            elif abs(new_vector.x) < abs(prev_vector.x):
                reward += 0.1
            else:
                reward += -0.1

            if self.step_counter >= 200:
                reward += -10.
                self.result = "out_of_time"
                self.done = True

            self.step_counter += 1

        return (self.state, reward, self.done,
                {
                    'lander': {
                        'pos': self.lander.pos,
                        'size': Lander.size,
                        'main_engine': action == 1,
                        'left_engine': action == 2,
                        'right_engine': action == 3
                    },
                    'platform': {
                        'pos': self.platform.pos,
                        'size': self.platform.size
                    }
                })

    def reset(self, platform_pos=None):
        if self.random_velocity_range is not None:
            lander_velocity = Vector(random.uniform(self.random_velocity_range[0][0], self.random_velocity_range[0][1]),
                                     random.uniform(self.random_velocity_range[1][0], self.random_velocity_range[1][1]))
        else:
            lander_velocity = None
        self.lander = Lander(pos=self.lander_start_pos, vel=lander_velocity)
        if platform_pos is None:
            platform_pos = random.randint(*self.platform_horisontal_pos_range)
        self.platform = Platform(pos=Vector(platform_pos, self.map_size.y))
        self.step_counter = 0
        self.done = False
        self.result = None

        return self.state


if __name__ == "__main__":
    # environment = Environment(platform_pos=Environment.map_size.x / 2.)
    environment = Environment()
    while not environment.done:
        state, reward, done, info = environment.step(action=random.choice(environment.action_space))
        print(f"step: {environment.step_counter} state: {state} reward: {reward}")
