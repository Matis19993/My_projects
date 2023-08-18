package lab.book;

public class MsBookException extends RuntimeException{

    public MsBookException(String message) {
        super(message);
    }

    public MsBookException(String message, Throwable cause) {
        super(message, cause);
    }
}
