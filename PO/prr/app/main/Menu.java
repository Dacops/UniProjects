package prr.app.main;

import prr.core.NetworkManager;

/**
 * Main menu.
 */
public final class Menu extends pt.tecnico.uilib.menus.Menu {

    /** @param receiver NetworkManager that will display the Main Menu. */
    public Menu(NetworkManager receiver) {
    super(Label.TITLE, //
          new DoOpenFile(receiver),
          new DoSaveFile(receiver),
          new DoOpenMenuClient(receiver),
          new DoOpenMenuTerminal(receiver),
          new DoOpenMenuLookups(receiver),
          new DoShowGlobalBalance(receiver.getNetwork())//
          );
  }
}
