import java.io.*;

public class TestA {
    static String f;
    TestA() {

    }
    // AMAHelper: 1
    public void onCreate() {
        foo(); // AMAHelper: control 2
        bar(); // AMAHelper: control 3
    }
    // AMAHelper: 1

    // AMAHelper: 2
    private void foo(){
        f = "sensitive data"; // AMAHelper: data 3
    }
    // AMAHelper: 2

    // AMAHelper: 3
    private void bar(){
        System.out.println(f);
    }
    // AMAHelper: 3

}