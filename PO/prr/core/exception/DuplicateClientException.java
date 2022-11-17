package prr.core.exception;

public class DuplicateClientException extends Exception{
    public DuplicateClientException() {
        super("ID do utilizador disponibilizado já existe!");
    }
}
