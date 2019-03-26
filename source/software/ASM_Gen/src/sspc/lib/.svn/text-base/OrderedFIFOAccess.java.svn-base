package sspc.lib;

public class OrderedFIFOAccess implements Comparable<OrderedFIFOAccess>{
	public OrderedFIFOAccess(int o, FIFO f) {
		ord = o;
		fifo = f;
	}
	
	
	public int ord;
	public FIFO fifo;
	
	@Override
	public int compareTo(OrderedFIFOAccess ordB) {
		return ord - ordB.ord;
	}
}
