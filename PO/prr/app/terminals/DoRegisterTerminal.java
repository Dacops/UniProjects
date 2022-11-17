package prr.app.terminals;

import prr.app.exception.*;
import prr.core.Network;
import prr.core.exception.DuplicateTerminalException;
import prr.core.exception.InvalidTerminalException;
import prr.core.exception.UnknownIdentifierException;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Register terminal.
 */
class DoRegisterTerminal extends Command<Network> {

  DoRegisterTerminal(Network receiver) {
    super(Label.REGISTER_TERMINAL, receiver);
    addStringField("id",Message.terminalKey());
    addOptionField("type",Message.terminalType(),"BASIC","FANCY");
    addStringField("clientID",Message.clientKey());
  }


  @Override
  protected final void execute() throws CommandException {
    try {
      _receiver.registerTerminal(stringField("type"),stringField("id"),stringField("clientID"));
    } catch (InvalidTerminalException e) {
      throw new InvalidTerminalKeyException(stringField("id"));
    }catch (DuplicateTerminalException e) {
      throw new DuplicateTerminalKeyException(stringField("id"));
    } catch (UnknownIdentifierException e) {
      throw  new UnknownClientKeyException(stringField("clientID"));
    }
  }
}
