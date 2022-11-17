package prr.core;


import prr.core.exception.*;


public class Basic extends Terminal {

    /**
     * BasicTerminal class constructor.
     * @param idTerminal ID of the created terminal.
     * @param associate ID of the owner of the created terminal.
     * @param network network where the terminal belongs
     */
    public Basic(String idTerminal, Client associate, Network network) {
        super(idTerminal, associate, network);
    }

    /** @return false Basic terminal can't receive video. */
    @Override
    protected boolean receiveVideo() { return false; }

    /**
     * Send an Interactive Communication.
     * @param destinationID ID of the destination terminal.
     * @param type of the interactive communication (VIDEO, VOICE).
     * @throws UnknownIdentifierException destination terminal does not exist.
     * @throws DestinationIsOffException destination terminal is turned OFF.
     * @throws DestinationIsBusyException destination terminal is busy.
     * @throws DestinationIsSilencedException destination terminal is silenced.
     * @throws UnsupportedAtOriginException origin terminal can't support Video Communications.
     */
    @Override
    public void sendInteractiveCommunication(String destinationID, String type) throws UnknownIdentifierException, DestinationIsOffException,
            DestinationIsBusyException, DestinationIsSilencedException,
            UnsupportedAtOriginException {
        switch (type) {
            case "VIDEO" -> throw new UnsupportedAtOriginException();
            case "VOICE" -> {
                var destination = this._network.getTerminal(destinationID);
                boolean isFriend = _friends.contains(destinationID);
                destination.getState().checkDestination(this, destination);
                this.setOnBusy();
                destination.setOnBusy();
                _ongoingCommunication = new Voice(this, destination, isFriend);
            }
        }
    }

}