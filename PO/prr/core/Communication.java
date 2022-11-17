package prr.core;

import java.io.Serializable;

abstract public class Communication implements Serializable {

    // Communication Attributes.
    private static int _counter;
    private int  _id;
    private boolean _isPaid;
    double _cost;
    boolean _isOngoing;
    private Terminal _from;
    private Terminal _to;

    /**
     * Communication class constructor.
     * @param from origin terminal.
     * @param to destination terminal.
     */
    public Communication(Terminal from, Terminal to) {
        _counter += 1;
        _id = _counter; //count upwards
        _isPaid = false;
        _cost = 0;
        _from = from.addMade(this);
        _to = to.addReceived(this);
    }

    protected void changeID(int id) { _id = id; }
    // Returns.
    /** @return this communication ID. */
    protected int getID() { return this._id; }

    /** @return if this communication is paid. */
    protected boolean isPaid() { return _isPaid; }

    /** @return this communication cost. */
    protected double getCost() {
        return _cost;
    }

    /** @return "ONGOING" if the communication is ongoing, "FINISHED" otherwise. */
    protected String getStatus() { return _isOngoing ? "ONGOING" : "FINISHED"; }

    /** @return this communication sender. */
    protected Client getClient() { return _from.getAssociate(); }

    protected void setPaidTrue() { _isPaid = true; }


    // More Complex Functions.
    /** @param cost of the communication to origin terminal. */
    protected void addCost(double cost) {
        _cost = cost;
        _from.addDebt(_cost);
    }

    /** frees both origin and destination terminals. */
    protected void freeTerminals() {
        this._from.getState().checkForNotification(_from.getOriginalState());
        this._to.getState().checkForNotification(_to.getOriginalState());
    }


    // Print Communication Information function.
    /** @return a String with the format type|idCommunication|idSender|idReceiver|units|price|status. */
    public String getReadyToDisplay() { return this.getClass().getSimpleName().toUpperCase() + "|" + this.getID() + "|" +  _from.getID() + "|"
            + _to.getID() + "|" + this.getSize() + "|" + Math.round(_cost) + "|" + this.getStatus(); }


    // Abstract functions skeletons to use in subclasses Text/Video/Voice Communications.
    protected abstract int getSize();
    protected abstract boolean isVoice();
    protected abstract boolean isVideo();
    protected abstract boolean isText();
    protected abstract double computeCost();
}