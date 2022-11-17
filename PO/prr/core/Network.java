package prr.core;


import java.io.Serializable;
import java.io.IOException;
import java.util.*;
import java.util.stream.Stream;

import prr.core.exception.*;

import static java.lang.Integer.parseInt;


public class Network implements Serializable {


  private static final long serialVersionUID = 202208091753L;


  // Network's Attributes
  private Map<String, Client> _clients;
  private Map<String, Terminal> _terminals;
  private Map<Integer, Communication> _communications;


  // Network's Constructor.
  public Network() {
    _clients = new TreeMap<>();
    _terminals = new TreeMap<>();
    _communications = new TreeMap<>();
  }


  // Returns.
  /** @return all the Clients. */
  public Collection<Client> getClients() { return Collections.unmodifiableCollection(_clients.values()); }

  /** @return all the Communications. */
  public Collection<Communication> getAllComms() { return Collections.unmodifiableCollection(_communications.values()); }

  /** @return all the Terminals. */
  public Collection<Terminal> getTerminals() { return Collections.unmodifiableCollection(_terminals.values()); }


  // More Complex Functions.
  /** @param c Communication to add to Communications array.*/
  protected void addCommunication(Communication c) {
    Integer integer = c.getID();
    _communications.put(integer, c);
  }

  /**
   * returns all terminals sorted
   * @param terminals a Collection with all Terminals.
   * @return a list with all terminals in the format terminalType|terminalId|ClientId|TerminalStatus|balance-paid|balance-debts
   *         or terminalType|terminalId|ClientId|TerminalStatus|balance-paid|balance-debts|friend1,...,friend sorted.
   */
  public Collection<String> getTerminalsDrawn(Collection<Terminal> terminals) {
    TreeMap<String, String> map = new TreeMap<>();

    for (Terminal t: terminals)
      map.put(t.getID(),t.getReadyToDisplay());

    return map.values();
  }

  /**
   * Read text input file and create corresponding domain entities.
   * @param filename name of the text input file
   * @throws UnrecognizedEntryException if some entry is not correct
   * @throws IOException if there is an IO exception while processing the text file
   */
  protected void importFile(String filename) throws UnrecognizedEntryException, IOException {
    Parser parser = new Parser(this);
    parser.parseFile(filename);
  }

  /**
   * gets client with given ID.
   * @param id id of the client to get.
   * @return the client with the given id.
   * @throws UnknownIdentifierException there's no client with the given id.
   */
  public Client getClient(String id) throws UnknownIdentifierException {
    if(_clients.get(id) == null)
      throw new UnknownIdentifierException(id);
    return _clients.get(id);
  }

  /**
   * gets terminal with given ID.
   * @param id id of the terminal to get.
   * @return the terminal with given id.
   * @throws UnknownIdentifierException there's no terminal with the given id.
   */
  public Terminal getTerminal(String id) throws UnknownIdentifierException {
    if(_terminals.get(id) == null)
      throw new UnknownIdentifierException(id);
    return _terminals.get(id);
  }

  public void unsubscribeTo(Terminal terminal ,Client client) { terminal.unsubscribe(client); }

  /**
   * Register Client with the info given as arguments by adding it to the HashMap of all the Clients of the app.
   * @param id Client's unique id.
   * @param name Client's name.
   * @param taxNumber Client's tax number.
   * @return Registered Client.
   * @throws DuplicateClientException there's already a client with given id.
   */
  public Client registerClient(String id, String name, int taxNumber) throws DuplicateClientException {
    String newID = id.toLowerCase();
    if(_clients.containsKey(newID))
      throw new DuplicateClientException();
    _clients.put(newID, new Client(id,name,taxNumber));
    return _clients.get(id);
  }

  public Stream<Client> getClientsWithDebt() { return getClients().stream().filter(Client::hasDebt).sorted(new DebtsComparator()); }

  /**
   * check if given ID is well formatted
   * @param id id to be checked
   * @throws InvalidTerminalException the given id wasn't well formatted.
   */
  protected void checkID(String id) throws InvalidTerminalException{
    if(id.length() == 6) {
      try {
        parseInt(id);
      }catch(NumberFormatException e) {
        throw new InvalidTerminalException();
      }
      return;
    }
    throw new InvalidTerminalException();
  }

  /**
   * Register Terminal with the info given as arguments by adding it to the HashMap of all the Terminals of the app.
   * @param type Terminal's type.
   * @param id  Terminal's id.
   * @param clientID Terminal's clientID.
   * @return Registered Terminal.
   * @throws DuplicateTerminalException already exists a terminal with given id.
   * @throws UnknownIdentifierException the clientID given wasn't well formatted.
   * @throws InvalidTerminalException the id given wasn't well formatted.
   */
  public Terminal registerTerminal(String type, String id, String clientID) throws DuplicateTerminalException, UnknownIdentifierException, InvalidTerminalException {
    checkID(id);
    if(_terminals.containsKey(id))
      throw new DuplicateTerminalException();
    Terminal created = null;
    Client associate = getClient(clientID);
    if(type.equals("BASIC"))
      created = new Basic(id, associate, this);
    else { created = new Fancy(id,associate, this); }
    _terminals.put(id, created);
    associate.addTerminal(created);
    return _terminals.get(id);
  }

  /**
   * Add given ID's terminal to given ID's friend's terminal.
   * @param terminal terminal where friend will be added.
   * @param friend  terminal friend to be added to given terminal.
   */
  public void addFriend(String terminal, String friend) {
    if(!terminal.equals(friend))
      _terminals.get(terminal).addFriend(friend);
  }
}
