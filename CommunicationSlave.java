import java.util.ArrayList;
import java.util.Scanner;

public class CommunicationSlave {
    public static ArrayList<String> getMessage() {
        // parse params
        Scanner input = new Scanner(System.in);
        String firstLine = input.nextLine();
        int nMsgLines = Integer.parseInt(firstLine);

        // read full answer message
        ArrayList<String> lines = new ArrayList<String>();
        for (int i = 0; i < nMsgLines; i++) {
            String line = input.nextLine();
            lines.add(line);
        }

        return lines;
    }

    public static void sendAnswer(String answer) {
        int nAnswerLines = 0;
        if (answer != null) {
            nAnswerLines = (answer + " ").split("\r?\n").length;
        }

        // send answer
        System.out.printf("%d\n%s\n", nAnswerLines, answer);
        System.out.flush();
    }
}
