package prr.core;


import java.util.Collection;


public class PlatinumState extends ClientState{

    private int streak = 0;
    /**
     * Platinum State class constructor.
     * @param client that is on this state.
     */
    public PlatinumState(Client client) {
        super(client, new int[] {0, 4, 0},10,10);
    }


    // Update Client States.
    /**
     * keeps the State in Platinum.
     * @param balance of client.
     */
    @Override
    protected void update(long balance){}

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
     * downgrades the State to Gold.
     * @param balance of client.
     * @param communicationStreak communications streak.
     */
    @Override
    protected void update(long balance, Collection<Communication> communicationStreak) { /*dentro do computeCost do Text*/
    }


    // Communications cost calculation with NormalState client
    /**
     * computes a Text communication cost.
     * @param comm Text communication cost to compute.
     * @return computed Text communication cost.
     */
    @Override
    protected double computeCost(Text comm) {
        streak += 1;
        if(streak >= 2 && _client.getBalance() > 0)
            _client.changeState(new GoldState(_client));
        return super.computeCost(comm, comm.getSize(),4); }

    /**
     * computes a Video communication cost.
     * @param comm Video communication cost to compute.
     * @return computed Video communication cost.
     */
    @Override
    protected double computeCost(Video comm) { streak = 0; return super.computeCost(comm, comm.getSize()); }

    /**
     * computes a Voice communication cost.
     * @param comm Voice communication cost to compute.
     * @return computed Voice communication cost.
     */
    @Override
    protected double computeCost(Voice comm) { streak = 0; return super.computeCost(comm, comm.getSize()); }
}