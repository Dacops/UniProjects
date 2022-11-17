package prr.app.lookup;


import prr.core.Client;
import prr.core.Network;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;

import java.util.Collection;


/**
 * Show clients with negative balance.
 */
class DoShowClientsWithDebts extends Command<Network> {

  DoShowClientsWithDebts(Network receiver) {
    super(Label.SHOW_CLIENTS_WITH_DEBTS, receiver);
  }

  @Override
  protected final void execute() throws CommandException {
    _receiver.getClientsWithDebt().forEach(c -> _display.addLine(c.getReadyToDisplay()));
    _display.display();
  }
}
