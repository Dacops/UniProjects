package prr.app.terminal;

import prr.core.Network;
import prr.core.Terminal;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Command for ending communication.
 */
class DoEndInteractiveCommunication extends TerminalCommand {

  DoEndInteractiveCommunication(Network context, Terminal terminal) {
    super(Label.END_INTERACTIVE_COMMUNICATION, context, terminal, Terminal::canEndCurrentCommunication);
    addIntegerField("duration", Message.duration());
  }
  
  @Override
  protected final void execute() throws CommandException {
    _display.add(Message.communicationCost(_receiver.endInteractiveCommunication(integerField("duration"))));
    _display.display();
  }
}
