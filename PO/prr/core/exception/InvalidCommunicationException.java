package prr.core.exception;

public class InvalidCommunicationException extends Exception{
    public InvalidCommunicationException() {
        super("A comunicação selecionada não existe!");
    }
}
