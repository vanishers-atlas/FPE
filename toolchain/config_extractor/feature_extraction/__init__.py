from . import PC_extraction
from . import IMM_extraction

from . import BAM_extraction
from . import ZOL_extraction

from . import instruction_set_extraction

features = [
    # Early passes, produce data required for laster passes
    PC_extraction,
    IMM_extraction,

    # Mid passes, dependant on data for Early passes but no other dependanes
    BAM_extraction,
    ZOL_extraction,

    # Late passes, dependant data from a lot of other passes data for Early passes but no other dependanes
    instruction_set_extraction,
]
