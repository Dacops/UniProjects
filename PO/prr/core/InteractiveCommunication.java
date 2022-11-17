package prr.core;


abstract public class InteractiveCommunication extends Communication {

    /** InteractiveCommunication attributes */
    private int _duration; //only added when communication is ended

    /**
     * InteractiveCommunication class constructor.
     * @param from origin terminal.
     * @param to destination terminal.
     */
    public InteractiveCommunication(Terminal from, Terminal to) {
        super(from, to);
        _isOngoing = true;
    }

    /**
     * Calculates the message length.
     * @return the message length in int form.
     */
    @Override
    protected int getSize() { return _duration; }

    /** @param duration duration of the communication. */
    protected void addDuration(int duration) {
        _duration = duration;
    }

    /** @param cost of the communication. */
    protected void sendCost(double cost) { super.addCost(cost); }

    protected void freeTerminals() { super.freeTerminals(); }

    /** @return the Client that created the communication. */
    protected Client getClient() { return super.getClient(); }

    protected void terminateComm() { _isOngoing = false; }


    // Abstract function skeleton to use in subclasses Video/Voice Communications.
    protected abstract long endCommunication(int duration);
}