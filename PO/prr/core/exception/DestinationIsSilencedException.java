package prr.core.exception;

public class DestinationIsSilencedException extends Exception {
    public DestinationIsSilencedException() {
        super("O terminal de destion encontra-se silenciado!");
    }
}
