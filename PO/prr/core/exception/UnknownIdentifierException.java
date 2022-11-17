package prr.core.exception;

public class UnknownIdentifierException extends Exception{
    public UnknownIdentifierException(String id) {
        super("ID : " + id + " não reconhecido pelo programa");
    }
}
