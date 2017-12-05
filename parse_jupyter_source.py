#!C:\Python27\python.exe -u

jupyter_source = r'C:\Users\christon\Desktop\Jupyter Notebook Parse\sqlalchemy_tutorial_source.txt'

header_pattern = """<div class="cell border-box-sizing text_cell rendered">"""
input_pattern = """<div class="cell border-box-sizing code_cell rendered">"""
output_pattern = """<div class="output_wrapper">"""

with open(jupyter_source, 'r') as f:
    header_cell_locations = []
    input_cell_locations = []
    output_cell_locations = []
    sections_profile = []
    x = 0
    line_count = 0
    for line in f:
        a = line.rstrip('\n')

        # If an input cell is found, then start gathering all subsequent cells into a string
        # until a new pattern is found. Then read the input number.

        if a == header_pattern:
            print x, '\t', a, "------------------------------------"
            header_cell_locations.append(x)
            p = str(x) + '\tHEADER'
            sections_profile.append(p)
            line_count += 1

        if a == input_pattern:
            print x, '\t', a
            input_cell_locations.append(x)
            p = str(x) + '\tIN'
            sections_profile.append(p)
            line_count += 1

        if a == output_pattern:
            print x, '\t', a
            output_cell_locations.append(x)
            p = str(x) + '\tOUTPUT'
            sections_profile.append(p)
            line_count += 1
        x += 1

num_sections = len(header_cell_locations)
print "There are", num_sections, "sections."
print header_cell_locations
print input_cell_locations
print output_cell_locations

for l in sections_profile:
    print l


