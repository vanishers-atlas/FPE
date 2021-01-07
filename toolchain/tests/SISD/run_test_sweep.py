# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys, os

    path_to_file = os.path.abspath(__file__)
    sys.path.append("\\".join(path_to_file.split("\\")[:2]))
    sys.path.append("\\".join(path_to_file.split("\\")[:-2]))
    parent_dir_path = "\\".join(path_to_file.split("\\")[:-1]).replace("\\", "/")

import ALU_test_simple_AB
import ALU_test_true_AB
import BAM_test
import input_test_single_channel
import JMP_test
import output_test_single_channel
import SCMP_JEQ_test
import SCMP_JGE_test
import SCMP_JGT_test
import SCMP_JLE_test
import SCMP_JLT_test
import SCMP_JNE_test
import store_and_fetch_test_ram
import store_and_fetch_test_reg
import UCMP_JEQ_test
import UCMP_JGE_test
import UCMP_JGT_test
import UCMP_JLE_test
import UCMP_JLT_test
import UCMP_JNE_test
import UCMP_SCMP_JEQ_test
import UCMP_SCMP_JGE_test
import UCMP_SCMP_JGT_test
import UCMP_SCMP_JLE_test
import UCMP_SCMP_JLT_test
import UCMP_SCMP_JNE_test
import ZOL_test

for test in [
    ALU_test_simple_AB,
    ALU_test_true_AB,
    BAM_test,
    input_test_single_channel,
    JMP_test,
    output_test_single_channel,
    SCMP_JEQ_test,
    SCMP_JGE_test,
    SCMP_JGT_test,
    SCMP_JLE_test,
    SCMP_JLT_test,
    SCMP_JNE_test,
    store_and_fetch_test_ram,
    store_and_fetch_test_reg,
    UCMP_JEQ_test,
    UCMP_JGE_test,
    UCMP_JGT_test,
    UCMP_JLE_test,
    UCMP_JLT_test,
    UCMP_JNE_test,
    UCMP_SCMP_JEQ_test,
    UCMP_SCMP_JGE_test,
    UCMP_SCMP_JGT_test,
    UCMP_SCMP_JLE_test,
    UCMP_SCMP_JLT_test,
    UCMP_SCMP_JNE_test,
    ZOL_test
    ]:

    test_dir = test.__file__.split("\\")[-2]
    print("\n#####################################################")
    print("Running %s test" % (test_dir))
    print("#####################################################")
    result = test.run_test(path="%s/%s" % (parent_dir_path, test_dir))
    assert result == 0, "%s, failed with code %i" % (str(test), result)

