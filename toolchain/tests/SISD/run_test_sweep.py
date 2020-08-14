# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

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
    test_name = test.__file__.split("\\")[-2]
    test_path = ".\\" + test_name

    print("\n#####################################################")
    print("Running %s test" %(test_name))
    print("#####################################################")

    result = test.run_test(path=test_path)
    if result != 0:
        raise ValueError("%s, failed with code %i"%(str(test_name), result))
    else:
        print("%s, passed"%(str(test_name)))
