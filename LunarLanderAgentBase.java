import java.util.Arrays;

public class LunarLanderAgentBase {
    // The resolution of the observation space
    // The four variables of the observation space, from left to right:
    //   0: X component of the vector pointing to the middle of the platform from the lander
    //   1: Y component of the vector pointing to the middle of the platform from the lander
    //   2: X component of the velocity vector of the lander
    //   3: Y component of the velocity vector of the lander
    static final int[] OBSERVATION_SPACE_RESOLUTION = {0, 0, 0, 0}; // TODO

    final double[][] observationSpace;
    double[][][][][] qTable;
    final int[] envActionSpace;
    private final int nIterations;

    double epsilon = 1.0;
    int iteration = 0;
    boolean test = false;

    // your variables here
    // ...
    double[][][][][] bestTable;
    double bestReward = -200;
    double lastReward = -200;

    double alpha = 0.1;
    double gamma = 0.6;
    int epsilon_step = 100;
    double epsilon_decay = 0.9;
    int save_interval = 1000;

    int epoch = 0;

    public LunarLanderAgentBase(double[][] observationSpace, int[] actionSpace, int nIterations) {
        this.observationSpace = observationSpace;
        this.qTable =
                new double[OBSERVATION_SPACE_RESOLUTION[0]]
                        [OBSERVATION_SPACE_RESOLUTION[1]]
                        [OBSERVATION_SPACE_RESOLUTION[2]]
                        [OBSERVATION_SPACE_RESOLUTION[3]]
                        [actionSpace.length];
        this.envActionSpace = actionSpace;
        this.nIterations = nIterations;
    }

    public static int[] quantizeState(double[][] observationSpace, double[] state) {
        return new int[observationSpace.length]; // TODO
    }

    public void epochEnd(double epochRewardSum) {
        return; // TODO
    }

    public void learn(double[] oldState, int action, double[] newState, double reward) {
        return; // TODO
    }

    public void trainEnd() {
        // ... TODO
        qTable = null; // TODO
        test = true;
    }
}
