import math

def width(value, bits_if_zero=1):
    if value == 0:
        return bits_if_zero
    elif value > 0:
        # value + 1 for starting at zero
        # log base 2 to convert to bits
        # ceil to round to smallest integer <- required bits
        # + 1 for leading negtive power of 2's comp
        return math.ceil(math.log(value + 1, 2)) + 1
    else:  # value < 0:
        # abs to get positive value
        # log base 2 to convert to bits
        # ceil to round to smallest integer <= required bits
        # + 1 for leading negtive power
        return math.ceil(math.log(abs(value), 2)) + 1

def encodeable(value, bits):
    return bits >= width(value)

def encode(value, bits):
    if encodeable(value, bits) == False:
        raise ValueError("Can't encode value %i with %i bits"%(value, bits))

    if value >= 0:
        return bin(value)[2:].rjust(bits, "0")
    else:
        return bin(value)[3:].rjust(bits, "1")
