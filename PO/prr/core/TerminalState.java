package prr.core;


import prr.core.exception.DestinationIsBusyException;
import prr.core.exception.DestinationIsOffException;
import prr.core.exception.DestinationIsSilencedException;

import java.io.Serializable;


public abstract class TerminalState implements Serializable {

    // TerminalState attributes.
    Terminal _terminal;

    /**
     * TerminalState class constructor
     * @param terminal that is on this state.
     */
    public TerminalState(Terminal terminal) {
        this._terminal = terminal;
    }

    /** @return this terminal State. */
    public String toString() { return this.getClass().getSimpleName()
            .substring(0,this.getClass().getSimpleName().length() - 5).toUpperCase(); }

    /**
     * creates notifications.
     * @param beforeState previous terminal state.
     * @param afterState new terminal state.
     */
    protected void notify(String beforeState, String afterState) { _terminal.getNotifier().notifyClients(beforeState,afterState); }

    protected void checkForNotification(TerminalState newState) {
        switch (newState.toString()) {
            case "IDLE" -> this.turnOn();
            case "SILENT" -> this.setOnSilent();
            default -> changeState(newState);
        }
    }

    // Abstract functions skeletons to use in subclasses Idle/Off/Busy/Silenced States.
    protected abstract boolean turnOn();
    protected abstract boolean turnOff();
    protected abstract boolean setOnSilent();
    protected abstract boolean setOnBusy();
    protected void changeState(TerminalState newState) { _terminal.changeState(newState); }
    protected abstract boolean isOn();
    protected abstract boolean isOnSilent();
    protected abstract void sendTextCommunication(Terminal destination, Terminal origin, String message) throws DestinationIsOffException;
    protected abstract void checkDestination(Terminal origin, Terminal destination) throws DestinationIsOffException, DestinationIsBusyException,
                                                                                                                    DestinationIsSilencedException;
}
