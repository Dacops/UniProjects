package prr.app.main;

import prr.core.Client;
import prr.core.Network;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Show global balance.
 */
class DoShowGlobalBalance extends Command<Network> {

  DoShowGlobalBalance(Network receiver) {
    super(Label.SHOW_GLOBAL_BALANCE, receiver);
  }
  
  @Override
  protected final void execute() throws CommandException {
    final long debts = Math.round(_receiver.getClients().stream().mapToDouble(Client::getDebts).sum());
    final long payments = Math.round(_receiver.getClients().stream().mapToDouble(Client::getPayments).sum());
    _display.popup(Message.globalPaymentsAndDebts(payments,debts));
  }
}
