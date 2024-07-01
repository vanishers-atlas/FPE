# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

import random
import math

####################################################
# Input Data
####################################################

# Structure - test[depth]
def generate_1d_data(number_tests, data_lenght):
    assert type(number_tests) == int and number_tests > 0, "number_tests must be a positve int"
    assert type(data_lenght) == int and data_lenght > 0, "data_lenght must be a positve int"

    output = {}

    for t in range(number_tests):
        output[t] = {}

        input_value = random.randrange(2**data_lenght)
        for l in range(data_lenght):
            # bit i th bit of input value is 0
            if math.floor(input_value / 2**l) % 2 == 0:
                output[t][l] = 0
            else:
                output[t][l] = 1
    return output

def format_1d_data(number_tests, data_lenght, data, line_start="", encode_width=1):
    assert type(number_tests) == int and number_tests > 0, "number_tests must be a positve int"
    assert type(data_lenght) == int and data_lenght > 0, "data_lenght must be a positve int"

    assert type(line_start) == str, "line_start must be a string"
    assert type(encode_width) == int and encode_width > 0, "encode_width must be a positve int"

    output = line_start

    for s in range(number_tests):
        for l in range(data_lenght):
            output += "\"" + tc_utils.unsigned.encode(data[s][l], encode_width) + "\","
        output += "\n" + line_start

    output = output[:-(len(",\n") + len(line_start))]

    return output

# Structure - test[row[col[depth]]]
def generate_2d_data(number_tests, data_rows, data_cols, data_depth):
    assert type(number_tests) == int and number_tests > 0, "number_tests must be a positve int"
    assert type(data_rows) == int and data_rows > 0, "data_rows must be a positve int"
    assert type(data_cols) == int and data_cols > 0, "data_cols must be a positve int"
    assert type(data_depth) == int and data_depth > 0, "data_depth must be a positve int"

    output = {}

    for test in range(number_tests):
        output[test] = {}

        for row in range(data_rows):
            output[test][row] = {}
            for col in range(data_cols):
                output[test][row][col] = {}

                input_value = random.randrange(2**data_depth)
                for depth in range(data_depth):
                    # bit i th bit of input value is 0
                    if math.floor(input_value / 2**depth) % 2 == 0:
                        output[test][row][col][depth] = 0
                    else:
                        output[test][row][col][depth] = 1
    return output

def format_2d_data(number_tests, data_rows, data_cols, data_depth, data, line_start="", encode_width=1):
    assert type(number_tests) == int and number_tests > 0, "number_tests must be a positve int"
    assert type(data_rows) == int and data_rows > 0, "data_rows must be a positve int"
    assert type(data_cols) == int and data_cols > 0, "data_cols must be a positve int"
    assert type(data_depth) == int and data_depth > 0, "data_depth must be a positve int"

    assert type(line_start) == str, "line_start must be a string"
    assert type(encode_width) == int and encode_width > 0, "encode_width must be a positve int"

    output = line_start

    for t in range(number_tests):
        for r in range(data_rows):
            for c in range(data_cols):
                for d in range(data_depth):
                    output += "\"" + tc_utils.unsigned.encode(data[t][r][c][d], encode_width) + "\","
                output += "\t"
            output += "\n" + line_start
        output += "\n" + line_start

    output = output[:-(len(",\n\n") + 2*len(line_start) + 1)]


    return output

#######################################################")

####################################################
# Padding
####################################################

# Structure - test[row[col[depth]]]
def padding_ouput(number_tests, data_rows, data_cols, data_depth, data):
    assert type(number_tests) == int and number_tests > 0, "number_tests must be a positve int"
    assert type(data_rows) == int and data_rows > 0, "data_rows must be a positve int"
    assert type(data_cols) == int and data_cols > 0, "data_cols must be a positve int"
    assert type(data_depth) == int and data_depth > 0, "data_depth must be a positve int"

    assert len(data) == number_tests
    output = {}

    for test in range(number_tests):
        assert len(data[test]) == data_rows
        output[test] = {}

        # Handle first and last rows
        for row in [0, data_rows + 1]:
            output[test][row] = {}
            for col in range(data_cols + 2):
                output[test][row][col] = {}
                for depth in range(data_depth):
                    output[test][row][col][depth] = (row + col + depth + 1) % 2

        # Translate data rows
        for row in range(data_rows):
            assert len(data[test][row]) == data_cols
            output[test][row+1] = {}

            # Handle first and last col
            for col in [0, data_cols + 1]:
                output[test][row+1][col] = {}
                for depth in range(data_depth):
                    output[test][row+1][col][depth] = (row + col + depth) % 2

            # Translate data cols
            for cols in range(data_cols):
                assert len(data[test][row][cols]) == data_depth

                output[test][row+1][cols+1] = data[test][row][cols]

    return output

####################################################
# Convulationw
####################################################

# Structure - set[weights[x[y]]:threashold:gamma]
def generate_kernals(num_kernals, data_depth):
    assert type(num_kernals) == int and num_kernals > 0, "num_kernals must be a positve int"
    assert type(data_depth) == int and data_depth > 0, "data_depth must be a positve int"

    output = {}
    for kernal in range(num_kernals):
        output[kernal] = {}

        # compute weights
        output[kernal]["weights"] = {}
        for row in [-1, 0, 1]:
            output[kernal]["weights"][row] = {}
            for col in [-1, 0, 1]:
                output[kernal]["weights"][row][col] = {}

                weight_value = random.randrange(2**data_depth)
                for depth in range(data_depth):
                    # bit i th bit of input value is 0
                    if math.floor(weight_value / 2**depth) % 2 == 0:
                        output[kernal]["weights"][row][col][depth] = 0
                    else:
                        output[kernal]["weights"][row][col][depth] = 1

        # compute threashold
        output[kernal]["threashold"] = random.randrange(data_depth + 1)

        # Compute gamma sign
        output[kernal]["gamma"] = random.randrange(2)

    return output


# Structure -test[row[col[depth]]]
def conv_outputs(number_tests, data_rows, data_cols, data_depth, data, num_kernals, kernals):
    assert type(number_tests) == int and number_tests > 0, "number_tests must be a positve int"
    assert type(data_rows) == int and data_rows > 0, "data_rows must be a positve int"
    assert type(data_cols) == int and data_cols > 0, "data_cols must be a positve int"
    assert type(data_depth) == int and data_depth > 0, "data_depth must be a positve int"
    assert type(num_kernals) == int and num_kernals > 0, "num_kernals must be a positve int"

    output = {}

    padded_data = padding_ouput(number_tests, data_rows, data_cols, data_depth, data)
    for t in range(number_tests):
        output[t] = {}
        for r in range(data_rows):
            output[t][r] = {}
            for c in range(data_cols):
                output[t][r][c] = {}
                for k in range(num_kernals):
                    acc = 0
                    for x in [-1, 0, 1]:
                        for y in [-1, 0, 1]:
                            for d in range(data_depth):
                                if padded_data[t][r+x+1][c+y+1][d] == kernals[k]["weights"][x][y][d]:
                                    acc += 1

                    # Perfrom theashold
                    gamma_sign = "+" if kernals[k]["gamma"] == 1 else "-"
                    diff_sign =  "+" if acc > kernals[k]["threashold"] else "-"

                    if gamma_sign == diff_sign:
                        output[t][r][c][k] = 1
                    else:
                        output[t][r][c][k] = 0

    return output

####################################################
# Pooing
####################################################

# Structure - test[row[col[depth]]]
def pooling_outputs(number_tests, data_rows, data_cols, data_depth, data):
    assert type(number_tests) == int and number_tests > 0, "number_tests must be a positve int"
    assert type(data_rows) == int and data_rows > 0 and data_rows % 2 == 0, "data_rows must be a positve even int"
    assert type(data_cols) == int and data_cols > 0 and data_cols % 2 == 0, "data_cols must be a positve even int"
    assert type(data_depth) == int and data_depth > 0, "data_depth must be a positve int"

    output = {}

    for test in range(number_tests):
        output[test] = {}
        for row in range(int(data_rows/2)):
            output[test][row] = {}
            for col in range(int(data_cols/2)):
                output[test][row][col] = {}
                for d in range(data_depth):
                    output[test][row][col][d] = max(data[test][2*row][2*col][d], data[test][2*row][2*col+1][d], data[test][2*row+1][2*col][d], data[test][2*row+1][2*col+1][d])

    return output

####################################################
# Dense & Acc
####################################################

# Structure - set[weights[depth]:threashold:gamma]
def generate_parameters(number_sets, data_lenght):
    assert type(number_sets) == int and number_sets > 0, "number_sets must be a positve int"
    assert type(data_lenght) == int and data_lenght > 0, "data_lenght must be a positve int"

    output = {}

    for set in range(number_sets):
        output[set] = {}

        # compute weights
        output[set]["weights"] = {}
        rand_weight = random.randrange(2**data_lenght)
        for i in range(data_lenght):
            # bit i th bit of input value is 0
            if math.floor(rand_weight / 2**i) % 2 == 0:
                output[set]["weights"][i] = 0
            else:
                output[set]["weights"][i] = 1

        # compute threashold
        output[set]["threashold"] = random.randrange(data_lenght + 1)

        # Compute gamma sign
        output[set]["gamma"] = random.randrange(2)

    return output

def acc_outputs(number_tests, data_lenght, data, number_sets, parameters):
    assert type(number_tests) == int and number_tests > 0, "number_tests must be a positve int"
    assert type(data_lenght) == int and data_lenght > 0, "data_lenght must be a positve int"
    assert type(number_sets) == int and number_sets > 0, "number_sets must be a positve int"

    output = {}

    for t in range(number_tests):
        output[t] = {}
        for s in range(number_sets):
            acc = 0
            for l in range(data_lenght):
                if data[t][l] == parameters[s]["weights"][l]:
                    acc += 1
            output[t][s] = acc
    return output

def dense_outputs(number_tests, data_lenght, data, number_sets, parameters):
    assert type(number_tests) == int and number_tests > 0, "number_tests must be a positve int"
    assert type(data_lenght) == int and data_lenght > 0, "data_lenght must be a positve int"
    assert type(number_sets) == int and number_sets > 0, "number_sets must be a positve int"

    output = {}
    acc_data = acc_outputs(number_tests, data_lenght, data, number_sets, parameters)

    for t in range(number_tests):
        output[t] = {}
        for s in range(number_sets):
            # Perfrom theashold
            gamma_sign = "+" if parameters[s]["gamma"] == 1 else "-"
            diff_sign =  "+" if acc_data[t][s] > parameters[s]["threashold"] else "-"

            if gamma_sign == diff_sign:
                output[t][s] = 1
            else:
                output[t][s] = 0

    return output

# Testing
if __name__ == '__main__':
    print("##########################################################")
    print("Testing 1d layers: acc/dense")
    print("##########################################################")
    print()
    print("Generating 1d test data")
    number_tests, data_lenght = 8, 12
    input_data = generate_1d_data(number_tests, data_lenght)
    print(format_1d_data(number_tests, data_lenght, input_data, line_start="", encode_width=1))
    print()

    print("##########################################################")
    print("Testing acc/dence layer")
    print("##########################################################")

    print("Generating parameters")
    number_sets = 8
    parameters = generate_parameters(number_sets, data_lenght)
    for s in range(number_sets):
        print("threashold", parameters[s]["threashold"], "gamma", parameters[s]["gamma"], sep="\t",end="\t")
        print(format_1d_data(1, data_lenght, {0: parameters[s]["weights"]}, line_start="", encode_width=1))

    print("##########################################################")
    print()

    print("acc output")
    acc_data = acc_outputs(number_tests, data_lenght, input_data, number_sets, parameters)
    print(format_1d_data(number_tests, number_sets, acc_data, line_start="", encode_width=4))
    print()

    print("##########################################################")
    print()

    print("Dense output")
    dense_data = dense_outputs(number_tests, data_lenght, input_data, number_sets, parameters)
    print(format_1d_data(number_tests, number_sets, dense_data, line_start="", encode_width=1))
    print()



    number_tests, data_rows, data_cols, data_depth = 2, 4, 6, 3
    print("##########################################################")
    print("Testing 2d layers: padding, acc, polling")
    print("##########################################################")
    print()

    print("Generating 2d test data")
    input_data = generate_2d_data(number_tests, data_rows, data_cols, data_depth)
    print(format_2d_data(number_tests, data_rows, data_cols, data_depth, input_data, line_start="", encode_width=data_depth))
    print()

    print("##########################################################")
    print("Testing padding_ouput layer type")
    print("##########################################################")
    print()

    print("padding output")
    padded_data = padding_ouput(number_tests, data_rows, data_cols, data_depth, input_data)
    print(format_2d_data(number_tests, data_rows + 2, data_cols + 2, data_depth, padded_data, line_start="", encode_width=data_depth))
    print()

    print("##########################################################")
    print("Testing conv layer type")
    print("##########################################################")
    print()

    print("Generating kenrals")
    num_kernals = 6
    kernals = generate_kernals(num_kernals, data_depth)
    for k in sorted(kernals.keys()):
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                for d in sorted(kernals[k]["weights"][x][y].keys()):
                    print(kernals[k]["weights"][x][y][d],end="")
                print("\t",end="")
            if y == -1:
                print("threashold", kernals[k]["threashold"],end="",sep="\t")
            if y == 0:
                print("gamma", kernals[k]["gamma"],end="",sep="\t")
            print("\n",end="")
        print("\n",end="")

    print("##########################################################")
    print()

    print("Conv output")
    conv_data = conv_outputs(number_tests, data_rows, data_cols, data_depth, input_data, num_kernals, kernals)
    print(format_2d_data(number_tests, data_rows, data_cols, num_kernals, conv_data, line_start="", encode_width=num_kernals))
    print()

    print("##########################################################")
    print("Testing pooling layer type")
    print("##########################################################")
    print()

    print("pooling output")
    pooled_data = pooling_outputs(number_tests, data_rows, data_cols, data_depth, input_data)
    print(format_2d_data(number_tests, int(data_rows/2), int(data_cols/2), data_depth, padded_data, line_start="", encode_width=data_depth))
    print()
