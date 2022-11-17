package prr.core;


import prr.core.exception.UnknownIdentifierException;

import java.io.Serializable;
import java.util.*;


public class Client implements Serializable {

    // Client's Attributes.
    private final String _id;
    private final String _name;
    private final int _taxNumber;
    private ClientState _state;
    private boolean _receiveNotifications;
    private double _debts;
    private double _payments;
    private Map<String, Terminal> _terminals;
    private Map<Integer,Communication> _madeCommunications;
    private Map<Integer,Communication> _receivedCommunications;
    private List<Notification> _notifications;


    /**
     * 3.2.3. -> Client's Constructor.
     * @param id Client's unique id.
     * @param name Client's name.
     * @param taxNumber Client's tax number.
     **/
    public Client(String id, String name, int taxNumber) {
        _id = id;
        _name = name;
        _taxNumber = taxNumber;
        _receiveNotifications = true;
        _terminals = new TreeMap<>();
        _madeCommunications = new TreeMap<>();
        _receivedCommunications = new TreeMap<>();
        _state = new NormalState(this);
        _notifications = new ArrayList<>();
    }



    // Returns.
    /** @return the Client ID. */
    protected String getID() { return _id; }

    /** @return the Client name. */
    protected String getName() { return _name; }

    /** @return the Client TaxID. */
    protected int getTaxID() { return _taxNumber; }

    /** @return the client state. */
    protected ClientState getState() { return _state; }

    /** @return true if the client can receive notifications, false otherwise. */
    public boolean isReceivingNotifications() { return _receiveNotifications; }

    // 3.2.6.
    /** @return debts rounded. */
    public long getDebts() { return Math.round(_debts); }

    // 3.2.6.
    /** @return payments rounded. */
    public long getPayments() { return Math.round(_payments); }

    /** @return the client terminals. */
    protected Collection<Terminal> getTerminals() { return Collections.unmodifiableCollection(_terminals.values()); }

    /** @return the client made communications. */
    public Collection<Communication> getMadeComms() { return Collections.unmodifiableCollection(_madeCommunications.values()); }

    /** @return the client received communications. */
    public Collection<Communication> getReceivedComms() { return Collections.unmodifiableCollection(_receivedCommunications.values()); }

    /** @return the client notifications. */
    public Collection<Notification> getNotifications() { return Collections.unmodifiableCollection(_notifications); }



    // More Complex Functions.

    // State Functions.
    /** @param state new Client state. */
    protected void changeState(ClientState state) { _state = state; }


    // Notifications Functions.
    // 3.2.4. / 3.2.5. -> turns ON / OFF the notifications.
    public void toggleReceivingNotifications() { _receiveNotifications = !_receiveNotifications; }

    public void clearNotifications(Network network) throws UnknownIdentifierException {
        String fromID;
        for(Notification n: _notifications) {
            fromID = n.getFromID();
            network.getTerminal(fromID).unsubscribe(this);
        }
        _notifications.clear();
    }

    /** @param notification to add. */
    protected void receiveNotification(Notification notification) {
        if (_receiveNotifications) { _notifications.add(notification); }
    }


    // Debt / Payment Functions.
    /** @param debt to add. */
    protected void addDebt(double debt) { _debts += debt; }

    /** @param payment to add. */
    protected void addPayment(double payment) { _payments += payment; }

    /** @return true if the client has debts, false otherwise. */
    public boolean hasDebt() { return _debts > 0; }

    /** @return the Client balance rounded. */
    protected long getBalance() { return Math.round(_payments-_debts); }


    // Terminal Functions.
    /** @param t new Terminal to add to the Client. */
    protected void addTerminal(Terminal t) { _terminals.put(t.getID(),t); }

    /** @return true if the Client has no terminals, false otherwise. */
    protected boolean hasNoTerminals() { return _terminals == null; }

    /** @return the number of the Client active terminals. */
    protected int getNumActiveTerminals() {
        if(hasNoTerminals())
            return 0;
        return _terminals.values().size();
    }


    // Communication functions.
    /** @param c new Communication to add to the made Client Communications. */
    protected void addMadeComm(Communication c) { _madeCommunications.put(c.getID(), c); }

    /** @param c new Communication to add to the received Client Communications. */
    protected void addReceivedComm(Communication c) { _receivedCommunications.put(c.getID(), c); }

    /** @return YES if the Clients receives communications, NO otherwise. */
    protected String getNotificationYorN() { return _receiveNotifications ? "YES" : "NO" ;}


    // Payments functions.
    /** @param comm Text Communication to calculate cost. */
    protected double computeCost(Text comm) { return _state.computeCost(comm);}

    /** @param comm Video Communication to calculate cost. */
    protected double computeCost(Video comm) { return _state.computeCost(comm);}

    /** @param comm Voice Communication to calculate cost. */
    protected double computeCost(Voice comm) { return _state.computeCost(comm);}

    /** @param value of the payment. */
    protected void pay(double value) {
        _debts -= value;
        addPayment(value);
        _state.update(getBalance());
    }


    // Print Client Information functions.
    /** @return a String with the format CLIENT|id|nome|taxId. */
    protected String getReadyToWrite() { return "CLIENT|" + this.getID() + "|" + this.getName()
            + "|" + this.getTaxID(); }

    /**
     * 3.2.1. / 3.2.2.
     * @return a String in the format CLIENT|key|name|taxID|notifications|terminals|payments|debts.
     * */
    public String getReadyToDisplay() { return getReadyToWrite() +"|"+ _state.toString()
            +"|" + getNotificationYorN() + "|" + getNumActiveTerminals() + "|" + getPayments() + "|" + getDebts(); }
}
