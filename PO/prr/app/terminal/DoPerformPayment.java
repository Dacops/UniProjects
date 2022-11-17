package prr.app.terminal;

import prr.core.Network;
import prr.core.Terminal;
import prr.core.exception.InvalidCommunicationException;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Perform payment.
 */
class DoPerformPayment extends TerminalCommand {

  DoPerformPayment(Network context, Terminal terminal) {
    super(Label.PERFORM_PAYMENT, context, terminal);
    addIntegerField("id", Message.commKey());
  }
  
  @Override
  protected final void execute() throws CommandException {
    try {
      _receiver.payCommunication(integerField("id"));
    } catch (InvalidCommunicationException exception) {
      _display.add(Message.invalidCommunication());
    } finally {
      _display.display();
    }
  }
}
