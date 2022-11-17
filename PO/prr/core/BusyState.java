package prr.core;


import prr.core.exception.DestinationIsBusyException;


public class BusyState extends TerminalState {

    /**
     * Busy State class constructor.
     * @param terminal that has become busy.
     */
    public BusyState(Terminal terminal) { super(terminal); }

    /** @return true, State change was successful. */
    @Override
    protected boolean turnOn() {
        super.changeState(new IdleState(_terminal));
        super.notify("BUSY","IDLE");
        return true;
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
        super.notify("BUSY", "SILENCE");
        return true;
    }

    /** @return false, State change can't proceed, Terminal is already busy. */
    @Override
    protected boolean setOnBusy() {
        return false;
    }

    /** @return false Terminal is busy, not ON. */
    @Override
    protected boolean isOn() { return false; }

    /** @return false Terminal is busy, not silent. */
    @Override
    protected boolean isOnSilent() { return false; }

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

    /**
     * Destination Terminal is Busy.
     * @param origin terminal.
     * @param destination terminal.
     * @throws DestinationIsBusyException destination terminal is Busy.
     */
    @Override
    protected void checkDestination(Terminal origin, Terminal destination) throws DestinationIsBusyException {
        destination.getNotifier().subscribe(origin.getAssociate());
        throw new DestinationIsBusyException();
    }
}
