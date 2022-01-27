# Current controls structure
# controls {
#     stage : {
#         signal : {
#             "type" : str
#             "width" : int | None
#             "values" : {
#                 value : [instr, instr]
#             }
#          }
#     }
# }

def init_controls():
    return { }

def add_control(controls, stage, signal, values, signal_type, width = None):

    assert type(controls) == dict, "controls must be a dict"
    assert type(stage) == str, "stage must be a string"
    assert type(signal) == str, "signal must be a string"
    assert type(values) == dict, "values must be a dict"
    assert type(signal_type) == str, "signal_type must be a string"
    assert type(width) == int or width == None, "signal_width must be an int or None"
    if __debug__ and signal_type.endswith("_vector"):
        assert type(width) == int, "signal_width must be an int (for vector type)"

    if __debug__:
        try:
            assert signal not in controls[stage].keys()
        except KeyError:
            pass

    try:
        controls[stage][signal] = {
            "values" : values,
            "type" : signal_type,
            "width" : width,
        }
    except KeyError as e:
        controls[stage] = {
            signal : {
                "values" : values,
                "type" : signal_type,
                "width" : width,
            }
        }
    return controls

def merge_controls(A, B):
    C = init_controls()

    for stage, stage_details in A.items():
        for signal, signal_details in stage_details.items():
            values = signal_details["values"]
            signal_type = signal_details["type"]
            width = signal_details["width"]
            add_control(C, stage, signal, values, signal_type, width)

    for stage, stage_details in B.items():
        for signal, signal_details in stage_details.items():
            values = signal_details["values"]
            signal_type = signal_details["type"]
            width = signal_details["width"]
            add_control(C, stage, signal, values, signal_type, width)

    return C

def get_controls(controls, stage=None):
    assert stage == None or type(stage) == str

    if stage != None:
        try:
            return controls[stage]
        except KeyError:
            return {}
    else:
        return controls
