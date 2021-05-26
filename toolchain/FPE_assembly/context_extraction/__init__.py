from . import constant_extractor
from . import jump_label_extractor
from . import loop_label_extractor
from . import component_extractor

extractors = [
    constant_extractor,
    jump_label_extractor,
    loop_label_extractor,
    component_extractor,
]
