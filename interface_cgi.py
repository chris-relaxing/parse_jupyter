#!C:\Python27\python.exe -u

# To do:
# 1. Clean up code
# 2. Add docstrings to all functions
# 3. Clean up user interface
# 4. Create a link to see the created html result (or popup window?)
# 5. CSS for the buttons
# 6. Command window version of the script?
# 7. Think of a good name for the script

import requests     # to get the source of Jupyter Notebooks
import cgi
import os

# Create instance of FieldStorage
form = cgi.FieldStorage()

# globals
page_source = ''
##selected_notebook = ''
cell_numbers = []

# Get data from form fields
create_html = form.getvalue('create_html')
select_jupyter = form.getvalue('select_jupyter')
selected_cells = form.getvalue('selected_cells')
selected_filename = form.getvalue('selected_filename')
selected_notebook = form.getvalue('selected_notebook')
get_URL = form.getvalue('get_URL')
ex_head = form.getvalue('EX_HEAD')
ex_out = form.getvalue('EX_OUT')


# Make sure selected_cells is always an array
if type(selected_cells) == str:
    selected_cells = [selected_cells]

def loadNotebook():
    global page_source
    global selected_notebook
    global get_URL
    if select_jupyter:
        if get_URL or selected_notebook:

            # Get the source of the target notebook:
            target_notebook = get_URL
            ## target_notebook = r'http://bluegalaxy.info/new/sqlalchemy_tutorial.html'
    ##        target_notebook = r'http://localhost:8888/notebooks/docs/Winpython_checker.ipynb'
            r = requests.get(target_notebook)
            page_source = r.text
            page_source = page_source.split('\n')


    if createHTML and selected_notebook != None:
            # Get the source of the target notebook:
            target_notebook = selected_notebook
            r = requests.get(target_notebook)
            page_source = r.text
            page_source = page_source.split('\n')

##writer = open(r'C:\Bitnami\wampstack-5.6.31-0\apache2\htdocs\builds\page_source.txt','w')
##for line in page_source:
##    line = line.encode('UTF-8')
##    writer.write(line + '\n')
##writer.close()


def parseNotebook():
    header_pattern = """<div class="cell border-box-sizing text_cell rendered">"""
    input_pattern = """<div class="cell border-box-sizing code_cell rendered">"""
    output_pattern = """<div class="output_wrapper">"""
    cell_number_pattern = """<div class="prompt input_prompt">"""

    # Load the html doc into an array of lines
    global page_source
    if page_source:
        source_lines = page_source

        header_cell_locations = []
        input_cell_locations = []
        output_cell_locations = []
        section_indexes = []
        section_types = []
        global cell_map
        global cell_numbers
        end_of_doc = 0
        x = 0
        line_count = 0
        for line in source_lines:
            a = line.rstrip('\n')
            if a == header_pattern:
                header_cell_locations.append(x)
                section_types.append("HEADER")
                section_indexes.append(x)
                line_count += 1

            if a == input_pattern:
                input_cell_locations.append(x)
                section_types.append("IN")
                section_indexes.append(x)
                line_count += 1

            if a == output_pattern:
                output_cell_locations.append(x)
                section_types.append("OUT")
                section_indexes.append(x)
                line_count += 1

            if a == '</html>':
                end_of_doc = x + 1
            x += 1
        num_sections = len(header_cell_locations)

        # Calculate the ranges
        section_ranges = []
        x = 0
        y = 1
        L = section_indexes
        while y < len(L):
    ##        tup = (L[x], L[y]-1)
            tup = (L[x], L[y])
            section_ranges.append(tup)
            x += 1
            y += 1

##        last_range = (L[-1], end_of_doc-1)
##        section_ranges.append(last_range)

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
                header_block = block

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
                        cell_numbers.append(cell_number)
                        cell_map[cell_number] = {section_types[x]: [section_ranges[x], block]}
                        if previous_header == 1:
                            cell_map[cell_number]["HEADER"] = [header_range, header_block]
            if section_types[x] == "OUT":
                cell_map[cell_number]["OUT"] = [section_ranges[x], block]
            x += 1


        # Get rid of empty (non-numeric) keys

        for k in cell_map.keys():
            try:
                int(k)
            except:
                del cell_map[k]




def interface_form():
    global cell_map
    global cell_numbers
    global selected_notebook
    interface_form_string = """
    <FORM name="get_URL" METHOD=POST ACTION="http://1uslchriston.ad.here.com:90/cgi-bin/interface_cgi.py">
    <table width="100%" cellpadding="0" cellspacing="0" valign="top" border="0">
        <tr>
            <td>
            URL of Jupyter Notebook input: <INPUT TYPE=TEXT NAME="get_URL" size="60">
            <INPUT TYPE=SUBMIT name="select_jupyter" VALUE="select_jupyter" style='margin-right:3em'>
            </form>
            </td>
        </tr>
        <tr>
            <td>
            <FORM name="select_cells" METHOD=POST ACTION="http://1uslchriston.ad.here.com:90/cgi-bin/interface_cgi.py">
            <input class="button" type="button" value="Check All" onclick="javascript:checkAll('select_cells', true);">
	       </td>
	       <td align="right">
	       <input class="button" type="button" value="Uncheck All" onclick="javascript:checkAll('select_cells', false);">
	       </td>
       </tr>
    </table>

    """

    select_all_buttons = """
    Exclude Headers *<INPUT TYPE=RADIO NAME="EX_HEAD" VALUE="Exclude Headers" style='margin-right:3em'>
    Exclude Outputs *<INPUT TYPE=RADIO NAME="EX_OUT" VALUE="Exclude Outputs" style='margin-right:3em'>
    * Headers and outputs are included by default.
    <BR>
    """

    print interface_form_string

    if cell_numbers:
        print select_all_buttons

    for number in cell_numbers:
        if number in cell_map.keys():
            checkbox = number + '<INPUT TYPE=CHECKBOX NAME="selected_cells" VALUE="%s" style="margin-right:3em">'
            print checkbox % (number)



    form_bottom = """
    <BR><BR>
    Choose file name for the cells: <INPUT TYPE=TEXT NAME="selected_filename"> .html
    <input type="hidden" name="selected_notebook" value="%s">
    <BR><BR><BR>

    <CENTER><INPUT TYPE=SUBMIT name="create_html" VALUE="Create HTML" style='margin-right:3em'></CENTER>
    </FORM>

    <BR>
    """
    iframe =  """<iframe src="%s" scrolling="yes" width="100%%" height="800">"""
    print "<BR><BR>create_html:<b>", create_html, "</b>"
    print "<BR>selected_cells:<b>", selected_cells, "</b>"
    print "<BR>ex_head:<b>", ex_head, "</b>"
    print "<BR>ex_out:<b>", ex_out, "</b>"
    if get_URL:
        print "<BR>selected_notebook:<b>", get_URL, "</b>"
    elif selected_notebook != None:
        print "<BR>selected_notebook:<b>", selected_notebook, "</b>"

    # Place selected_notebook URL into the hidden tag
    if get_URL:
        print form_bottom % (get_URL)
    elif selected_notebook != None:
        print form_bottom % (selected_notebook)

    if get_URL:
        print iframe % (get_URL)
    elif createHTML and selected_notebook != None:
        print iframe % (selected_notebook)


interface_top = """
<html>
<head>
  <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
<style>
  body {
      font-family: 'Roboto', sans-serif;
      font-size: 16px;
  }
</style>
</head>
<body bgcolor="#ccc">

<script type="text/javascript" language="javascript">
    function checkAll(select_cells, checktoggle)
    {
      var checkboxes = new Array();
      checkboxes = document[select_cells].getElementsByTagName('input');

      for (var i=0; i<checkboxes.length; i++)  {
        if (checkboxes[i].type == 'checkbox')   {
          checkboxes[i].checked = checktoggle;
        }
      }
    }
</script>
<h2>Select Cells to export</h2>

"""


interface_bottom = """
</body>
</html>"""


def print_output():
    print "Content-type: text/html\n\n";
    parseNotebook()
    print interface_top
    interface_form()
    print interface_bottom

def createHTML():

    html_close = """
</div>
<div id="maintoolbar" class="navbar">
</body>
</html>
    """

    if create_html:
        global selected_filename
        global page_source
        template_path = "C:\\Bitnami\\wampstack-5.6.31-0\\apache2\\htdocs\\templates\\"
        selected_filename = selected_filename + ".html"
        writepath = "C:\\Bitnami\\wampstack-5.6.31-0\\apache2\\htdocs\\builds\\" + selected_filename

        # Get top portion of html
        build_top = template_path + "\\nb_top.txt"
        f = open(build_top, 'r')
        top = f.readlines()
        f.close()

        writer = open(writepath,'w')
        for line in top:
            writer.write(line)
        # num 	{'HEADER': (11748, 11756), 'OUT': (11773, 11788), 'IN': (11757, 11772)}
        for num in selected_cells:
            begin_next_cell = r'<!--  Beginning of next cell  -->'
            writer.write('\n\n' + begin_next_cell + '\n')
            header = cell_map[num].get('HEADER', '')
            if header:
                header_range = header[0]
                print "header_range", header_range
                start = header_range[0]
                end = header_range[1]
                header_block = page_source[start: end]
                for line in header_block:
                    line = line.encode('UTF-8')
                    writer.write(line + '\n')
            input_cell = cell_map[num].get('IN', '')
            if input_cell:
                input_range = input_cell[0]
                print "input_range", input_range

                start = input_range[0]
                end = input_range[1]
                input_block = page_source[start: end]
                for line in input_block:
                    line = line.encode('UTF-8')
                    writer.write(line + '\n')

            output_cell = cell_map[num].get('OUT', '')
            if output_cell:
                output_range = output_cell[0]
                print "output_range", output_range

                start = output_range[0]
                end = output_range[1]
                output_block = page_source[start: end]
                for line in output_block:
                    line = line.encode('UTF-8')
                    writer.write(line + '\n')

        writer.write('\n' + html_close)
        writer.close()



def main():
    loadNotebook()
    print_output()
    global page_source
    createHTML()

if __name__ == '__main__':
    main()
