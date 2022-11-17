package prr.core.exception;

public class UnsupportedAtOriginException extends Exception {
    public UnsupportedAtOriginException() {
        super("Este terminal não consegue realizar essa operação!");
    }
}
