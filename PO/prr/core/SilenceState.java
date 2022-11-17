package prr.core;


import prr.core.exception.DestinationIsSilencedException;


public class SilenceState extends TerminalState {

    /**
     * Silence State class constructor.
     * @param terminal that has become busy.
     */
    public SilenceState(Terminal terminal) { super(terminal); }

    /** @return true, State change was successful. */
    @Override
    protected boolean turnOn() {
        super.changeState(new IdleState(_terminal));
        super.notify("SILENCE","IDLE");
        return true;
    }

    /** @return true, State change was successful. */
    @Override
    protected boolean turnOff() {
        super.changeState(new OffState(_terminal));
        return true;
    }

    /** @return false, State change can't proceed, Terminal is already silenced. */
    @Override
    protected boolean setOnSilent() {
        return false;
    }

    /** @return true, State change was successful. */
    @Override
    protected boolean setOnBusy() {
        super.changeState(new BusyState(_terminal));
        return true;
    }

    /** @return false Terminal is silenced, not ON. */
    @Override
    protected boolean isOn() {
        return false;
    }

    /** @return true Terminal is silenced. */
    @Override
    protected boolean isOnSilent() {
        return true;
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

    /**
     * Destination Terminal is Silenced.
     * @param origin terminal.
     * @param destination terminal.
     * @throws DestinationIsSilencedException destination terminal is Silenced.
     */
    @Override
    protected void checkDestination(Terminal origin, Terminal destination) throws DestinationIsSilencedException {
        destination.getNotifier().subscribe(origin.getAssociate());
        throw new DestinationIsSilencedException();
    }
}
