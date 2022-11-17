package prr.core;


public class NotificationSender extends Notifier {

    // NotificationSender class constructor.
    /** @param sender terminal that send the notification. */
    public NotificationSender(Terminal sender) { super(sender); }


    /**
     * adds a client to the Notifier list.
     * @param client to add.
     */
    @Override
    protected void subscribe(Client client) { _clientsToNotify.add(client); }

    @Override
    protected void unsubscribe(Client client) {
        _clientsToNotify.remove(client);
    }

    /**
     * notify all clients in the Notifier list.
     * @param beforeState previous terminal state.
     * @param afterState new terminal state.
     */
    @Override
    protected void notifyClients(String beforeState, String afterState) {
        for(Client c: _clientsToNotify) {
            c.receiveNotification(new Notification(beforeState, afterState, super._sender));
        }
    }

}
