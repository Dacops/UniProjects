package prr.core.exception;

public class DestinationIsBusyException extends Exception {
    public DestinationIsBusyException() {
        super("O terminal de destion encontra-se ocupado!");
    }
}
