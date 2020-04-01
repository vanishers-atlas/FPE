import math

def width(value, bias, tally_size):
    if value < 0:
        raise ValueError("Can't encode a negtive value with biased tally encoding")
    elif value < bias:
        raise ValueError("Can't encode value, %i, with bias of %i"%(value, bias))
    else:
        return math.ceil(value/(bias + tally_size))

def encodeable(value, bits):
    raise NotImplementedError()

def encode(value, bits):
    raise NotImplementedError()
