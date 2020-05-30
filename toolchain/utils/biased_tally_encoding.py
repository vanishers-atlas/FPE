import math
import builtins
from . import unsigned_encoding

def width(value, bias, range):
    if value < 0:
        raise ValueError("Can't encode a negtive value with biased tally encoding")
    elif value < bias:
        raise ValueError("Can't encode value, %i, with bias of %i"%(value, bias))
    else:
        return math.ceil(value/(bias + range))

def encodeable(value, tallies, bias, range):
    return tallies >= width(value, bias, range)

def encode(value, tallies, bias, range):
    if encodeable(value, tallies, bias, range) == False:
        raise ValueError("Can't encode value %i with %i tallies of %i to %i"%(value, tallies, bias, bias + range))

    bits_per_tally = unsigned_encoding.width(range)
    remaining = value - bias*tallies
    result = ""

    for _ in builtins .range(tallies):
        if remaining > range:
            result += bin(range)[2:].rjust(bits_per_tally, "0")
            remaining -= range
        else:
            result += bin(remaining)[2:].rjust(bits_per_tally, "0")
            remaining = 0

    return result
