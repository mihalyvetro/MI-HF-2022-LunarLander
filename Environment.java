import java.util.Arrays;
import java.util.Random;

import static java.lang.Math.*;

public class Environment {
    int[][] randomVelocityRange;
    static final Vector mapSize = new Vector(300, 200);
    double[] platformHorizontalPosRange = new double[]{Platform.size, mapSize.x - Platform.size};
    Vector landerStartPos = new Vector(mapSize.x / 2, mapSize.y / 10);
    Lander lander = new Lander(landerStartPos, null);
    Platform platform = new Platform(new Vector(mapSize.x / 2, mapSize.y));
    final Vector gravity = new Vector(0, 0.2);
    int stepCounter = 0;
    boolean done = false;
    Result result = null;
    Random rand = new Random();

    // 0: Idle
    // 1: Fire main engine
    // 2: Fire left engine
    // 3: Fire right engine
    final int[] actionSpace = {0, 1, 2, 3};
    final double[][] observationSpace = {
            {-mapSize.x, mapSize.x},             // Horizontal vector to the center of the platform
            {0, mapSize.y},                      // Vertical vector to the center of the platform
            {-Lander.maxSpeed, Lander.maxSpeed}, // Horizontal velocity
            {-Lander.maxSpeed, Lander.maxSpeed}, // Vertical velocity
    };
    final double[] observationSpaceSize = {
            observationSpace[0][1] - observationSpace[0][0],
            observationSpace[1][1] - observationSpace[1][0],
            observationSpace[2][1] - observationSpace[2][0],
            observationSpace[3][1] - observationSpace[3][0],
    };

    double[] state() {
        Vector vectorToPlatform = platform.vectorFromLander(lander);
        return new double[] {vectorToPlatform.x, vectorToPlatform.y,
                                lander.vel.x, lander.vel.y}; 
    }

    EnvStepDTO step(int action) {
        double reward = 0;

        if (!done) {
            Vector force = null;
            switch (action) {
                case 0:
                    force = gravity;
                    break;
                case 1:
                    force = gravity.add(Lander.thrustVectorMainEngine);
                    reward += -0.01;
                    break;
                case 2:
                    force = gravity.add(Lander.thrustVectorLeftEngine);
                    reward += -0.01;
                    break;
                case 3:
                    force = gravity.add(Lander.thrustVectorRightEngine);
                    reward += -0.01;
                    break;
            }

            Vector prevVector = platform.vectorFromLander(lander);
            lander.step(force);
            Vector newVector = platform.vectorFromLander(lander);

            if (lander.checkCollide(this)) {
                if ((newVector.y - lander.size) <= 0 && abs(newVector.x) <= Platform.size) {
                    if (lander.vel.length() <= 2.) {
                        reward += 100.;
                        result = Result.LANDED;
                    } else if (lander.vel.length() <= 4.) {
                        reward += 10. + (40. - (lander.vel.length() * 10));
                        result = Result.LANDING_GEAR_CRASHED;
                    } else {
                        reward += 10.;
                        result = Result.CRASH_LANDING;
                    }
                } else {
                    reward += -100;
                    result = Result.CRASH;
                }
                done = true;
            } else if (abs(newVector.x) < abs(prevVector.x)) {
                reward += 0.1;
            } else {
                reward += -0.1;
            }

            if (stepCounter >= 200) {
                reward += -10.;
                result = Result.OUT_OF_TIME;
                done = true;
            }

            stepCounter += 1;
        }

        return new EnvStepDTO(state(), reward, done);
    }

    public Environment(double platformPos, int[][] randomVelocityRange) {
        this.randomVelocityRange = randomVelocityRange;
        this.reset(platformPos);
    }

    public Environment(int[][] randomVelocityRange) {
        this.randomVelocityRange = randomVelocityRange;
        reset();
    }


    public double[] reset() {
        double platformPos = rand.nextDouble() *
                (platformHorizontalPosRange[1] - platformHorizontalPosRange[0])
                + platformHorizontalPosRange[0];
        return reset(platformPos);
    }
    public double[] reset(double platformPos) {
        Vector landerVelocity;
        if (randomVelocityRange != null) {
            landerVelocity = new Vector(
                    randomVelocityRange[0][0] + rand.nextDouble() *
                            (randomVelocityRange[0][1] - randomVelocityRange[0][0]),
                    randomVelocityRange[1][0] + rand.nextDouble() *
                            (randomVelocityRange[1][1] - randomVelocityRange[1][0]));
        } else {
            landerVelocity = null;
        }
        lander = new Lander(landerStartPos, landerVelocity);

        platform = new Platform(new Vector(platformPos, mapSize.y));
        stepCounter = 0;
        done = false;
        result = null;

        return state();
    }


    class EnvStepDTO {
        double[] state;
        double reward;
        boolean done;

        public EnvStepDTO(double[] state, double reward, boolean done) {
            this.state = state;
            this.reward = reward;
            this.done = done;
        }
    }

    public static void main(String[] args) {
        Environment env = new Environment(null);
        EnvStepDTO res;
        while (!env.done) {
            res = env.step(env.rand.nextInt(env.actionSpace.length));
            System.out.println(
                    "step: " + env.stepCounter +
                    ", state: " + Arrays.toString(res.state) +
                    ", reward:" + res.reward
            );
        }
    }

}

enum Result {
    LANDED,
    LANDING_GEAR_CRASHED,
    CRASH_LANDING,
    CRASH,
    OUT_OF_TIME,
}

class Vector {
    double x;
    double y;

    public Vector(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public Vector subtract(Vector other) {
        return new Vector(this.x - other.x, this.y - other.y);
    }

    public Vector add(Vector other) {
        return new Vector(this.x + other.x, this.y + other.y);
    }

    public Vector prod(Vector other) {
        return new Vector(this.x * other.x, this.y * other.y);
    }

    public Vector prod(double scalar) {
        return new Vector(this.x * scalar, this.y * scalar);
    }

    public double length() {
        return sqrt(pow(x, 2) + pow(y, 2));
    }

    public void normalize() {
        double len = this.length();
        x /= len;
        y /= len;
    }
}

class Lander {
    final double size = 5;
    static final double maxSpeed = 7;
    static final Vector thrustVectorMainEngine = new Vector(0., -0.4);
    static final Vector thrustVectorLeftEngine = new Vector(0.2, 0.);
    static final Vector thrustVectorRightEngine = new Vector(-0.2, 0.);
    Vector pos;
    Vector vel;
    public Lander(Vector pos, Vector vel) {
        this.pos = pos;
        if (vel == null) {
            this.vel = new Vector(0, 0);
        } else {
            this.vel = vel;
        }
    }

    void step(Vector force) {
        vel = vel.add(force);
        if (vel.length() > maxSpeed) {
            vel.normalize();
            vel = vel.prod(maxSpeed);
        }
        pos = pos.add(vel);
    }

    boolean checkCollide(Environment env) {
        if (((pos.x - size) < 0.) || ((pos.y - size) < 0.)) {
            return true;
        }
        if (((pos.x + size) > env.mapSize.x) || ((pos.y + size) > env.mapSize.y)) {
            return true;
        }
        return false;
    }
}

class Platform {
    static final double size = 20;
    Vector pos;

    public Platform(Vector pos) {
        this.pos = pos;
    }

    public Vector vectorFromLander(Lander lander) {
        return pos.subtract(lander.pos);
    }
}
