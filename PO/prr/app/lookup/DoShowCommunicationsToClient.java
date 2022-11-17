package prr.app.lookup;

import prr.app.exception.UnknownClientKeyException;
import prr.core.Network;
import prr.core.exception.UnknownIdentifierException;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Show communications to a client.
 */
class DoShowCommunicationsToClient extends Command<Network> {

  DoShowCommunicationsToClient(Network receiver) {
    super(Label.SHOW_COMMUNICATIONS_TO_CLIENT, receiver);
    addStringField("id", Message.clientKey());
  }

  @Override
  protected final void execute() throws CommandException {
    try {
      _receiver.getClient(stringField("id")).getReceivedComms().forEach(c -> _display.addLine(c.getReadyToDisplay()));
      _display.display();
    } catch (UnknownIdentifierException e) {
      throw new UnknownClientKeyException(stringField("id"));
    }
  }
}
