package prr.app.terminals;

import prr.core.Network;

/**
 * Menu for terminal operations.
 */
public class Menu extends pt.tecnico.uilib.menus.Menu {

    /** @param receiver Network that will display the Terminals Menu. */
  public Menu(Network receiver) {
    super(Label.TITLE, //
          new DoShowAllTerminals(receiver), //
          new DoRegisterTerminal(receiver), //
          new DoOpenMenuTerminalConsole(receiver)//
          );
  }
}
