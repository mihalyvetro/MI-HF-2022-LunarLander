import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.Scanner;

public class CommunicationSlave {
    RandomAccessFile streamToSlave;
    RandomAccessFile streamFromSlave = null;
    String pipeFromSlavePath;
    String pipeToSlavePath;

    public CommunicationSlave(String pipeToSlavePath, String pipeFromSlavePath) {
        this.pipeFromSlavePath = pipeFromSlavePath;
        this.pipeToSlavePath = pipeToSlavePath;

        try {
            streamToSlave = new RandomAccessFile(pipeToSlavePath, "r");
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    public ArrayList<String> getMessage() {
        // parse params
        String firstLine;
        try {
            firstLine = streamToSlave.readLine();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        int nMsgLines = Integer.parseInt(firstLine);

        // read full answer message
        ArrayList<String> lines = new ArrayList<String>();
        for (int i = 0; i < nMsgLines; i++) {
            String line;
            try {
                line = streamToSlave.readLine();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            lines.add(line);
        }

        return lines;
    }

    public void sendAnswer(String answer) {
        if (streamFromSlave == null) {
            try {
                streamFromSlave = new RandomAccessFile(pipeFromSlavePath, "rw");
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }
        }

        int nAnswerLines = 0;
        if (answer != null) {
            nAnswerLines = (answer + " ").split("\r?\n").length;
        }

        // send answer
        try {
            streamFromSlave.write(String.format("%d\n%s\n", nAnswerLines, answer).getBytes());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
