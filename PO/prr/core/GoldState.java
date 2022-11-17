package prr.core;


import java.util.Collection;


public class GoldState extends ClientState{

    private double streak = 0;

    /**
     * Gold State class constructor.
     * @param client that is on this state.
     */
    public GoldState(Client client) {
        super(client, new int[] {10,10,2}, 10,20);
    }


    // Update Client States.
    /**
     * keeps the state in Gold
     * @param balance of client.
     */
    @Override
    protected void update(long balance) {}

    /**
     * downgrades the State to Normal.
     * @param balance of client.
     * @param comm communication.
     */
    @Override
    protected void update(long balance, Communication comm) {
        if(balance < 0)
            _client.changeState(new NormalState(_client));
    }

    /**
     * upgrades the State to Platinum.
     * @param balance of client.
     * @param communicationStreak communications streak.
     */
    @Override
    protected void update(long balance , Collection<Communication> communicationStreak) {
        if(streak >= 5.0 && balance > 0)
            _client.changeState(new PlatinumState(_client));
    }


    // Communications cost calculation with GoldState client
    /**
     * computes a Text communication cost.
     * @param comm Text communication cost to compute.
     * @return computed Text communication cost.
     */
    @Override
    protected double computeCost(Text comm) { streak = 0; return super.computeCost(comm, comm.getSize(),0); }

    /**
     * computes a Video communication cost.
     * @param comm Video communication cost to compute.
     * @return computed Video communication cost.
     */
    @Override
    protected double computeCost(Video comm) { streak += 0.5; return super.computeCost(comm, comm.getSize()); }

    /**
     * computes a Voice communication cost.
     * @param comm Voice communication cost to compute.
     * @return computed Voice communication cost.
     */
    @Override
    protected double computeCost(Voice comm) { streak = 0; return super.computeCost(comm, comm.getSize()); }
}
