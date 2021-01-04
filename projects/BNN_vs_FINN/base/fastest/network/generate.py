# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 6
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

import random
import math

from FPE.toolchain.tests import utils as test_utils

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils
from FPE.toolchain.HDL_generation import HDL_generator as generator

def generate_conv_files(layer_number, input_r, input_c, input_d, output_d):
    pop_width = tc_utils.unsigned.width(3 * 3 * input_d + 1)

    RAM_width = tc_utils.unsigned.width(3 * (input_c + 2) * input_d)
    RAM_depth = 2 ** RAM_width

    rom_kernal_span = 3 * 3 * input_d * output_d
    rom_thresholds_span = input_r * input_c * output_d

    # Generate program File
    with open("layer_%i_program.fpea"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\tDEF input_r  %i ;\n"%(input_r, ))
        f.write("\tDEF input_c  %i ;\n"%(input_c, ))
        f.write("\tDEF input_d  %i ;\n"%(input_d, ))
        f.write("\tDEF number_kernals %i ;\n"%(output_d, ))
        f.write("\n")
        f.write("\t// Define meaningfully names for Block access managers\n")
        f.write("\tDEF inputs_writes   0 ;\n")
        f.write("\tDEF inputs_read_r0  1 ;\n")
        f.write("\tDEF inputs_read_r1  2 ;\n")
        f.write("\tDEF inputs_read_r2  3 ;\n")
        f.write("\tDEF kenrals         4 ;\n")
        f.write("\tDEF threasholds     5 ;\n")
        f.write("\t\n")
        f.write("\t// Reset all BAMs\n")
        f.write("\tRESET BAM[inputs_writes];\n")
        f.write("\tRESET BAM[inputs_read_r0];\n")
        f.write("\tRESET BAM[inputs_read_r1];\n")
        f.write("\tRESET BAM[inputs_read_r2];\n")
        f.write("\tRESET BAM[threasholds];\n")
        f.write("\t\n")
        f.write("\t// Write packing for first row of input\n")
        f.write("\tZOL ((input_c + 2) * input_d)\n")
        f.write("\t{\n")
        f.write("\t\tMOV( 0, RAM[BAM[inputs_writes]<FORWARD>] ) ;\n")
        f.write("\t}\n")
        f.write("\t\n")
        f.write("\t// Read first line of data\n")
        f.write("\tZOL (input_d)\n")
        f.write("\t{\n")
        f.write("\t\tMOV( 0, RAM[BAM[inputs_writes]<FORWARD>] ) ;\n")
        f.write("\t}\n")
        f.write("\tZOL (input_c * input_d)\n")
        f.write("\t{\n")
        f.write("\t\tMOV( GET[0]<ADV>, RAM[BAM[inputs_writes]<FORWARD>] ) ;\n")
        f.write("\t}\n")
        f.write("\tZOL (input_d)\n")
        f.write("\t{\n")
        f.write("\t\tMOV( 0, RAM[BAM[inputs_writes]<FORWARD>] ) ;\n")
        f.write("\t}\n")
        f.write("\t\n")
        f.write("\t// Process body of sliding window\n")
        f.write("\tZOL (input_r - 1)\n")
        f.write("\t{\n")
        f.write("\t\t// Read next line of data\n")
        f.write("\t\tZOL (input_d)\n")
        f.write("\t\t{\n")
        f.write("\t\t\tMOV( 0, RAM[BAM[inputs_writes]<FORWARD>] ) ;\n")
        f.write("\t\t}\n")
        f.write("\t\tZOL (input_c * input_d)\n")
        f.write("\t\t{\n")
        f.write("\t\t\tMOV( GET[0]<ADV>, RAM[BAM[inputs_writes]<FORWARD>] ) ;\n")
        f.write("\t\t}\n")
        f.write("\t\tZOL (input_d)\n")
        f.write("\t\t{\n")
        f.write("\t\t\tMOV( 0, RAM[BAM[inputs_writes]<FORWARD>] ) ;\n")
        f.write("\t\t}\n")
        f.write("\t\t\n")
        f.write("\t\t// Handle each col of sliding window\n")
        f.write("\t\tZOL (input_c)\n")
        f.write("\t\t{\n")
        f.write("\t\t\t// Reset kenral BAM to start at first kernal\n")
        f.write("\t\t\tRESET BAM[kenrals];\n")
        f.write("\t\t\tNOP;\n")
        f.write("\t\t\tNOP;\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Process each kernal\n")
        f.write("\t\t\tZOL (number_kernals)\n")
        f.write("\t\t\t{\n")
        f.write("\t\t\t\t// Handle kernal row 0\n")
        f.write("\t\t\t\tXOR ( RAM[BAM[inputs_read_r0]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], REG[0] ) ; // Overwrite popcountA\n")
        f.write("\t\t\t\tXOR ( RAM[BAM[inputs_read_r0]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], REG[1] ) ; // Overwrite popcountA\n")
        f.write("\t\t\t\tZOL ((3 * input_d - 2) / 2)\n")
        f.write("\t\t\t\t{\n")
        f.write("\t\t\t\t\tXOR ( RAM[BAM[inputs_read_r0]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\t\tADD ( REG[0], ACC, REG[0]) ;\n")
        f.write("\t\t\t\t\tXOR ( RAM[BAM[inputs_read_r0]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\t\tADD ( REG[1], ACC, REG[1]) ;\n")
        f.write("\t\t\t\t}\n")
        f.write("\t\t\t\t\n")
        f.write("\t\t\t\t// Push row's BAM back to cols worth\n")
        f.write("\t\t\t\tSEEK BAM[inputs_read_r0] (3*input_d)<BACKWARD>;\n")
        f.write("\t\t\t\t\n")
        f.write("\t\t\t\t// Handle kernal row 1\n")
        f.write("\t\t\t\tZOL (3 * input_d / 2)\n")
        f.write("\t\t\t\t{\n")
        f.write("\t\t\t\t\tXOR ( RAM[BAM[inputs_read_r1]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\t\tADD ( REG[0], ACC, REG[0]) ;\n")
        f.write("\t\t\t\t\tXOR ( RAM[BAM[inputs_read_r1]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\t\tADD ( REG[1], ACC, REG[1]) ;\n")
        f.write("\t\t\t\t}\n")
        f.write("\t\t\t\t\n")
        f.write("\t\t\t\t// Push row's BAM back to cols worth\n")
        f.write("\t\t\t\tSEEK BAM[inputs_read_r1] (3*input_d)<BACKWARD>;\n")
        f.write("\t\t\t\t\n")
        f.write("\t\t\t\t// Handle kernal row 2\n")
        f.write("\t\t\t\tZOL (3 * input_d / 2)\n")
        f.write("\t\t\t\t{\n")
        f.write("\t\t\t\t\tXOR ( RAM[BAM[inputs_read_r2]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\t\tADD ( REG[0], ACC, REG[0]) ;\n")
        f.write("\t\t\t\t\tXOR ( RAM[BAM[inputs_read_r2]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\t\tADD ( REG[1], ACC, REG[1]) ;\n")
        f.write("\t\t\t\t}\n")
        f.write("\t\t\t\t\n")
        f.write("\t\t\t\t// Push row's BAM back to cols worth\n")
        f.write("\t\t\t\tSEEK BAM[inputs_read_r2] (3*input_d)<BACKWARD>;\n")
        f.write("\t\t\t\t\n")
        f.write("\t\t\t\t// Add popcountA and popcountB to get full popcount\n")
        f.write("\t\t\t\t// At this point popcountB (REG[1]) isn't fetchable, but is still in ACC\n")
        f.write("\t\t\t\tADD ( REG[0], ACC, ACC) ;\n")
        f.write("\t\t\t\t\n")
        f.write("\t\t\t\t// output the most significent bit of the difference between the popcount and the threashold\n")
        f.write("\t\t\t\t// Evalation to a sign function on the difference\n")
        f.write("\t\t\t\tSUB(ROM[BAM[threasholds]<FORWARD>], ACC, ACC);\n")
        f.write("\t\t\t\tRSH(ACC, %i, PUT[0]); // Shift by lg(3 * 3 * input_d + 1) - 1 bits to get the MSB\n"%(pop_width, ) )
        f.write("\t\t\t\t}\n")
        f.write("\t\t\t\t\n")
        f.write("\t\t\t\t// Advance input bams to next col\n")
        f.write("\t\t\t\tSEEK BAM[inputs_read_r0] (input_d) <FORWARD> ;\n")
        f.write("\t\t\t\tSEEK BAM[inputs_read_r1] (input_d) <FORWARD> ;\n")
        f.write("\t\t\t\tSEEK BAM[inputs_read_r2] (input_d) <FORWARD> ;\n")
        f.write("\t\t\t}\n")
        f.write("\t\t// Advance input bams to nect row\n")
        f.write("\t\tSEEK BAM[inputs_read_r0] (2*input_d) <FORWARD> ;\n")
        f.write("\t\tSEEK BAM[inputs_read_r1] (2*input_d) <FORWARD> ;\n")
        f.write("\t\tSEEK BAM[inputs_read_r2] (2*input_d) <FORWARD> ;\n")
        f.write("\t}\n")
        f.write("\tNOP;\n")
        f.write("\t\n")
        f.write("\t// Process last of sliding window\n")
        f.write("\t// Write packing for first row of input\n")
        f.write("\tZOL ((input_c + 2) * input_d)\n")
        f.write("\t{\n")
        f.write("\t\tMOV( 0, RAM[BAM[inputs_writes]<FORWARD>] ) ;\n")
        f.write("\t}\n")
        f.write("\t\n")
        f.write("\t// Handle each col of sliding window\n")
        f.write("\tZOL (input_c)\n")
        f.write("\t{\n")
        f.write("\t\t// Reset kenral BAM to start at first kernal\n")
        f.write("\t\tRESET BAM[kenrals];\n")
        f.write("\t\tNOP;\n")
        f.write("\t\tNOP;\n")
        f.write("\t\t\n")
        f.write("\t\t// Process each kernal\n")
        f.write("\t\tZOL (number_kernals)\n")
        f.write("\t\t{\n")
        f.write("\t\t\t// Handle kernal row 0\n")
        f.write("\t\t\tXOR ( RAM[BAM[inputs_read_r0]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], REG[0] ) ; // Overwrite popcountA\n")
        f.write("\t\t\tXOR ( RAM[BAM[inputs_read_r0]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], REG[1] ) ; // Overwrite popcountA\n")
        f.write("\t\t\tZOL ((3 * input_d - 2) / 2)\n")
        f.write("\t\t\t{\n")
        f.write("\t\t\t\tXOR ( RAM[BAM[inputs_read_r0]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\tADD ( REG[0], ACC, REG[0]) ;\n")
        f.write("\t\t\t\tXOR ( RAM[BAM[inputs_read_r0]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\tADD ( REG[1], ACC, REG[1]) ;\n")
        f.write("\t\t\t}\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Push row's BAM back to cols worth\n")
        f.write("\t\t\tSEEK BAM[inputs_read_r0] (3*input_d)<BACKWARD>;\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Handle kernal row 1\n")
        f.write("\t\t\tZOL (3 * input_d / 2)\n")
        f.write("\t\t\t{\n")
        f.write("\t\t\t\tXOR ( RAM[BAM[inputs_read_r1]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\tADD ( REG[0], ACC, REG[0]) ;\n")
        f.write("\t\t\t\tXOR ( RAM[BAM[inputs_read_r1]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\tADD ( REG[1], ACC, REG[1]) ;\n")
        f.write("\t\t\t}\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Push row's BAM back to cols worth\n")
        f.write("\t\t\tSEEK BAM[inputs_read_r1] (3*input_d)<BACKWARD>;\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Handle kernal row 2\n")
        f.write("\t\t\tZOL (3 * input_d / 2)\n")
        f.write("\t\t\t{\n")
        f.write("\t\t\t\tXOR ( RAM[BAM[inputs_read_r2]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\tADD ( REG[0], ACC, REG[0]) ;\n")
        f.write("\t\t\t\tXOR ( RAM[BAM[inputs_read_r2]<FORWARD>], ROM[BAM[kenrals]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\t\tADD ( REG[1], ACC, REG[1]) ;\n")
        f.write("\t\t\t}\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Push row's BAM back to cols worth\n")
        f.write("\t\t\tSEEK BAM[inputs_read_r2] (3*input_d)<BACKWARD>;\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Add popcountA and popcountB to get full popcount\n")
        f.write("\t\t\t// At this point popcountB (REG[1]) isn't fetchable, but is still in ACC\n")
        f.write("\t\t\tADD ( REG[0], ACC, ACC) ;\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// output the most significent bit of the difference between the popcount and the threashold\n")
        f.write("\t\t\t// Evalation to a sign function on the difference\n")
        f.write("\t\t\tSUB(ROM[BAM[threasholds]<FORWARD>], ACC, ACC);\n")
        f.write("\t\t\tRSH(ACC, %i, PUT[0]); // Shift by lg(3 * 3 * input_d + 1) - 1 bits to get the MSB\n"%(pop_width, ) )
        f.write("\t\t}\n")
        f.write("\t\t\n")
        f.write("\t\t// Advance input bams to nect col\n")
        f.write("\t\tSEEK BAM[inputs_read_r0] (input_d) <FORWARD> ;\n")
        f.write("\t\tSEEK BAM[inputs_read_r1] (input_d) <FORWARD> ;\n")
        f.write("\t\tSEEK BAM[inputs_read_r2] (input_d) <FORWARD> ;\n")
        f.write("\t}\n")
        f.write("\tNOP;\n")
        f.write("}\n")

    # Generate rom File
    with open("layer_%i_ROM.mem"%(layer_number, ), "w") as f:
        for _ in range(output_d*3*3*input_d):
            f.write(tc_utils.unsigned.encode(random.randrange(2), pop_width))
            f.write("\n")

        for _ in range(input_r*input_c*output_d):
            f.write(tc_utils.unsigned.encode(random.randrange(3*3*input_d + 1), pop_width))
            f.write("\n")

    # Generate parameter File
    with open("layer_%i_parameters.json"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t\"SIMD\": {\n")
        f.write("\t\t\"lanes\": 1\n")
        f.write("\t},\n")

        f.write("\t\"address_sources\": {\n")
        f.write("\t\t\"BAM_0\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_1\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": %i\n"%(3 * input_d, ) )
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_2\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": %i\n"%(3 * input_d, ) )
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_3\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": %i\n"%(3 * input_d, ) )
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_4\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(rom_kernal_span - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(rom_kernal_span - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_5\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(rom_kernal_span + rom_thresholds_span - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(rom_thresholds_span - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n")
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"data_memories\": {\n")
        f.write("\t\t\"GET\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"IMM\": {},\n")
        f.write("\t\t\"PUT\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"RAM\": {\n")
        f.write("\t\t\t\"data_width\": 1,\n")
        f.write("\t\t\t\"depth\": %i\n"%(RAM_depth, ))
        f.write("\t\t},\n")
        f.write("\t\t\"REG\": {\n")
        f.write("\t\t\t\"data_width\": %i,\n"%(pop_width, ))
        f.write("\t\t\t\"depth\": 2\n")
        f.write("\t\t},\n")
        f.write("\t\t\"ROM\": {\n")
        f.write("\t\t\t\"data_width\": %i,\n"%(pop_width, ))
        f.write("\t\t\t\"depth\": %i\n"%(rom_kernal_span + rom_thresholds_span ))
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"execute_units\": {\n")
        f.write("\t\t\"ALU\": {\n")
        f.write("\t\t\t\"data_width\": %i\n"%(pop_width + 1, ))
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"instr_decoder\": {},\n")
        f.write("\t\"program_flow\": {}\n")
        f.write("}\n")

    # Generate generics File
    with open("layer_%i_generics.json"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t\"BAM_0_base\": 0,\n")
        f.write("\t\"BAM_0_increment\": 1,\n")
        f.write("\t\"BAM_1_base\": %i,\n"%(0*(input_c + 2)*input_d), )
        f.write("\t\"BAM_1_increment\": 1,\n")
        f.write("\t\"BAM_2_base\": %i,\n"%(1*(input_c + 2)*input_d), )
        f.write("\t\"BAM_2_increment\": 1,\n")
        f.write("\t\"BAM_3_base\": %i,\n"%(2*(input_c + 2)*input_d), )
        f.write("\t\"BAM_3_increment\": 1,\n")
        f.write("\t\"BAM_4_base\": 0,\n")
        f.write("\t\"BAM_4_increment\": 1,\n")
        f.write("\t\"BAM_5_base\": %i,\n"%(3*3*input_d*output_d))
        f.write("\t\"BAM_5_increment\": 1,\n")
        f.write("\t\"ROM_mem_file\": \"..\\\\layer_%i_ROM.mem\"\n"%(layer_number, ))
        f.write("}\n")

def generate_pool_files(layer_number, input_r, input_c, input_d):
    RAM_depth = input_c * input_d / 2

    # Generate program File
    with open("layer_%i_program.fpea"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\tDEF input_r  %i ;\n"%(input_r, ))
        f.write("\tDEF input_c  %i ;\n"%(input_c, ))
        f.write("\tDEF input_d  %i ;\n"%(input_d, ))
        f.write("\t\n")
        f.write("\t// Define meaningfully names for Block access managers\n")
        f.write("\tDEF results_read  0 ;\n")
        f.write("\tDEF results_write 1 ;\n")
        f.write("\t\n")
        f.write("\tRESET BAM[results_write];\n")
        f.write("\tRESET BAM[results_read];\n")
        f.write("\tNOP;\n")
        f.write("\t\n")
        f.write("\t// Handle each row of kernals\n")
        f.write("\tZOL (input_r / 2)\n")
        f.write("\t{\n")
        f.write("\t\t// Handle upper elements of each kernals in row\n")
        f.write("\t\tZOL (input_c / 2)\n")
        f.write("\t\t{\n")
        f.write("\t\t\t// Handle first upper elements\n")
        f.write("\t\t\tZOL (input_d)\n")
        f.write("\t\t\t{\n")
        f.write("\t\t\t\tMOV (GET[0]<ADV>, RAM[BAM[results_write]<FORWARD>]);\n")
        f.write("\t\t\t}\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Push write back for second upper elements\n")
        f.write("\t\t\tSEEK BAM[results_write](input_d)<BACKWARD>;\n")
        f.write("\t\t\tNOP;\n")
        f.write("\t\t\tNOP;\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Handle second upper elements\n")
        f.write("\t\t\tZOL (input_d)\n")
        f.write("\t\t\t{\n")
        f.write("\t\t\t\tOR (GET[0]<ADV>, RAM[BAM[results_read]<FORWARD>], RAM[BAM[results_write]<FORWARD>]);\n")
        f.write("\t\t\t}\n")
        f.write("\t\t\tNOP;\n")
        f.write("\t\t}\n")
        f.write("\t\tNOP;\n")
        f.write("\t\t\n")
        f.write("\t\t// Handle lower elements of each kernals in row\n")
        f.write("\t\tZOL (input_c / 2)\n")
        f.write("\t\t{\n")
        f.write("\t\t\t// Handle first lower elements\n")
        f.write("\t\t\tZOL (input_d)\n")
        f.write("\t\t\t{\n")
        f.write("\t\t\t\tOR (GET[0]<ADV>, RAM[BAM[results_read]<FORWARD>], RAM[BAM[results_write]<FORWARD>]);\n")
        f.write("\t\t\t}\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Push write back for second lower elements\n")
        f.write("\t\t\tSEEK BAM[results_read](input_d)<BACKWARD>;\n")
        f.write("\t\t\tNOP;\n")
        f.write("\t\t\tNOP;\n")
        f.write("\t\t\t\n")
        f.write("\t\t\t// Handle second lower elements\n")
        f.write("\t\t\tZOL (input_d)\n")
        f.write("\t\t\t{\n")
        f.write("\t\t\t\tOR (GET[0]<ADV>, RAM[BAM[results_read]<FORWARD>], PUT[0]);\n")
        f.write("\t\t\t}\n")
        f.write("\t\t\tNOP;\n")
        f.write("\t\t}\n")
        f.write("\t\tNOP;\n")
        f.write("\t}\n")
        f.write("\tNOP;\n")
        f.write("}\n")

    # Generate parameter File
    with open("layer_%i_parameters.json"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t\"SIMD\": {\n")
        f.write("\t\t\"lanes\": 1\n")
        f.write("\t},\n")

        f.write("\t\"address_sources\": {\n")
        f.write("\t\t\"BAM_0\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": %i\n"%(input_d, ) )
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_1\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": %i\n"%(input_d, ) )
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"data_memories\": {\n")
        f.write("\t\t\"GET\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"PUT\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"RAM\": {\n")
        f.write("\t\t\t\"data_width\": 1,\n")
        f.write("\t\t\t\"depth\": %i\n"%(RAM_depth, ))
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"execute_units\": {\n")
        f.write("\t\t\"ALU\": {\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"instr_decoder\": {},\n")
        f.write("\t\"program_flow\": {}\n")
        f.write("}\n")

    # Generate generics File
    with open("layer_%i_generics.json"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t\"BAM_0_base\": 0,\n")
        f.write("\t\"BAM_0_increment\": 1,\n")
        f.write("\t\"BAM_1_base\": 0,\n")
        f.write("\t\"BAM_1_increment\": 1\n")
        f.write("}\n")

def generate_dense_files(layer_number, input_lenght, output_lenght):
    pop_width = tc_utils.unsigned.width(input_lenght + 1)

    ROM_depth = (input_lenght + 1) * output_lenght

    # Generate program File
    with open("layer_%i_program.fpea"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t//*\n")
        f.write("\t\tThis constants are free to change to match the target layer.\n")
        f.write("\t\tCurrently no speacal cases have been found\n")
        f.write("\t*//\n")
        f.write("\tDEF input_neurons  %i ;\n"%(input_lenght, ))
        f.write("\tDEF output_neurons %i ;\n"%(output_lenght, ))
        f.write("\t\n")
        f.write("\t// Common constants deviced from other constants\n")
        f.write("\t\n")
        f.write("\t// Define meaningfully names for Block access managers\n")
        f.write("\tDEF inputs       0 ;\n")
        f.write("\tDEF parameters   1 ;\n")
        f.write("\t\n")
        f.write("\tRESET BAM[inputs] ;\n")
        f.write("\tRESET BAM[parameters] ;\n")
        f.write("\t NOP ;\n")
        f.write("\t\n")
        f.write("\t// Read input data to RAM\n")
        f.write("\tZOL (input_neurons)\n")
        f.write("\t{\n")
        f.write("\t\tMOV( GET[0]<ADV>, RAM[BAM[inputs]<FORWARD>] ) ;\n")
        f.write("\t}\n")
        f.write("\t\n")
        f.write("\t// Process each neuron in turn\n")
        f.write("\tZOL (output_neurons)\n")
        f.write("\t{\n")
        f.write("\t\t// BAM[inputs] will have wrapped around to 0 at this point\n")
        f.write("\t\t// therefore no need to reset\n")
        f.write("\t\t\n")
        f.write("\t\t// Preform XOR and popcount weight\n")
        f.write("\t\tXOR ( RAM[BAM[inputs]<FORWARD>], ROM[BAM[parameters]<FORWARD>], REG[0] ) ; // Overwrite popcountA\n")
        f.write("\t\tXOR ( RAM[BAM[inputs]<FORWARD>], ROM[BAM[parameters]<FORWARD>], REG[1] ) ; // Overwrite popcountB\n")
        f.write("\t\tZOL ((input_neurons - 2)/2)\n")
        f.write("\t\t{\n")
        f.write("\t\t\tXOR ( RAM[BAM[inputs]<FORWARD>], ROM[BAM[parameters]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\tADD ( REG[0], ACC, REG[0]) ;\n")
        f.write("\t\t\tXOR ( RAM[BAM[inputs]<FORWARD>], ROM[BAM[parameters]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\tADD ( REG[1], ACC, REG[1]) ;\n")
        f.write("\t\t}\n")
        f.write("\t\t\n")
        f.write("\t\t// Add popcountA and popcountB to get full popcount\n")
        f.write("\t\t// At this point popcountB (REG[1]) isn't fetchable, but is still in ACC\n")
        f.write("\t\tADD ( REG[0], ACC, ACC) ;\n")
        f.write("\t\t\n")
        f.write("\t\t// output the most significent bit of the difference between the popcount and the threashold\n")
        f.write("\t\t// Evalation to a sign function on the difference\n")
        f.write("\t\tSUB(ROM[BAM[parameters]<FORWARD>], ACC, ACC); // Threadhold - popcount so 0 MSB - negative value\n")
        f.write("\t\tRSH(ACC, %i, PUT[0]); // Shift by lg(3 * 3 * input_d + 1) - 1 bits to get the MSB\n"%(pop_width, ) )
        f.write("\t}\n")
        f.write("\tNOP ;\n")
        f.write("}\n")

    # Generate rom File
    with open("layer_%i_ROM.mem"%(layer_number, ), "w") as f:
        for _ in range(output_lenght):
            for _ in range(input_lenght):
                f.write(tc_utils.unsigned.encode(random.randrange(2), pop_width))
                f.write("\n")

            f.write(tc_utils.unsigned.encode(random.randrange(input_lenght + 1), pop_width))
            f.write("\n")

    # Generate parameter File
    with open("layer_%i_parameters.json"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t\"SIMD\": {\n")
        f.write("\t\t\"lanes\": 1\n")
        f.write("\t},\n")

        f.write("\t\"address_sources\": {\n")
        f.write("\t\t\"BAM_0\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(input_lenght - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(input_lenght - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_1\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(ROM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(ROM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n" )
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"data_memories\": {\n")
        f.write("\t\t\"GET\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"PUT\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"RAM\": {\n")
        f.write("\t\t\t\"data_width\": 1,\n")
        f.write("\t\t\t\"depth\": %i\n"%(input_lenght, ))
        f.write("\t\t},\n")
        f.write("\t\t\"REG\": {\n")
        f.write("\t\t\t\"data_width\": %i,\n"%(pop_width, ))
        f.write("\t\t\t\"depth\": 2\n")
        f.write("\t\t},\n")
        f.write("\t\t\"ROM\": {\n")
        f.write("\t\t\t\"data_width\": %i,\n"%(pop_width, ))
        f.write("\t\t\t\"depth\": %i\n"%(ROM_depth, ))
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"execute_units\": {\n")
        f.write("\t\t\"ALU\": {\n")
        f.write("\t\t\t\"data_width\": %i\n"%(pop_width + 1, ))
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"instr_decoder\": {},\n")
        f.write("\t\"program_flow\": {}\n")
        f.write("}\n")

    # Generate generics File
    with open("layer_%i_generics.json"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t\"BAM_0_base\": 0,\n")
        f.write("\t\"BAM_0_increment\": 1,\n")
        f.write("\t\"BAM_1_base\": 0,\n")
        f.write("\t\"BAM_1_increment\": 1,\n")
        f.write("\t\"ROM_mem_file\": \"..\\\\layer_%i_ROM.mem\"\n"%(layer_number, ))
        f.write("}\n")

def generate_last_files(layer_number, input_lenght, output_lenght):
    pop_width = tc_utils.unsigned.width(input_lenght + 1)
    ROM_depth = (input_lenght + 1) * output_lenght

    # Generate program File
    with open("layer_%i_program.fpea"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t//*\n")
        f.write("\t\tThis constants are free to change to match the target layer.\n")
        f.write("\t\tCurrently no speacal cases have been found\n")
        f.write("\t*//\n")
        f.write("\tDEF input_neurons  %i ;\n"%(input_lenght, ))
        f.write("\tDEF output_neurons %i ;\n"%(output_lenght, ))
        f.write("\t\n")
        f.write("\t// Common constants deviced from other constants\n")
        f.write("\t\n")
        f.write("\t// Define meaningfully names for Block access managers\n")
        f.write("\tDEF inputs       0 ;\n")
        f.write("\tDEF parameters   1 ;\n")
        f.write("\t\n")
        f.write("\tRESET BAM[inputs] ;\n")
        f.write("\tRESET BAM[parameters] ;\n")
        f.write("\t NOP ;\n")
        f.write("\t\n")
        f.write("\t// Read input data to RAM\n")
        f.write("\tZOL (input_neurons)\n")
        f.write("\t{\n")
        f.write("\t\tMOV( GET[0]<ADV>, RAM[BAM[inputs]<FORWARD>] ) ;\n")
        f.write("\t}\n")
        f.write("\t\n")
        f.write("\t// Process each neuron in turn\n")
        f.write("\tZOL (output_neurons)\n")
        f.write("\t{\n")
        f.write("\t\t// BAM[inputs] will have wrapped around to 0 at this point\n")
        f.write("\t\t// therefore no need to reset\n")
        f.write("\t\t\n")
        f.write("\t\t// Preform XOR and popcount weight\n")
        f.write("\t\tXOR ( RAM[BAM[inputs]<FORWARD>], ROM[BAM[parameters]<FORWARD>], REG[0] ) ; // Overwrite popcountA\n")
        f.write("\t\tXOR ( RAM[BAM[inputs]<FORWARD>], ROM[BAM[parameters]<FORWARD>], REG[1] ) ; // Overwrite popcountB\n")
        f.write("\t\tZOL ((input_neurons - 2)/2)\n")
        f.write("\t\t{\n")
        f.write("\t\t\tXOR ( RAM[BAM[inputs]<FORWARD>], ROM[BAM[parameters]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\tADD ( REG[0], ACC, REG[0]) ;\n")
        f.write("\t\t\tXOR ( RAM[BAM[inputs]<FORWARD>], ROM[BAM[parameters]<FORWARD>], ACC ) ;\n")
        f.write("\t\t\tADD ( REG[1], ACC, REG[1]) ;\n")
        f.write("\t\t}\n")
        f.write("\t\t\n")
        f.write("\t\t// Add popcountA and popcountB to get full popcount\n")
        f.write("\t\t// At this point popcountB (REG[1]) isn't fetchable, but is still in ACC\n")
        f.write("\t\tADD ( REG[0], ACC, PUT[0]) ;\n")
        f.write("\t}\n")
        f.write("\tNOP ;\n")
        f.write("}\n")

    # Generate rom File
    with open("layer_%i_ROM.mem"%(layer_number, ), "w") as f:
        for _ in range(output_lenght):
            for _ in range(input_lenght):
                f.write(tc_utils.unsigned.encode(random.randrange(2), 1))
                f.write("\n")

    # Generate parameter File
    with open("layer_%i_parameters.json"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t\"SIMD\": {\n")
        f.write("\t\t\"lanes\": 1\n")
        f.write("\t},\n")

        f.write("\t\"address_sources\": {\n")
        f.write("\t\t\"BAM_0\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(input_lenght - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(input_lenght - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_1\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(ROM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(ROM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n" )
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"data_memories\": {\n")
        f.write("\t\t\"GET\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"PUT\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": %i\n"%(pop_width, ) )
        f.write("\t\t},\n")
        f.write("\t\t\"RAM\": {\n")
        f.write("\t\t\t\"data_width\": 1,\n")
        f.write("\t\t\t\"depth\": %i\n"%(input_lenght, ))
        f.write("\t\t},\n")
        f.write("\t\t\"REG\": {\n")
        f.write("\t\t\t\"data_width\": 1,\n")
        f.write("\t\t\t\"depth\": 2\n")
        f.write("\t\t},\n")
        f.write("\t\t\"ROM\": {\n")
        f.write("\t\t\t\"data_width\": 1,\n")
        f.write("\t\t\t\"depth\": %i\n"%(ROM_depth, ))
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"execute_units\": {\n")
        f.write("\t\t\"ALU\": {\n")
        f.write("\t\t\t\"data_width\": %i\n"%(pop_width, ))
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"instr_decoder\": {},\n")
        f.write("\t\"program_flow\": {}\n")
        f.write("}\n")

    # Generate generics File
    with open("layer_%i_generics.json"%(layer_number), "w") as f:
        f.write("{\n")
        f.write("\t\"BAM_0_base\": 0,\n")
        f.write("\t\"BAM_0_increment\": 1,\n")
        f.write("\t\"BAM_1_base\": 0,\n")
        f.write("\t\"BAM_1_increment\": 1,\n")
        f.write("\t\"ROM_mem_file\": \"..\\\\layer_%i_ROM.mem\"\n"%(layer_number, ))
        f.write("}\n")

# Make sure is FPE discoverable
if __name__ == "__main__":
    # Init generation and return varables
    IMPORTS   = []
    ARCH_HEAD = gen_utils.indented_string()
    ARCH_BODY = gen_utils.indented_string()
    INTERFACE = { "ports" : [], "generics" : [] }

    # Include extremely commom libs
    IMPORTS += [
        {
            "library" : "ieee",
            "package" : "std_logic_1164",
            "parts" : "all"
        }
    ]

    # Connect data ports
    INTERFACE["ports"] += [
        {
            "name" : "clock",
            "type" : "std_logic",
            "direction" : "in"
        }
    ]

    input_r = 32
    input_c = 32
    input_d = 24

    layers = [
        {
            "type" : "conv",
            "channels" : 64
        },
        {
            "type" : "conv",
            "channels" : 64
        },
        {
            "type" : "pool"
        },

        {
            "type" : "conv",
            "channels" : 128
        },
        {
            "type" : "conv",
            "channels" : 128
        },
        {
            "type" : "pool"
        },

        {
            "type" : "conv",
            "channels" : 256
        },
        {
            "type" : "conv",
            "channels" : 256
        },
        {
            "type" : "pool"
        },

        {
            "type" : "dense",
            "channels" : 512
        },
        {
            "type" : "last",
            "channels" : 10
        }
    ]

    for layer, details in enumerate(layers):
        if   details["type"] == "conv":
            # Generate input FIFO
            FIFO_config = {
                "width" : 1,
                "depth" : input_r * input_c * input_d
            }
            FIFO_name = generator.generate(
                "memory.FIFO",
                "FIFO",
                FIFO_config,
                ".\\toolchain_files",
                True,
                True
            )

            # Instancate input FIFO
            ARCH_BODY += "FIFO_%i : entity work.%s(arch)\n\>"%(layer, FIFO_name,)
            ARCH_BODY += "port map (\>\n"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "clear => '0',\n"
            ARCH_BODY += "full  => open,\n"
            ARCH_BODY += "empty => open,\n"

            if layer == 0:
                INTERFACE["ports"] += [
                    {
                        "name" : "input_data",
                        "type" : "std_logic_vector(0 downto 0)",
                        "direction" : "in"
                    },
                    {
                        "name" : "input_write",
                        "type" : "std_logic",
                        "direction" : "in"
                    },
                    {
                        "name" : "input_ready",
                        "type" : "std_logic",
                        "direction" : "out"
                    },
                ]

                ARCH_BODY += "data_in => input_data,\n"
                ARCH_BODY += "data_write => input_write,\n"
                ARCH_BODY += "data_write_ready => input_ready,\n"
            else:
                ARCH_HEAD += "signal FIFO_%i_data_in : std_logic_vector(0 downto 0);\n"%(layer, )
                ARCH_HEAD += "signal FIFO_%i_data_write : std_logic;\n"%(layer, )
                ARCH_HEAD += "signal FIFO_%i_data_write_ready : std_logic;\n"%(layer, )

                ARCH_BODY += "data_in => FIFO_%i_data_in,\n"%(layer, )
                ARCH_BODY += "data_write => FIFO_%i_data_write,\n"%(layer, )
                ARCH_BODY += "data_write_ready => FIFO_%i_data_write_ready,\n"%(layer, )

            ARCH_HEAD += "signal FIFO_%i_data_out : std_logic_vector(0 downto 0);\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_read : std_logic;\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_read_ready : std_logic;\n"%(layer, )

            ARCH_BODY += "data_out => FIFO_%i_data_out,\n"%(layer, )
            ARCH_BODY += "data_read => FIFO_%i_data_read,\n"%(layer, )
            ARCH_BODY += "data_read_ready => FIFO_%i_data_read_ready\n"%(layer, )

            ARCH_BODY += "\<);\<\n\n"

            # Generate layer FPE
            generate_conv_files(layer + 1, input_r, input_c, input_d, details["channels"])
            test_utils.run_toolchain(
                "layer_%i_program.fpea"%(layer + 1, ),
                "layer_%i_parameters.json"%(layer + 1, ),
                "layer_%i_generics.json"%(layer + 1, ),
                ".\\toolchain_files",
                "layer_%i_FPE"%(layer + 1, ),
                False,
                True
            )

            # Instancate FPE
            ARCH_HEAD += "signal layer_%i_FPE_kickoff : std_logic;\n"%(layer + 1, )
            ARCH_BODY += "layer_%i_FPE_kickoff <= FIFO_%i_data_read_ready and FIFO_%i_data_write_ready;\n"%(layer + 1, layer, layer + 1, )

            ARCH_BODY += "layer_%i_FPE : entity work.layer_%i_FPE_inst(arch)\n\>"%(layer + 1, layer + 1, )
            ARCH_BODY += "port map (\>\n"

            ARCH_BODY += "GET_FIFO_0_data => FIFO_%i_data_out,\n" %(layer, )
            ARCH_BODY += "GET_FIFO_0_red  => FIFO_%i_data_read,\n"%(layer, )

            ARCH_BODY += "PUT_FIFO_0_data  => FIFO_%i_data_in,\n"   %(layer + 1, )
            ARCH_BODY += "PUT_FIFO_0_write => FIFO_%i_data_write,\n"%(layer + 1, )

            ARCH_BODY += "kickoff => layer_%i_FPE_kickoff,\n"%(layer + 1, )

            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "running => open\n"

            ARCH_BODY += "\<);\<\n\n"

            # Update input_r, input_c, input_d for next layer
            input_r = input_r
            input_c = input_c
            input_d = details["channels"]

        elif details["type"] == "pool":
            # Generate input FIFO
            FIFO_config = {
                "width" : 1,
                "depth" : input_r * input_c * input_d
            }
            FIFO_name = generator.generate(
                "memory.FIFO",
                "FIFO",
                FIFO_config,
                ".\\toolchain_files",
                True,
                True
            )

            # Instancate input FIFO
            ARCH_BODY += "FIFO_%i : entity work.%s(arch)\n\>"%(layer, FIFO_name,)
            ARCH_BODY += "port map (\>\n"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "clear => '0',\n"
            ARCH_BODY += "full  => open,\n"
            ARCH_BODY += "empty => open,\n"

            ARCH_HEAD += "signal FIFO_%i_data_in : std_logic_vector(0 downto 0);\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_write : std_logic;\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_write_ready : std_logic;\n"%(layer, )

            ARCH_BODY += "data_in => FIFO_%i_data_in,\n"%(layer, )
            ARCH_BODY += "data_write => FIFO_%i_data_write,\n"%(layer, )
            ARCH_BODY += "data_write_ready => FIFO_%i_data_write_ready,\n"%(layer, )

            ARCH_HEAD += "signal FIFO_%i_data_out : std_logic_vector(0 downto 0);\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_read : std_logic;\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_read_ready : std_logic;\n"%(layer, )

            ARCH_BODY += "data_out => FIFO_%i_data_out,\n"%(layer, )
            ARCH_BODY += "data_read => FIFO_%i_data_read,\n"%(layer, )
            ARCH_BODY += "data_read_ready => FIFO_%i_data_read_ready\n"%(layer, )

            ARCH_BODY += "\<);\<\n\n"

            # Generate layer FPE
            generate_pool_files(layer + 1, input_r, input_c, input_d)
            test_utils.run_toolchain(
                "layer_%i_program.fpea"%(layer + 1, ),
                "layer_%i_parameters.json"%(layer + 1, ),
                "layer_%i_generics.json"%(layer + 1, ),
                ".\\toolchain_files",
                "layer_%i_FPE"%(layer + 1, ),
                False,
                True
            )

            # Instancate FPE
            ARCH_HEAD += "signal layer_%i_FPE_kickoff : std_logic;\n"%(layer + 1, )
            ARCH_BODY += "layer_%i_FPE_kickoff <= FIFO_%i_data_read_ready and FIFO_%i_data_write_ready;\n"%(layer + 1, layer, layer + 1, )

            ARCH_BODY += "layer_%i_FPE : entity work.layer_%i_FPE_inst(arch)\n\>"%(layer + 1, layer + 1, )
            ARCH_BODY += "port map (\>\n"

            ARCH_BODY += "GET_FIFO_0_data => FIFO_%i_data_out,\n" %(layer, )
            ARCH_BODY += "GET_FIFO_0_red  => FIFO_%i_data_read,\n"%(layer, )

            ARCH_BODY += "PUT_FIFO_0_data  => FIFO_%i_data_in,\n"   %(layer + 1, )
            ARCH_BODY += "PUT_FIFO_0_write => FIFO_%i_data_write,\n"%(layer + 1, )

            ARCH_BODY += "kickoff => layer_%i_FPE_kickoff,\n"%(layer + 1, )

            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "running => open\n"

            ARCH_BODY += "\<);\<\n\n"

            # Update input_r, input_c, input_d for next layer
            input_r = int(input_r / 2)
            input_c = int(input_c / 2)
            input_d = input_d
        elif details["type"] == "dense":
            # Generate input FIFO
            FIFO_config = {
                "width" : 1,
                "depth" : input_r * input_c * input_d
            }
            FIFO_name = generator.generate(
                "memory.FIFO",
                "FIFO",
                FIFO_config,
                ".\\toolchain_files",
                True,
                True
            )

            # Instancate input FIFO
            ARCH_BODY += "FIFO_%i : entity work.%s(arch)\n\>"%(layer, FIFO_name,)
            ARCH_BODY += "port map (\>\n"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "clear => '0',\n"
            ARCH_BODY += "full  => open,\n"
            ARCH_BODY += "empty => open,\n"

            ARCH_HEAD += "signal FIFO_%i_data_in : std_logic_vector(0 downto 0);\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_write : std_logic;\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_write_ready : std_logic;\n"%(layer, )

            ARCH_BODY += "data_in => FIFO_%i_data_in,\n"%(layer, )
            ARCH_BODY += "data_write => FIFO_%i_data_write,\n"%(layer, )
            ARCH_BODY += "data_write_ready => FIFO_%i_data_write_ready,\n"%(layer, )

            ARCH_HEAD += "signal FIFO_%i_data_out : std_logic_vector(0 downto 0);\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_read : std_logic;\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_read_ready : std_logic;\n"%(layer, )

            ARCH_BODY += "data_out => FIFO_%i_data_out,\n"%(layer, )
            ARCH_BODY += "data_read => FIFO_%i_data_read,\n"%(layer, )
            ARCH_BODY += "data_read_ready => FIFO_%i_data_read_ready\n"%(layer, )

            ARCH_BODY += "\<);\<\n\n"

            generate_dense_files(layer + 1, input_r * input_c * input_d, details["channels"])
            test_utils.run_toolchain(
                "layer_%i_program.fpea"%(layer + 1, ),
                "layer_%i_parameters.json"%(layer + 1, ),
                "layer_%i_generics.json"%(layer + 1, ),
                ".\\toolchain_files",
                "layer_%i_FPE"%(layer + 1, ),
                False,
                True
            )

            # Instancate FPE
            ARCH_HEAD += "signal layer_%i_FPE_kickoff : std_logic;\n"%(layer + 1, )
            ARCH_BODY += "layer_%i_FPE_kickoff <= FIFO_%i_data_read_ready and FIFO_%i_data_write_ready;\n"%(layer + 1, layer, layer + 1, )

            ARCH_BODY += "layer_%i_FPE : entity work.layer_%i_FPE_inst(arch)\n\>"%(layer + 1, layer + 1, )
            ARCH_BODY += "port map (\>\n"

            ARCH_BODY += "GET_FIFO_0_data => FIFO_%i_data_out,\n" %(layer, )
            ARCH_BODY += "GET_FIFO_0_red  => FIFO_%i_data_read,\n"%(layer, )

            ARCH_BODY += "PUT_FIFO_0_data  => FIFO_%i_data_in,\n"   %(layer + 1, )
            ARCH_BODY += "PUT_FIFO_0_write => FIFO_%i_data_write,\n"%(layer + 1, )

            ARCH_BODY += "kickoff => layer_%i_FPE_kickoff,\n"%(layer + 1, )

            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "running => open\n"

            ARCH_BODY += "\<);\<\n\n"

            # Update input_r, input_c, input_d for next layer
            input_r = 1
            input_c = 1
            input_d = details["channels"]
        elif details["type"] == "last":
            # Generate input FIFO
            FIFO_config = {
                "width" : 1,
                "depth" : input_r * input_c * input_d
            }
            FIFO_name = generator.generate(
                "memory.FIFO",
                "FIFO",
                FIFO_config,
                ".\\toolchain_files",
                True,
                True
            )

            # Instancate input FIFO
            ARCH_BODY += "FIFO_%i : entity work.%s(arch)\n\>"%(layer, FIFO_name,)
            ARCH_BODY += "port map (\>\n"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "clear => '0',\n"
            ARCH_BODY += "full  => open,\n"
            ARCH_BODY += "empty => open,\n"

            ARCH_HEAD += "signal FIFO_%i_data_in : std_logic_vector(0 downto 0);\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_write : std_logic;\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_write_ready : std_logic;\n"%(layer, )

            ARCH_BODY += "data_in => FIFO_%i_data_in,\n"%(layer, )
            ARCH_BODY += "data_write => FIFO_%i_data_write,\n"%(layer, )
            ARCH_BODY += "data_write_ready => FIFO_%i_data_write_ready,\n"%(layer, )

            ARCH_HEAD += "signal FIFO_%i_data_out : std_logic_vector(0 downto 0);\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_read : std_logic;\n"%(layer, )
            ARCH_HEAD += "signal FIFO_%i_data_read_ready : std_logic;\n"%(layer, )

            ARCH_BODY += "data_out => FIFO_%i_data_out,\n"%(layer, )
            ARCH_BODY += "data_read => FIFO_%i_data_read,\n"%(layer, )
            ARCH_BODY += "data_read_ready => FIFO_%i_data_read_ready\n"%(layer, )

            ARCH_BODY += "\<);\<\n\n"

            pop_width = tc_utils.unsigned.width(input_r * input_c * input_d + 1)
            generate_last_files(layer + 1, input_r * input_c * input_d, details["channels"])
            test_utils.run_toolchain(
                "layer_%i_program.fpea"%(layer + 1, ),
                "layer_%i_parameters.json"%(layer + 1, ),
                "layer_%i_generics.json"%(layer + 1, ),
                ".\\toolchain_files",
                "layer_%i_FPE"%(layer + 1, ),
                False,
                True
            )
            # Instancate FPE
            ARCH_HEAD += "signal layer_%i_FPE_kickoff : std_logic;\n"%(layer + 1, )
            ARCH_BODY += "layer_%i_FPE_kickoff <= FIFO_%i_data_read_ready and FIFO_%i_data_write_ready;\n"%(layer + 1, layer, layer + 1, )

            ARCH_BODY += "layer_%i_FPE : entity work.layer_%i_FPE_inst(arch)\n\>"%(layer + 1, layer + 1, )
            ARCH_BODY += "port map (\>\n"

            ARCH_BODY += "GET_FIFO_0_data => FIFO_%i_data_out,\n" %(layer, )
            ARCH_BODY += "GET_FIFO_0_red  => FIFO_%i_data_read,\n"%(layer, )

            ARCH_BODY += "PUT_FIFO_0_data  => FIFO_%i_data_in,\n"   %(layer + 1, )
            ARCH_BODY += "PUT_FIFO_0_write => FIFO_%i_data_write,\n"%(layer + 1, )

            ARCH_BODY += "kickoff => layer_%i_FPE_kickoff,\n"%(layer + 1, )

            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "running => open\n"

            ARCH_BODY += "\<);\<\n\n"

            # Generate output FIFO
            FIFO_config = {
                "width" : pop_width,
                "depth" : details["channels"]
            }
            FIFO_name = generator.generate(
                "memory.FIFO",
                "FIFO",
                FIFO_config,
                ".\\toolchain_files",
                True,
                True
            )

            # Instancate input FIFO
            ARCH_BODY += "FIFO_%i : entity work.%s(arch)\n\>"%(layer + 1, FIFO_name,)
            ARCH_BODY += "port map (\>\n"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "clear => '0',\n"
            ARCH_BODY += "full  => open,\n"
            ARCH_BODY += "empty => open,\n"

            ARCH_HEAD += "signal FIFO_%i_data_in : std_logic_vector(%i downto 0);\n"%(layer + 1, pop_width - 1, )
            ARCH_HEAD += "signal FIFO_%i_data_write : std_logic;\n"%(layer + 1, )
            ARCH_HEAD += "signal FIFO_%i_data_write_ready : std_logic;\n"%(layer + 1, )

            ARCH_BODY += "data_in => FIFO_%i_data_in,\n"%(layer + 1, )
            ARCH_BODY += "data_write => FIFO_%i_data_write,\n"%(layer + 1, )
            ARCH_BODY += "data_write_ready => FIFO_%i_data_write_ready,\n"%(layer + 1, )

            INTERFACE["ports"] += [
                {
                    "name" : "output_data",
                    "type" : "std_logic_vector(%i downto 0)"%(pop_width - 1, ),
                    "direction" : "out"
                },
                {
                    "name" : "output_read",
                    "type" : "std_logic",
                    "direction" : "in"
                },
                {
                    "name" : "output_ready",
                    "type" : "std_logic",
                    "direction" : "out"
                },
            ]

            ARCH_BODY += "data_out => output_data,\n"
            ARCH_BODY += "data_read => output_read,\n"
            ARCH_BODY += "data_read_ready => output_ready\n"

            ARCH_BODY += "\<);\<\n\n"

            # Update input_r, input_c, input_d for next layer
            input_r = 1
            input_c = 1
            input_d = details["channels"]

    # Save code to file
    gen_utils.generate_files(".", "network_baseline", IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)
