package prr.app.client;

import prr.core.Network;
import prr.app.exception.UnknownClientKeyException;
import prr.core.exception.UnknownIdentifierException;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Disable client notifications.
 */
class DoDisableClientNotifications extends Command<Network> {

  DoDisableClientNotifications(Network receiver) {
    super(Label.DISABLE_CLIENT_NOTIFICATIONS, receiver);
    addStringField("id", Message.key());
  }
  
  @Override
  protected final void execute() throws CommandException {
    try {
      if(!_receiver.getClient(stringField("id")).isReceivingNotifications())
        _display.popup(Message.clientNotificationsAlreadyDisabled());
      else { _receiver.getClient(stringField("id")).toggleReceivingNotifications();}
    }catch(UnknownIdentifierException e) {
      throw new UnknownClientKeyException(stringField("id"));
    }
  }
}
