package prr.core;


import prr.core.exception.DestinationIsOffException;


public class OffState extends TerminalState {

    /**
     * Off State class constructor.
     * @param terminal that has become busy.
     */
    public OffState(Terminal terminal) { super(terminal); }

    /** @return true, State change was successful. */
    @Override
    protected boolean turnOn() {
        super.changeState(new IdleState(_terminal));
        super.notify("OFF","IDLE");
        return true;
    }

    /** @return false, State change can't proceed, Terminal is already off. */
    @Override
    protected boolean turnOff() {
        return false;
    }

    /** @return true, State change was successful. */
    @Override
    protected boolean setOnSilent() {
        super.changeState(new SilenceState(_terminal));
        super.notify("OFF","SILENCE");
        return true;
    }

    /** @return true, State change was successful. */
    @Override
    protected boolean setOnBusy() {
        super.changeState(new BusyState(_terminal));
        return true;
    }

    /** @return false Terminal is off, not ON. */
    @Override
    protected boolean isOn() {
        return false;
    }

    /** @return false Terminal is off, not silenced. */
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
    protected void sendTextCommunication(Terminal destination, Terminal origin, String message) throws DestinationIsOffException {
        destination.getNotifier().subscribe(origin.getAssociate());
        throw new DestinationIsOffException();
    }

    /**
     * Destination Terminal is OFF.
     * @param origin terminal.
     * @param destination terminal.
     * @throws DestinationIsOffException destination terminal is OFF.
     */
    @Override
    protected void checkDestination(Terminal origin, Terminal destination) throws DestinationIsOffException {
        destination.getNotifier().subscribe(origin.getAssociate());
        throw new DestinationIsOffException();
    }
}
