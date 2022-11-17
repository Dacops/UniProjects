package prr.core.exception;

public class DestinationIsOffException extends Exception {
    public DestinationIsOffException() {
        super("O terminal de destion encontra-se desligado!");
    }
}
