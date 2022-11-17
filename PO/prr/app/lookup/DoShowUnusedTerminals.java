package prr.app.lookup;

import prr.core.Network;
import prr.core.Terminal;
import pt.tecnico.uilib.menus.Command;

/**
 * Show unused terminals (without communications).
 */
class DoShowUnusedTerminals extends Command<Network> {

  /** @param receiver Network from where terminals with no activity will be searched. */
  DoShowUnusedTerminals(Network receiver) {
    super(Label.SHOW_UNUSED_TERMINALS, receiver);
  }

  @Override
  protected final void execute() {
    _receiver.getTerminals().stream().filter(Terminal::notUsed).forEach(t -> _display.addLine(t.getReadyToDisplay()));
    _display.display();
  }
}
