package prr.core;


public class Video extends InteractiveCommunication {

    // Video attributes
    private final double _friendMultiplier;  //if it's friend 50% discount

    /**
     * Video class constructor.
     * @param from terminal where the communication is started.
     * @param to terminal where the communication is received.
     */
    public Video(Terminal from, Terminal to, boolean isFriend) {
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

    /** @return false, it's Video. */
    @Override
    protected boolean isVoice() { return false; }

    /** @return true, it's Video. */
    @Override
    protected boolean isVideo() { return true; }

    /** @return false, it's Video. */
    @Override
    protected boolean isText() { return false; }

    /** @return the cost of the communication. */
    @Override
    protected double computeCost() { return super.getClient().computeCost(this); }
}