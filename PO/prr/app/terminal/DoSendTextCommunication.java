package prr.app.terminal;

import prr.core.Network;
import prr.core.Terminal;
import prr.app.exception.UnknownTerminalKeyException;
import pt.tecnico.uilib.menus.CommandException;
import prr.core.exception.*;

/**
 * Command for sending a text communication.
 */
class DoSendTextCommunication extends TerminalCommand {

  DoSendTextCommunication(Network context, Terminal terminal) {
    super(Label.SEND_TEXT_COMMUNICATION, context, terminal, receiver -> receiver.canStartCommunication());
    addStringField("id", Message.terminalKey());
    addStringField("message", Message.textMessage());
  }
  
  @Override
  protected final void execute() throws CommandException {
    try {
      _receiver.sendTextCommunication(stringField("id"), stringField("message"));

    } catch (UnknownIdentifierException exception) {
      throw new UnknownTerminalKeyException(stringField("id"));
    } catch (DestinationIsOffException exception) {
      _display.add(Message.destinationIsOff(stringField("id")));
    } finally {
      _display.display();
    }
  }
} 
