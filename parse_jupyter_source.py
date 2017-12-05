#!C:\Python27\python.exe -u



jupyter_source = r'C:\Users\christon\Desktop\Jupyter Notebook Parse\sqlalchemy_tutorial_source.txt'

header_pattern = """<div class="cell border-box-sizing text_cell rendered">"""
input_pattern = """<div class="cell border-box-sizing code_cell rendered">"""
output_pattern = """<div class="output_wrapper">"""

with open(jupyter_source, 'r') as f:
    x = 0
    line_count = 0
    for line in f:
        a = line.rstrip('\n')

        if a == output_pattern:
            print a
            line_count += 1
        x += 1


print line_count


