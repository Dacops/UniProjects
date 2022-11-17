package prr.app.lookup;

import prr.core.Client;
import prr.core.Network;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;
import java.util.function.Predicate;

/**
 * Show clients with positive balance.
 */
class DoShowClientsWithoutDebts extends Command<Network> {

  DoShowClientsWithoutDebts(Network receiver) {
    super(Label.SHOW_CLIENTS_WITHOUT_DEBTS, receiver);
  }

  @Override
  protected final void execute() throws CommandException {
    _receiver.getClients().stream().filter(Predicate.not(Client::hasDebt)).forEach(c -> _display.addLine(c.getReadyToDisplay()));
    _display.display();
  }
}
