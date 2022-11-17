package prr.core;


public class Text extends Communication {

    /** TextCommunication attributes */
    private String _message;

    /**
     * Text class constructor.
     *
     * @param message message sent.
     * @param from terminal where the communication is started.
     * @param to terminal where the communication is received.
     */
    public Text(String message, Terminal from, Terminal to) {
        super(from, to);
        _message = message;
        _isOngoing = false;
        super.addCost(computeCost());
    }

    /**
     * Calculates the message length.
     * @return the message length in int form.
     */
    @Override
    protected int getSize() {
        return _message.length();
    }

    /** @return false, it's Text. */
    @Override
    protected boolean isVoice() { return false; }

    /** @return false, it's Text. */
    @Override
    protected boolean isVideo() { return false; }

    /** @return true, it's Text. */
    @Override
    protected boolean isText() { return true; }

    /** @return the cost of the communication. */
    @Override
    protected double computeCost() { return super.getClient().computeCost(this); }
}