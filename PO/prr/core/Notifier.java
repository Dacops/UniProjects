package prr.core;

import java.io.Serializable;
import java.util.HashSet;
import java.util.Set;

public abstract class Notifier implements Serializable {

    // Notifier attributes.
    Set<Client> _clientsToNotify;
    Terminal _sender;

    // Notifier Class Constructor.
    /** @param sender terminal that send the notification. */
    public Notifier(Terminal sender) {
        _clientsToNotify =  new HashSet<>();
        _sender = sender;
    }


    // Abstract functions implemented in NotifierSender class. */
    protected abstract void subscribe(Client client);
    protected abstract void unsubscribe(Client client);
    protected abstract  void notifyClients(String beforeState, String afterState);
}
