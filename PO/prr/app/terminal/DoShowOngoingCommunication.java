package prr.app.terminal;

import prr.core.Network;
import prr.core.Terminal;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Command for showing the ongoing communication.
 */
class DoShowOngoingCommunication extends TerminalCommand {

  DoShowOngoingCommunication(Network context, Terminal terminal) {
    super(Label.SHOW_ONGOING_COMMUNICATION, context, terminal);
  }
  
  @Override
  protected final void execute() throws CommandException {
    String ongoingCommunication = _receiver.showOngoingCommunication();
    _display.add( (ongoingCommunication!=null) ? ongoingCommunication : Message.noOngoingCommunication() );
    _display.display();
  }
}
