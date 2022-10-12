import java.util.ArrayList;
import java.util.Arrays;

public class StudentCodeBinder {
    public static void main(String[] args) {
        String pipeToSlavePath = args[0];
        String pipeFromSlavePath = args[1];

        CommunicationSlave cs = new CommunicationSlave(pipeToSlavePath, pipeFromSlavePath);
        
        // initialization
        ArrayList<String> init_msg = cs.getMessage();
        boolean msg_ok =
                init_msg.contains("observation_space") &&
                init_msg.contains("action_space") &&
                init_msg.contains("n_iterations");

        if (!msg_ok) {
            cs.sendAnswer("0");
        }

        int observationSpaceIdx = init_msg.indexOf("observation_space");
        int actionSpaceIdx = init_msg.indexOf("action_space");
        int nIterationsIdx = init_msg.indexOf("n_iterations");

        // parse init parameters
        int observation_space_size = actionSpaceIdx - observationSpaceIdx - 1;
        double[][] observationSpace = new double[observation_space_size][2];
        for (int row = 0; row < observation_space_size; row++) {
            double[] values = Arrays.stream(init_msg.get(observationSpaceIdx + 1 + row)
                            .split(","))
                    .mapToDouble(Double::parseDouble)
                    .toArray();
            observationSpace[row] = values;
        }
        int[] action_space = Arrays.stream(init_msg.get(actionSpaceIdx + 1).split(", "))
                .mapToInt(Integer::valueOf)
                .toArray();
        int nIterations = Integer.parseInt(init_msg.get(nIterationsIdx+1));

        LunarLanderAgent agent = new LunarLanderAgent(observationSpace, action_space, nIterations);
        cs.sendAnswer("1");

        // process commands
        boolean end = false;
        while (!end) {
            ArrayList<String> command = cs.getMessage();

            switch (command.get(0)) {
                case "step": {
                    double[] state = Arrays.stream(command.get(1).split(", "))
                            .mapToDouble(Double::parseDouble)
                            .toArray();
                    int action = agent.step(state);
                    cs.sendAnswer(String.valueOf(action));
                }
                    break;
                case "learn": {
                    double[] oldState = Arrays.stream(command.get(1).split(", "))
                            .mapToDouble(Double::parseDouble)
                            .toArray();
                    int action = Integer.valueOf(command.get(2));
                    double[] newState = Arrays.stream(command.get(3).split(", "))
                            .mapToDouble(Double::parseDouble)
                            .toArray();
                    double reward = Double.valueOf(command.get(4));
                    agent.learn(oldState, action, newState, reward);
                    cs.sendAnswer("1");
                }
                    break;
                case "epoch_end":
                    double epochRewardSum = Double.valueOf(command.get(1));
                    agent.epochEnd(epochRewardSum);
                    cs.sendAnswer("1");
                    break;
                case "train_end":
                    agent.trainEnd();
                    cs.sendAnswer("1");
                    break;
                default:
                    cs.sendAnswer("1");
                    end = true;
            }

        }

    }
}