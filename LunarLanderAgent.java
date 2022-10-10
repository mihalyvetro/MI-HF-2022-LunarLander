import java.util.Random;

public class LunarLanderAgent extends LunarLanderAgentBase {
    Random randomGenerator = new Random();

    public LunarLanderAgent(double[][] observationSpace, int[] actionSpace, int nIterations) {
        super(observationSpace, actionSpace, nIterations);
    }

    public int step(double[] state) {
        int[] stateQuantized = LunarLanderAgentBase.quantizeState(this.observationSpace, state);
        int action = 0;
        if (!this.test && (Math.random() < this.epsilon)) {
            action = this.envActionSpace[ // explore action space
                    this.randomGenerator.nextInt(this.envActionSpace.length)];
        } else {
            action = // exploit learned
                    argmax(this.qTable[stateQuantized[0]]
                            [stateQuantized[1]]
                            [stateQuantized[2]]
                            [stateQuantized[3]]);
        }

        return action;
    }
    public static int argmax(double[] array) {
        double max = array[0];
        int re = 0;
        for (int i = 1; i < array.length; i++) {
            if (array[i] > max) {
                max = array[i];
                re = i;
            }
        }
        return re;
    }
}
