package prr.app.terminal;

import prr.core.Network;
import prr.core.Terminal;
import prr.app.exception.UnknownTerminalKeyException;
import prr.core.exception.*;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Command for starting communication.
 */
class DoStartInteractiveCommunication extends TerminalCommand {

  private String _thisID; //get this ID for UnsupportedAtOriginException.

  DoStartInteractiveCommunication(Network context, Terminal terminal) {
    super(Label.START_INTERACTIVE_COMMUNICATION, context, terminal, receiver -> receiver.canStartCommunication());
    _thisID = terminal.getID();
    addStringField("id", Message.terminalKey());
    addOptionField("type", Message.commType(), "VIDEO", "VOICE");
  }
  
  @Override
  protected final void execute() throws CommandException {
    try {
      _receiver.sendInteractiveCommunication(stringField("id"), stringField("type"));

    } catch (UnknownIdentifierException exception) {
      throw new UnknownTerminalKeyException(stringField("id"));
    } catch (DestinationIsOffException exception) {
      _display.add(Message.destinationIsOff(stringField("id")));
    } catch (DestinationIsBusyException exception) {
      _display.add(Message.destinationIsBusy(stringField("id")));
    } catch (DestinationIsSilencedException exception) {
      _display.add(Message.destinationIsSilent(stringField("id")));
    } catch (UnsupportedAtOriginException exception) {
      _display.add(Message.unsupportedAtOrigin(_thisID, stringField("type")));
     } catch (UnsupportedAtDestinationException exception) {
      _display.add(Message.unsupportedAtDestination(stringField("id"), stringField("type")));
    } finally {
      _display.display();
    }
  }
}
