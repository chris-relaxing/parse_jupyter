#!C:\Python27\python.exe -u

jupyter_source = r'C:\Users\christon\Desktop\Jupyter Notebook Parse\sqlalchemy_tutorial_source.txt'

header_pattern = """<div class="cell border-box-sizing text_cell rendered">"""
input_pattern = """<div class="cell border-box-sizing code_cell rendered">"""
output_pattern = """<div class="output_wrapper">"""
cell_number_pattern = """<div class="prompt input_prompt">"""

# things to store:
# 1. the range for each cell (values) - first store these as a list
# 2. the cell number (keys)
# how to determine the last range? take from starting to end of document

# Load the html doc into an array of lines
f = open(jupyter_source, 'r')
source_lines = f.readlines()
f.close()

with open(jupyter_source, 'r') as f:

    header_cell_locations = []
    input_cell_locations = []
    output_cell_locations = []
    sections_profile = []
    section_indexes = []
    section_types = []
    end_of_doc = 0
    x = 0
    line_count = 0
    for line in f:
        a = line.rstrip('\n')

        # If an input cell is found, then start gathering all subsequent cells into a string
        # until a new pattern is found. Then read the input number.

        if a == header_pattern:
##            print x, '\t', a, "------------------------------------"
            header_cell_locations.append(x)
            p = '\n' + str(x) + '\tHEADER'
            sections_profile.append(p)
            section_types.append("HEADER")
            section_indexes.append(x)
            line_count += 1

        if a == input_pattern:
##            print x, '\t', a
            input_cell_locations.append(x)
            p = str(x) + '\tIN'
            sections_profile.append(p)
            section_types.append("IN")
            section_indexes.append(x)
            line_count += 1

        if a == output_pattern:
##            print x, '\t', a
            output_cell_locations.append(x)
            p = str(x) + '\tOUTPUT'
            sections_profile.append(p)
            section_types.append("OUT")
            section_indexes.append(x)
            line_count += 1

        if a == '</html>':
##            print x, '\t', a, " End of last cell range.."
            end_of_doc = x + 1

        x += 1

num_sections = len(header_cell_locations)
##print "There are", num_sections, "sections."
##print header_cell_locations
##print input_cell_locations
##print output_cell_locations

##for l in sections_profile:
##    print l

##for r in section_indexes:
##    print r

##print section_indexes
##print section_types

##print "End of doc:", end_of_doc

# Calculate the ranges
section_ranges = []
x = 0
y = 1
L = section_indexes
while y < len(L):
    tup = (L[x], L[y]-1)
    section_ranges.append(tup)
##    print tup
    x += 1
    y += 1

last_range = (L[-1], end_of_doc-1)
section_ranges.append(last_range)
##print "Number of ranges:", len(section_ranges)

##for r in section_ranges:
##    print r

# Create a dictionary to store the complete picture
# keys = cell numbers
# values = dict where keys = cell type and values = section range
cell_map = {}

x = 0
HEADER = 0
cell_number = 0
previous_header = 0
cell_numbers = []
while x < len(section_ranges):

    cell_type = section_types[x]
    section = section_ranges[x]
    s1 = section[0]
    s2 = section[1]
    block1 = source_lines[s1:s2]
    block = ''.join(block1)
##    print  "--------------------------------------\n", block
    if cell_type == "HEADER":
        HEADER = 1
        header_range = section_ranges[x]

    if cell_type == "IN":
        if HEADER == 1:
            previous_header = 1
            HEADER = 0
        else:
            previous_header = 0
        for row in block1:
            if cell_number_pattern in row:
                target_line = row
                target_line = target_line.split('>')[1]
                target_line = target_line.split('<')[0]
                cell_number = target_line.split('[')[1]
                cell_number = cell_number.split(']')[0]
##                print "\n--------------cell number is:", cell_number
##                print "previous was header", previous_header
                cell_numbers.append(cell_number)
                cell_map[cell_number] = {section_types[x]: section_ranges[x]}

                if previous_header == 1:
                    cell_map[cell_number]["HEADER"] = header_range

##    print section_ranges[x], '\t',  section_types[x]
    if section_types[x] == "OUT":
        cell_map[cell_number]["OUT"] = section_ranges[x]
    x += 1

##print cell_numbers
print "\nBefore:", len(cell_map.keys())
for k, v in sorted(cell_map.iteritems()):
    print k, '\t', v

# Get rid of empty (non-numeric) keys

for k in cell_map.keys():
    try:
        int(k)
    except:
        del cell_map[k]

print "\nAfter:", len(cell_map.keys())
for k, v in sorted(cell_map.iteritems()):
    print k, '\t', v

