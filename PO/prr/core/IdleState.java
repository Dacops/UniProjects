package prr.core;

public class IdleState extends TerminalState {

    /**
     * Idle State class constructor.
     * @param terminal that has become busy.
     */
    public IdleState(Terminal terminal) { super(terminal); }

    /** @return false, State change can't proceed, Terminal is already on. */
    @Override
    protected boolean turnOn() {
        return false;
    }

    /** @return true, State change was successful. */
    @Override
    protected boolean turnOff() {
        super.changeState(new OffState(_terminal));
        return true;
    }

    /** @return true, State change was successful. */
    @Override
    protected boolean setOnSilent() {
        super.changeState(new SilenceState(_terminal));
        return true;
    }

    /** @return true, State change was successful. */
    @Override
    protected boolean setOnBusy() {
        super.changeState(new BusyState(_terminal));
        return true;
    }

    /** @return true Terminal is ON. */
    @Override
    protected boolean isOn() {
        return true;
    }

    /** @return false Terminal is ON, not silenced. */
    @Override
    protected boolean isOnSilent() {
        return false;
    }

    /**
     * Sends a Text Communication.
     * @param destination terminal.
     * @param origin terminal.
     * @param message to send.
     */
    @Override
    protected void sendTextCommunication(Terminal destination, Terminal origin, String message) {
        new Text(message, origin, destination);
    }

    //does nothing, communication possible
    @Override
    protected void checkDestination(Terminal origin, Terminal destination) {}
}
