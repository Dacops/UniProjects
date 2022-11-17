package prr.core;


public class Voice extends InteractiveCommunication {

    // Video attributes
    private final double _friendMultiplier; //if it's friend 50% discount

    /**
     * Voice class constructor.
     * @param from terminal where the communication is started.
     * @param to terminal where the communication is received.
     */
    public Voice(Terminal from, Terminal to, boolean isFriend) {
        super(from, to);
        _friendMultiplier = (isFriend) ? .5 : 1;
    }

    /**
     * Ends this communication.
     * @param duration of the communication.
     * @return the cost of the communication.
     */
    @Override
    protected long endCommunication(int duration) {
        super.addDuration(duration);
        super.terminateComm();
        super.sendCost(_friendMultiplier * computeCost());
        return Math.round(_friendMultiplier * computeCost());
    }

    /** @return true, it's Voice. */
    @Override
    protected boolean isVoice() { return true; }

    /** @return false, it's Voice. */
    @Override
    protected boolean isVideo() { return false; }

    /** @return false, it's Voice. */
    @Override
    protected boolean isText() { return false; }

    /** @return the cost of the communication. */
    @Override
    protected double computeCost() { return super.getClient().computeCost(this); }
}