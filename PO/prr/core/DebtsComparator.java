package prr.core;

import java.util.Comparator;
import java.util.Objects;

public class DebtsComparator implements Comparator<Client> {

    @Override
    public int compare(Client c1, Client c2) { return Long.compare(c2.getDebts(), c1.getDebts()); }
}
