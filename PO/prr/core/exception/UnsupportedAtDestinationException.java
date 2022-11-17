package prr.core.exception;

public class UnsupportedAtDestinationException extends Exception {
    public UnsupportedAtDestinationException() {
        super("O terminal de destino não consegue realizar essa operação!");
    }
}
