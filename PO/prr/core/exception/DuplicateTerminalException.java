package prr.core.exception;

public class DuplicateTerminalException extends Exception{
    public DuplicateTerminalException() {
        super("ID do terminal disponibilizado já existe!");
    }
}
