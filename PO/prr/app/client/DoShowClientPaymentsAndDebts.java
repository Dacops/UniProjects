package prr.app.client;

import prr.core.Network;
import prr.app.exception.UnknownClientKeyException;
import prr.core.exception.UnknownIdentifierException;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Show the payments and debts of a client.
 */
class DoShowClientPaymentsAndDebts extends Command<Network> {

  DoShowClientPaymentsAndDebts(Network receiver) {
    super(Label.SHOW_CLIENT_BALANCE, receiver);
    addStringField("id", Message.key());
  }
  
  @Override
  protected final void execute() throws CommandException {
    try {
      _display.popup(Message.clientPaymentsAndDebts(stringField("id"),_receiver.getClient(stringField("id")).getPayments(),
              _receiver.getClient(stringField("id")).getDebts()));
    }catch (UnknownIdentifierException e) {
      throw new UnknownClientKeyException(stringField("id"));
    }
  }
}
