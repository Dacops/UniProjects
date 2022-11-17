package prr.core;


import java.util.Collection;


public class NormalState extends ClientState {

    /**
     * Normal State class constructor.
     * @param client that is on this state.
     */
    public NormalState(Client client) {
        super(client, new int[] {10,16,2}, 20,30);
    }


    // Update Client States.
    /**
     * upgrades the State to Gold.
     * @param balance of client.
     */
    @Override
    protected void update(long balance) {
        if(balance > 500)
            _client.changeState(new GoldState(_client));
    }

    /**
     * keeps the State in Normal.
     * @param balance of client.
     * @param comm communication.
     */
    @Override
    protected void update(long balance, Communication comm) {}

    /**
     * keeps the State in Normal.
     * @param balance of client.
     * @param communicationStreak communications streak.
     */
    @Override
    protected void update(long balance , Collection<Communication> communicationStreak) {}


    // Communications cost calculation with NormalState client
    /**
     * computes a Text communication cost.
     * @param comm Text communication cost to compute.
     * @return computed Text communication cost.
     */
    @Override
    protected double computeCost(Text comm) { return super.computeCost(comm, comm.getSize(),0); }

    /**
     * computes a Video communication cost.
     * @param comm Video communication cost to compute.
     * @return computed Video communication cost.
     */
    @Override
    protected double computeCost(Video comm) { return super.computeCost(comm, comm.getSize()); }

    /**
     * computes a Voice communication cost.
     * @param comm Voice communication cost to compute.
     * @return computed Voice communication cost.
     */
    @Override
    protected double computeCost(Voice comm) { return super.computeCost(comm, comm.getSize()); }
}
