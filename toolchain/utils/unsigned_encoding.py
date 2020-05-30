import math

def width(value, bits_if_zero=1):
    if value == 0:
        return bits_if_zero
    elif value > 0:
        # value + 1 for starting at zero
        # log base 2 to convert to bits
        # ceil to round to smallest integer <- required bits
        return math.ceil(math.log(value + 1, 2))
    else : # value < 0
        raise ValueError("Can't encode a negtive value with unsigned encoding")

def encodeable(value, bits):
    if value >= 0:
        return bits >= width(value)
    else : # value < 0
        return False

def encode(value, bits):
    if encodeable(value, bits) == False:
        raise ValueError("Can't encode value %i with %i bits"%(value, bits))

    return bin(value)[2:].rjust(bits, "0")
