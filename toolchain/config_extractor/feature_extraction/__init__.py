from . import PC_extraction

from . import IMM_extraction
from . import BAM_extraction
from . import hidden_ZOL_extraction
from . import declared_ZOL_extraction
from . import rep_bank_extraction

from . import instruction_set_extraction

features = [
    # Early passes, produce data required for laster passes
    PC_extraction,

    # Mid passes, dependant on data for Early passes but no other dependanes
    IMM_extraction,
    BAM_extraction,
    hidden_ZOL_extraction,
    declared_ZOL_extraction,
    rep_bank_extraction,

    # Late passes, dependant data from a lot of other passes data for Early passes but no other dependanes
    instruction_set_extraction,
]
