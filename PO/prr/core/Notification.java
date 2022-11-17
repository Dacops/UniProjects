package prr.core;

import java.io.Serializable;

enum NotificationType{
    O2S,
    O2I,
    B2S,
    B2I,
    S2I;
}

public class Notification implements Serializable {

    // Notification attributes
    private NotificationType _type;
    private final Terminal _terminalNotifying;
    private final String _fromID;
    private boolean _isvalid;


    /**
     * Notification Class Constructor.
     * @param beforeState previous terminal state.
     * @param afterState new terminal state.
     * @param terminal terminal where the notifications are being created.
     */
    public Notification(String beforeState, String afterState, Terminal terminal) {
        _terminalNotifying = terminal;
        _fromID = terminal.getID();
        _isvalid = true;
        switch (beforeState) {
            case "OFF" :
                switch (afterState) {
                    case "SILENCE" -> _type = NotificationType.O2S;
                    case "IDLE" -> _type = NotificationType.O2I;
                }
                break;
            case "BUSY" :
                switch (afterState) {
                    case "SILENCE" -> _type = NotificationType.B2S;
                    case "IDLE" -> _type = NotificationType.B2I;
                }
                break;
            case "SILENCE" :
                if(afterState.equals("IDLE"))
                    _type = NotificationType.S2I;
                break;
            default:
                _isvalid = false;
                break;
        }
    }

    public boolean isvalid() { return _isvalid; }

    public String getFromID() { return _fromID; }

    /** @return a String with the format NotificationType|TerminalID. */
    public String toString() { return _type.toString() + "|" + _terminalNotifying.getID(); }
}
