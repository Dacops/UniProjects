package prr.app.client;

import prr.core.Client;
import prr.core.Network;
import prr.app.exception.UnknownClientKeyException;
import prr.core.exception.UnknownIdentifierException;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Show specific client: also show previous notifications.
 */
class DoShowClient extends Command<Network> {

  DoShowClient(Network receiver) {
    super(Label.SHOW_CLIENT, receiver);
    addStringField("id",Message.key());
  }

  @Override
  protected final void execute() throws CommandException {
    try {
      Client client = _receiver.getClient(stringField("id"));
      _display.add(client.getReadyToDisplay());
      client.getNotifications().forEach(n -> _display.addLine(n.toString()));
      client.clearNotifications(_receiver);
    }catch (UnknownIdentifierException e) {
      throw new UnknownClientKeyException(stringField("id"));
    }finally {
      _display.display();
    }
  }
}
