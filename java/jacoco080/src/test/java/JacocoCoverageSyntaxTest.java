import org.junit.Test;

import static org.junit.Assert.*;

public class JacocoCoverageSyntaxTest {
    @Test
    public void constructor() throws Exception {
        JacocoCoverageSyntax obj = new JacocoCoverageSyntax();
    }

    @Test
    public void tryCatchResource() throws Exception {
        JacocoCoverageSyntax.tryCatchResource("build.gradle");
        JacocoCoverageSyntax.tryCatchResource("non");
        try {
            JacocoCoverageSyntax.tryCatchResource(null);
            fail();
        } catch (NullPointerException ex) {
            // OK
        }
    }

    @Test
    public void stringSwitch() throws Exception {
        JacocoCoverageSyntax.StringSwitch("A");
        JacocoCoverageSyntax.StringSwitch("B");
        JacocoCoverageSyntax.StringSwitch("C");
        JacocoCoverageSyntax.StringSwitch("D");
    }

    @Test
    public void synchronizedPrint() throws Exception {
        JacocoCoverageSyntax.synchronizedPrint("taro");
        try {
            JacocoCoverageSyntax.synchronizedPrint(null);
            fail();
        } catch (NullPointerException ex) {
            //OK
        }

        try {
            JacocoCoverageSyntax.synchronizedPrint("A");
            fail();
        } catch (RuntimeException ex) {
            //OK
        }
    }

    @Test
    public void enum_values_valueOf() throws Exception {
        JacocoCoverageSyntax.DummyEnum d;
        d = JacocoCoverageSyntax.DummyEnum.RED;
        d = JacocoCoverageSyntax.DummyEnum.YELLOW;
        d = JacocoCoverageSyntax.DummyEnum.GREEN;

        // --------------------------------------------------------
        // values() and valueOf()
        // In jacoco 0.7.9 or previous, you need to test each method
        // to accomplish 100% coverage.
        // --------------------------------------------------------
//        JacocoCoverageSyntax.DummyEnum.values();
//
//        d = JacocoCoverageSyntax.DummyEnum.valueOf("RED");
//        assertEquals(JacocoCoverageSyntax.DummyEnum.RED, d);
    }
}