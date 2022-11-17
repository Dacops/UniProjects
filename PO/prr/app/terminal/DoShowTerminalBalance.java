package prr.app.terminal;

import prr.core.Network;
import prr.core.Terminal;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Show balance.
 */
class DoShowTerminalBalance extends TerminalCommand {

  private String id;

  DoShowTerminalBalance(Network context, Terminal terminal) {
    super(Label.SHOW_BALANCE, context, terminal);
    id = terminal.getID();
  }
  
  @Override
  protected final void execute() throws CommandException {
    final long payments = _receiver.showPayments();
    final long debts = _receiver.showDebts();

    _display.add(Message.terminalPaymentsAndDebts(id, payments, debts));
    _display.display();
  }
}
