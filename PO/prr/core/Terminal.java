package prr.core;


import java.io.Serializable;
import java.util.*;
import java.util.stream.Collectors;

import prr.core.exception.*;


abstract public class Terminal implements Serializable {


  private static final long serialVersionUID = 202208091753L;
  
  // Terminal Attributes.
  private String _id;
  private double _debt;
  private double _payments;
  private TerminalState _stateBefore;
  private TerminalState _state;
  private Client _associate;
  protected Set<String> _friends;
  private Map<Integer,Communication> _madeCommunications;
  private Map<Integer,Communication> _receivedCommunications;
  protected InteractiveCommunication _ongoingCommunication;
  private Notifier _notifier;
  protected Network _network;


  /**
   * Terminal class constructor.
   * @param id ID of the created terminal.
   * @param associate ID of the owner of the created terminal.
   */
  public Terminal(String id, Client associate, Network network) {
    _id = id;
    _debt = 0.0;
    _payments = 0.0;
    _state = new IdleState(this);
    _associate = associate;
    _friends = new TreeSet<>();
    _madeCommunications = new TreeMap<>();
    _receivedCommunications = new TreeMap<>();
    _ongoingCommunication = null;
    _stateBefore = null;
    _notifier = new NotificationSender(this);
    _network = network;
  }


  // Returns.
  /** @return terminal id. */
  public String getID() { return this._id; }

  /** @return terminal debt amount. */
  protected double getDebt() { return  this._debt; }

  /** @return terminal payments amount. */
  protected double getPayments() { return  this._payments; }

  /** @return previous terminal state. */
  protected TerminalState getOriginalState() { return _stateBefore; }

  /** @return this terminal state. */
  protected TerminalState getState() { return this._state; }

  /** @return associated client id. */
  protected Client getAssociate() { return this._associate; }

  /** @return this terminal notifier. */
  protected Notifier getNotifier() { return _notifier; }

  protected Network getNetwork() { return _network; }

  // More Complex Functions
  /** @return this terminal balance. */
  protected double getBalance() { return getPayments()-getDebt(); }

  /** @return a Set with terminal made communications. */
  protected Map<Integer, Communication> getMadeComms() { return Collections.unmodifiableMap(_madeCommunications); }

  /**
   * adds a received Communication.
   * @param c Communication to add.
   * @return this terminal.
   */
  protected Terminal addReceived(Communication c) {
    _associate.addReceivedComm(c);
    _receivedCommunications.put(c.getID(), c);
    return this;
  }

  /**
   * adds a made Communication.
   * @param c Communication to add.
   * @return this terminal.
   */
  protected Terminal addMade(Communication c) {
    c.changeID(_network.getAllComms().size()+1);
    _associate.addMadeComm(c);
    _network.addCommunication(c);
    _madeCommunications.put(c.getID(), c);
    return this;
  }

  /** @param cost to add to debt. */
  protected void addDebt(double cost) {
    _debt += cost;
    _associate.addDebt(cost);
  }

  /** @return a String with all terminal friends IDs. */
  public String getFriendsIDs() {
    return _friends.isEmpty() ? "" : "|" + _friends.stream().map(String::toString).collect(Collectors.joining(","));
  }

  /** @return a String with the format terminalType|terminalId|ClientId|TerminalStatus. */
  public String getReadyToWrite() { return this.getClass().getSimpleName().toUpperCase()+ "|" + this.getID() + "|" + this.getAssociate().getID()
          + "|" + _state.toString(); }

  /** @return a String with the format terminalType|terminalId|ClientId|TerminalStatus|balance-paid|balance-debts|friend1,...,friend. */
  public String getReadyToDisplay() { return getReadyToWrite() +"|"+ Math.round(getPayments())
          +"|" + Math.round(getDebt()) + getFriendsIDs() ; }

  /**
   * 3.5.1, 3.5.2, 3.5.3 -> turns the terminals to On/Off/Silence/Busy modes.
   * @return true if the terminal state changes, false if it's already the requested state
   */
  public boolean turnOn() { return _state.turnOn(); }
  public boolean turnOff() { return _state.turnOff(); }

  public boolean setOnSilent() { return _state.setOnSilent(); }
  public boolean setOnBusy() { return _state.setOnBusy(); }

  /** @param newState change terminal to given state. */
  public void changeState(TerminalState newState) {
    _stateBefore = _state;
    _state = newState;
  }

  /**
   * 3.5.4 -> adds a new friend terminal to this terminal friends.
   * @param id id of terminal to add as friend.
   */
    public void addFriend(String id) { _friends.add(id); }

  /**
   * 3.5.5 -> removes a friend terminal from this terminal friends.
   * @param id id of terminal to remove as friend.
   */
    public void removeFriend(String id) { _friends.remove(id); }

  /**
   * 3.5.6 -> pays a communication.
   * @param id communication to pay.
   * @throws InvalidCommunicationException communication does not exist.
   */
    public void payCommunication(int id) throws InvalidCommunicationException {
      if (this._madeCommunications.containsKey(id)) {
        var communication = _madeCommunications.get(id);
        var cost = communication.getCost();
        if(!communication.isPaid() && !communication._isOngoing) {
          _debt -= cost;
          _payments += cost;
          _associate.pay(cost);
          communication.setPaidTrue();
          return;
        }
        throw new InvalidCommunicationException();
      }
      throw new InvalidCommunicationException();
    }

  /**
   * 3.5.7 -> gets payments/debts of this terminal
   * @return the payments/debts of this terminal
   */
  public long showPayments() { return Math.round(_payments); }

  public long showDebts() { return Math.round(_debt); }

  public boolean notUsed() { return _madeCommunications.isEmpty() && _receivedCommunications.isEmpty(); }

  /**
   * 3.5.8 -> send a text communication.
   * @param destinationID ID of the destination terminal.
   * @param message to send in the communication.
   * @throws UnknownIdentifierException given terminal does not exist.
   * @throws DestinationIsOffException destination terminal is turned off.
   */
  public void sendTextCommunication(String destinationID, String message) throws UnknownIdentifierException, DestinationIsOffException {
    Terminal destination = this._network.getTerminal(destinationID);
    destination.getState().sendTextCommunication(destination, this, message);
    _associate.getState().update(_associate.getBalance(),_ongoingCommunication);
  }

  public boolean hasPositiveBalance() { return (_payments - _debt) > 0; }

  protected void unsubscribe(Client client) { _notifier.unsubscribe(client); }

  protected abstract boolean receiveVideo();

  /**
   * 3.5.9 -> send a interactive communication.
   * @param destinationID ID of the destination terminal.
   * @param type of the interactive communication (VIDEO, VOICE).
   * @throws UnknownIdentifierException given terminal does not exist.
   * @throws DestinationIsOffException destination terminal is turned off.
   * @throws DestinationIsBusyException destination terminal is busy.
   * @throws DestinationIsSilencedException destination terminal is silenced.
   * @throws UnsupportedAtOriginException this terminal doesn't support video.
   * @throws UnsupportedAtDestinationException destination terminal doesn't support video.
   */
  public abstract void sendInteractiveCommunication(String destinationID, String type) throws UnknownIdentifierException, DestinationIsOffException,
                                                                                     DestinationIsBusyException, DestinationIsSilencedException,
                                                                                     UnsupportedAtOriginException, UnsupportedAtDestinationException;

  /**
   * 3.5.10 -> ends current interactive communication.
   * @param duration of the communication.
   * @return cost of the communication.
   */
  public long endInteractiveCommunication(int duration) {
    long cost = _ongoingCommunication.endCommunication(duration);
    _ongoingCommunication.freeTerminals();
    _associate.getState().update(_associate.getBalance(),_ongoingCommunication);
    _associate.getState().update(_associate.getBalance(),_madeCommunications.values());
    _ongoingCommunication=null;
    return cost;
  }

  /**
   * 3.5.11 -> shows current interactive communication.
   * @return the current interactive communication with the requested format.
   */
  public String showOngoingCommunication() {
    return (_ongoingCommunication!=null) ? _ongoingCommunication.getReadyToDisplay() : null;
  }

  /**
   * Checks if this terminal can end the current interactive communication.
   * @return true if this terminal is busy (i.e., it has an active interactive communication) and
   *          it was the originator of this communication.
   **/
  public boolean canEndCurrentCommunication() {
    return _ongoingCommunication != null && _ongoingCommunication._isOngoing;
  }
  
  /**
   * Checks if this terminal can start a new communication.
   * @return true if this terminal is neither off neither busy, false otherwise.
   **/
  public boolean canStartCommunication() {
    return (!canEndCurrentCommunication() && (_state.isOn()) || _state.isOnSilent());
  }
}
