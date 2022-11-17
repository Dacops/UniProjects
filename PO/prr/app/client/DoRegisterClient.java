package prr.app.client;

import prr.app.exception.DuplicateClientKeyException;
import prr.core.Network;
import prr.core.exception.DuplicateClientException;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Register new client.
 */
class DoRegisterClient extends Command<Network> {

  DoRegisterClient(Network receiver) {
    super(Label.REGISTER_CLIENT, receiver);
    addStringField("id",Message.key());
    addStringField("name",Message.name());
    addIntegerField("taxID",Message.taxId());
  }

  @Override
  protected final void execute() throws CommandException {
    try {
      _receiver.registerClient(stringField("id"), stringField("name"), integerField("taxID"));
    }catch(DuplicateClientException e) {
      throw new DuplicateClientKeyException(stringField("id"));
    }
  }
}
