# Add FPE to PYTHONPATH
import sys, os
sys.path.append("\\".join(os.getcwd().split("\\")[:-2]))

import output_test_single_channel
import ZOL_test
import BAM_test
import ALU_test
import input_test_single_channel
import store_and_fetch_test_ram
import store_and_fetch_test_reg
import jumping_test

for test in [
        output_test_single_channel,
        ZOL_test,
        BAM_test,
        ALU_test,
        input_test_single_channel,
        store_and_fetch_test_ram,
        store_and_fetch_test_reg,
        jumping_test,
    ]:
    result = test.run_test(path="\\".join(test.__file__.split("\\")[-2:-1]))
    if result != 0:
        raise ValueError("%s, failed with code %i"%(str(test), result))
    else:
        print("%s, passed"%(str(test)))
