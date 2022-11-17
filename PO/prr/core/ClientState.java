package prr.core;


import java.io.Serializable;
import java.util.Collection;


public abstract class ClientState implements Serializable {

    // ClientState attributes.
    protected Client _client;
    protected int[] _textPrices;
    protected int _voicePrice;
    protected int _videoPrice;


    /**
     * ClientState class constructor.
     * @param client that is on this state.
     * @param textPrices of this state.
     * @param voicePrice of this state.
     * @param videoPrice of this state.
     */
    public ClientState(Client client, int[] textPrices, int voicePrice, int videoPrice) {
        _client = client;
        _textPrices = textPrices;
        _voicePrice = voicePrice;
        _videoPrice = videoPrice;
    }

    /** @return this state name. */
    public String toString() { return this.getClass().getSimpleName()
            .substring(0,this.getClass().getSimpleName().length() - 5).toUpperCase(); }


    // Communications prices calculation.
    /**
     * computes a Text communication cost.
     * @param comm Text communication to compute price of.
     * @param size of the Text communication.
     * @param extraCost of the Text communication.
     * @return the Text communication price.
     */
    protected double computeCost(Text comm, int size, int extraCost) {
        if(size < 50)
            return _textPrices[0];
        else if (size < 100) {
            return _textPrices[1];
        }
        return getBigTextPrice(_textPrices[2], size, extraCost);
    }

    /**
     * computes a big Text communication cost (length >= 100).
     * @param bigPrice price per character.
     * @param size of the Text communication.
     * @param extra price for Platinum state, (bigPrize = 0 in this case).
     * @return the big Text communication cost.
     */
    private double getBigTextPrice(int bigPrice, int size, int extra) { return (bigPrice * size) + extra; }

    /**
     * computes a Video communication cost.
     * @param comm Video communication to compute price of.
     * @param size of the Video communication.
     * @return the video communication price.
     */
    protected double computeCost(Video comm, int size) {
        return _videoPrice * size;
    }

    /**
     * computes a Voice communication cost.
     * @param comm Voice communication to compute price of.
     * @param size of the Voice communication.
     * @return the Voice communication price.
     */
    protected double computeCost(Voice comm, int size) {
        return _voicePrice * size;
    }


    // Abstract functions skeletons to use in subclasses Normal/Gold/Platinum States.
    protected abstract double computeCost(Text comm);
    protected abstract double computeCost(Video comm);
    protected abstract double computeCost(Voice comm);

    protected abstract void update(long balance);
    protected abstract void update(long balance, Communication comm);
    protected abstract void update(long balance , Collection<Communication> communicationStreak);
}
