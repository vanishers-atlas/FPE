import re
line_break = re.compile("\+(\-+\+)+")
key_line = re.compile("\|(\s*([\w ]+)\s*\|)+")

def process_report(report_text):
    # Split text in lines
    assert type(report_text) == str
    report_lines = report_text.split("\n")
    curr_line = 0

    # Check for header
    line_0_match  = line_break.match(report_lines[0])
    line_1_match  = key_line.match(report_lines[1])
    line_2_match  = line_break.match(report_lines[2])
    if not (line_0_match  and line_1_match and line_2_match ):
        raise ValueError("Invalid report_text format")

    # Handle key_line
    com_names_raw = report_lines[1].split("|")[3:-1]
    com_names = ["_" + com.strip() for com in com_names_raw]
    pattern_text= "\| (\s*)([\w\d\.\(\)\[\]_]+)\s*\|[^\|]+\|"
    for _ in com_names:
        pattern_text += "\s*(\d+) \|"
    extractor = re.compile(pattern_text)

    # Process body of table
    module, data, _ = __process_report(extractor, com_names, report_lines, 3, len(""))
    result = {module : data}

    return result

def __process_report(extractor, com_names, report_lines, line, curr_indent):
    next_line = line
    data = {}

    # Handle first line
    match = extractor.match(report_lines[line])
    module = match.groups()[1]
    coms = match.groups()[2:]
    for i, com in enumerate(com_names):
        data[com] = coms[i]

    # Handle next rows
    next_line = line + 1
    match = extractor.match(report_lines[next_line])
    while match and len(match.groups()[0]) > curr_indent:
        sub_module, sub_data, next_line = __process_report(extractor, com_names, report_lines, next_line, len(match.groups()[0]) )
        data[sub_module] = sub_data

        match = extractor.match(report_lines[next_line])

    return module, data, next_line

if __name__ == "__main__":
    import json
    import sys

    assert len(sys.argv) == 3
    report_text = None
    assert type(sys.argv[1]) == str
    with open(sys.argv[1], "r") as f:
        report_text = f.read()
    if report_text == None:
        print("ERROR: Couldbn't load supported file's data")
    else:
        report = process_report(report_text)
        with open(sys.argv[2], "w") as f:
            f.write(json.dumps(report, indent=2))
