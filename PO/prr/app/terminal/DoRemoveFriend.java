package prr.app.terminal;

import prr.app.exception.UnknownTerminalKeyException;
import prr.core.Network;
import prr.core.Terminal;
import prr.core.exception.UnknownIdentifierException;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Add a friend.
 */
class DoRemoveFriend extends TerminalCommand {

  private Network _network;

  DoRemoveFriend(Network context, Terminal terminal) {
    super(Label.REMOVE_FRIEND, context, terminal);
    _network = context;
    addStringField("id", Message.terminalKey());
  }

  @Override
  protected final void execute() throws CommandException {
    try{
      _network.getTerminal(stringField("id"));
      _receiver.removeFriend(stringField("id"));
    } catch (UnknownIdentifierException e) {
      throw new UnknownTerminalKeyException(stringField("id"));
    }finally {
      _display.display();
    }
  }
}
