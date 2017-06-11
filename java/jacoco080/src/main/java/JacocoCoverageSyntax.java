import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class JacocoCoverageSyntax {

    public static void tryCatchResource(String fileName) {
        try(BufferedReader br = new BufferedReader(
                new FileReader(fileName))) {
            String firstLine = br.readLine();
            System.out.println(firstLine);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void StringSwitch(String s) {
        switch (s) {
            case "A": break;
            case "B": break;
            case "C": break;
            default: break;
        }
    }


    static Object lock = new Object();

    //TODO: find out the uncovered pattern.
    public static void synchronizedPrint(String name) {
        synchronized (lock) {
            System.out.println(name.length());
            if(name.length() == 1) {
                throw new RuntimeException();
            }
        }
    }

    enum DummyEnum {
        RED, YELLOW, GREEN;
    }

}
