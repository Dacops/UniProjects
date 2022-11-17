package prr.app.main;

import prr.core.NetworkManager;
import prr.app.exception.FileOpenFailedException;
import pt.tecnico.uilib.menus.Command;
import pt.tecnico.uilib.menus.CommandException;
import prr.core.exception.UnavailableFileException;
import java.io.FileNotFoundException;

/**
 * Command to open a file.
 */
class DoOpenFile extends Command<NetworkManager> {

  DoOpenFile(NetworkManager receiver) {
    super(Label.OPEN_FILE, receiver);
    addStringField("filename",Message.openFile());

  }

  @Override
  protected final void execute() throws CommandException {
      try {
          _receiver.load(stringField("filename"));
      } catch (UnavailableFileException | FileNotFoundException e) {
        throw new FileOpenFailedException(e);
      }
  }
}
