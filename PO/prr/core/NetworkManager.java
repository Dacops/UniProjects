package prr.core;


import java.io.*;

import prr.core.exception.ImportFileException;
import prr.core.exception.MissingFileAssociationException;
import prr.core.exception.UnavailableFileException;
import prr.core.exception.UnrecognizedEntryException;


public class NetworkManager {

  // Network Attributes.
  private Network _network = new Network();
  private String _filename;

  // Network Class Constructor.
  public Network getNetwork() {
    return _network;
  }
  
  /**
   * loads a file.
   * @param filename name of the file containing the serialized application's state to load.
   * @throws UnavailableFileException if the specified file does not exist or there is an error while processing this file.
   */
  public void load(String filename) throws UnavailableFileException, FileNotFoundException{
    try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(filename))) {
      _network = (Network)ois.readObject();
      _filename = (String)ois.readObject();
    }
    catch (IOException | ClassNotFoundException e) {
      throw new UnavailableFileException(filename);
    }
  }
  
  /**
   * Saves the serialized application's state into the file associated to the current network.
   * @throws FileNotFoundException if for some reason the file cannot be created or opened. 
   * @throws MissingFileAssociationException if the current network does not have a file.
   * @throws IOException if there is some error while serializing the state of the network to disk.
   */
  public void save() throws FileNotFoundException, MissingFileAssociationException, IOException {
    if(_filename == null)
      throw new MissingFileAssociationException();
    try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(_filename))) {
      oos.writeObject(_network);
      oos.writeObject(_filename);
    }
  }
  
  /**
   * Saves the serialized application's state into the specified file. The current network is associated to this file.
   * @param filename the name of the file.
   * @throws FileNotFoundException if for some reason the file cannot be created or opened.
   * @throws MissingFileAssociationException if the current network does not have a file.
   * @throws IOException if there is some error while serializing the state of the network to disk.
   */
  public void saveAs(String filename) throws FileNotFoundException, MissingFileAssociationException, IOException {
    _filename = filename;
    save();
  }
  
  /**
   * Read text input file and create domain entities.
   * @param filename name of the text input file
   * @throws ImportFileException if the file couldn't be imported.
   */
  public void importFile(String filename) throws ImportFileException {
    try {
      _network.importFile(filename);
    } catch (UnrecognizedEntryException | IOException e) {
      throw new ImportFileException(filename, e);
    }
  }

  /** @return true if object is saved, false otherwise. */
  public boolean hasAssociate() { return _filename != null; }
}
