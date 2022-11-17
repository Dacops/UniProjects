package prr.core;


import prr.core.exception.*;


public class Fancy extends Terminal {

    /**
     * FancyTerminal class constructor.
     * @param idTerminal ID of the created terminal.
     * @param associate ID of the owner of the created terminal.
     * @param network network where the terminal belongs
     */
    public Fancy(String idTerminal, Client associate, Network network) {
        super(idTerminal, associate, network);
    }

    /** @return true, Fancy terminal can receive videos. */
    @Override
    protected boolean receiveVideo() { return true; }

    /**
     * Sends an interactive communication.
     * @param destinationID ID of the destination terminal.
     * @param type of the interactive communication (VIDEO, VOICE).
     * @throws UnknownIdentifierException destination terminal does not exist.
     * @throws DestinationIsOffException destination terminal is turned OFF.
     * @throws DestinationIsBusyException destination terminal is busy.
     * @throws DestinationIsSilencedException destination terminal is silenced.
     * @throws UnsupportedAtDestinationException destination terminal can't support Video Communications.
     */
    @Override
    public void sendInteractiveCommunication(String destinationID, String type) throws UnknownIdentifierException, DestinationIsOffException,
            DestinationIsBusyException, DestinationIsSilencedException,
            UnsupportedAtDestinationException {
        var destination = this._network.getTerminal(destinationID);
        boolean isFriend = _friends.contains(destinationID);

        destination.getState().checkDestination(this, destination);

        switch (type) {
            case "VIDEO" -> {
                if (!destination.receiveVideo()) throw new UnsupportedAtDestinationException();
                else {
                    _ongoingCommunication = new Video(this, destination, isFriend);
                }
            }
            case "VOICE" -> _ongoingCommunication = new Voice(this, destination, isFriend);
        }
        this.setOnBusy();
        destination.setOnBusy();
    }
}