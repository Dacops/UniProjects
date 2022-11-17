package prr.app.client;

import prr.core.Network;
import prr.app.exception.UnknownClientKeyException;
import prr.core.exception.UnknownIdentifierException;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;

/**
 * Enable client notifications.
 */
class DoEnableClientNotifications extends Command<Network> {

  DoEnableClientNotifications(Network receiver) {
    super(Label.ENABLE_CLIENT_NOTIFICATIONS, receiver);
    addStringField("id", Message.key());
  }
  
  @Override
  protected final void execute() throws CommandException {
    try {
      if(_receiver.getClient(stringField("id")).isReceivingNotifications())
        _display.popup(Message.clientNotificationsAlreadyEnabled());
      else { _receiver.getClient(stringField("id")).toggleReceivingNotifications();}
    }catch(UnknownIdentifierException e) {
      throw new UnknownClientKeyException(stringField("id"));
    }
  }
}
