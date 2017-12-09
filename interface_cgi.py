#!C:\Python27\python.exe -u

# To do:
# 1. Add docstrings to all functions
# 2. Command window version of the script?


import requests     # to get the source of Jupyter Notebooks
import cgi
import os

# Create instance of FieldStorage
form = cgi.FieldStorage()

# globals
page_source = ''
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
ex_head_out = form.getvalue('EX_HEAD_OUT')


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
            r = requests.get(target_notebook)
            page_source = r.text
            page_source = page_source.split('\n')


    if createHTML and selected_notebook != None:
            # Get the source of the target notebook:
            target_notebook = selected_notebook
            r = requests.get(target_notebook)
            page_source = r.text
            page_source = page_source.split('\n')


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
            tup = (L[x], L[y])
            section_ranges.append(tup)
            x += 1
            y += 1


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
    <table width="100%%" cellpadding="0" cellspacing="0" valign="top" border="0">
        <tr>
            <td>
            <h3>Input</h3>
            URL of Jupyter Notebook:
            <BR>(must be an html document stored on the web)<BR>
            <INPUT TYPE=TEXT NAME="get_URL" size="60">
            <INPUT TYPE="SUBMIT" name="select_jupyter" VALUE="Select Jupyter" class="btn">
            </form>
            </td>
        </tr>
    </table>
    """

    if cell_numbers:
        print interface_form_string
        confirmed_cell_numbers = []
        for number in cell_numbers:
            if number in cell_map.keys():
                confirmed_cell_numbers.append(number)
        print '<center>'
        printCheckboxes(confirmed_cell_numbers)
        print '</center>'

    else:
        print interface_form_string

    form_bottom = """
    <BR><BR>
    <h3>Output</h3>
    Choose file name for the extracted cells:<BR>
    <INPUT TYPE=TEXT NAME="selected_filename"> .html
    <BR><BR>
    <select NAME="inclusion">
     <option value="default">Complete cells (default)</option>
     <option value="EX_HEAD">Exclude headers</option>
     <option value="EX_OUT">Exclude outputs</option>
     <option value="EX_HEAD_OUT">Exclude headers and outputs</option>
    </select>
    <input type="hidden" name="selected_notebook" value="%s">
    <BR><BR><BR>

    <CENTER><INPUT class="btn" TYPE=SUBMIT name="create_html" VALUE="Create HTML"></CENTER>
    </FORM>

    <BR>
    """

    iframe =  """<iframe src="%s" scrolling="yes" width="100%%" height="800" frameBorder="0">"""
    tab_divs = """
    <div class="tab">
      <button class="tablinks" onclick="openTab(event, '%s');loadiFrame('%s')" id="defaultOpen">%s</button>
      <button class="tablinks" onclick="openTab(event, '%s');loadiFrame('%s')">%s</button>
    </div>

    <div id="%s" class="tabcontent">
      <p>%s</p>
    </div>

    <div id="%s" class="tabcontent">
      <p>%s</p>
    </div>

    <script>
    function openTab(evt, option) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");

        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(option).style.display = "block";
        evt.currentTarget.className += " active";
    }

    // Get the element with id="defaultOpen" and click on it
    document.getElementById("defaultOpen").click();

    function loadiFrame(url) {
        iframe_source = '<iframe src="' + url + '" scrolling="yes" width="100%%" height="800" frameBorder="0">'
        document.getElementById("iframe").innerHTML = iframe_source;
    }

    </script>
    <div id="iframe">
        <iframe src="%s" scrolling="yes" width="100%%" height="800" frameBorder="0">
    </div>

    """

    # Place selected_notebook URL into the hidden tag
    if get_URL:
        print form_bottom % (get_URL)
    elif selected_notebook != None:
        print form_bottom % (selected_notebook)

    if get_URL:
        print iframe % (get_URL)
    elif create_html and selected_notebook != None:
        createHTML()
        input_label = "Input HTML"
        output_label = "Extracted Cells HTML"
        iframe_html_writepath = 'http://1uslchriston.ad.here.com:90/builds/' + selected_filename

        print tab_divs % (input_label, selected_notebook, input_label, output_label, iframe_html_writepath, output_label,
                          input_label, selected_notebook, output_label, iframe_html_writepath, selected_notebook)


def print_output():

    interface_top = """
    <html>
    <head>
      <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
    <style>
          body {
              font-family: 'Roboto', sans-serif;
              font-size: 16px;
          }

        .btn {
          -webkit-border-radius: 8;
          -moz-border-radius: 8;
          -webkit-box-shadow: 0px 2px 5px #666666;
          -moz-box-shadow: 0px 2px 5px #666666;
          box-shadow: 0px 2px 5px #666666;
          color: #ffffff;
          font-size: 14px;
          background: #0369ad;
          padding: 3px 15px 4px 15px;
          text-decoration: none;
        }

        .btn:hover {
          background: #299be6;
          text-decoration: none;
        }


        /* Style the tab */
        div.tab {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
        }

        /* Style the buttons inside the tab */
        div.tab button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 17px;
        }

        /* Change background color of buttons on hover */
        div.tab button:hover {
            background-color: #ddd;
        }

        /* Create an active/current tablink class */
        div.tab button.active {
            background-color: #D2E4FC;
        }

        /* Style the tab content */
        .tabcontent {
            display: none;
            padding: 6px 12px;
            border: 1px solid #ccc;
            border-top: none;
        }

    </style>
    </head>
    <body bgcolor="#fff">

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
    <center><h1>Jupyter Notebook Cell Export Tool</h1></center>
    """

    interface_bottom = """
    </body>
    </html>"""

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
        global html_writepath
        template_path = "C:\\Bitnami\\wampstack-5.6.31-0\\apache2\\htdocs\\templates\\"
        selected_filename = selected_filename + ".html"
        html_writepath = "C:\\Bitnami\\wampstack-5.6.31-0\\apache2\\htdocs\\builds\\" + selected_filename

        # Get top portion of html
        build_top = template_path + "\\nb_top.txt"
        f = open(build_top, 'r')
        top = f.readlines()
        f.close()

        writer = open(html_writepath,'w')
        for line in top:
            writer.write(line)
        # num 	{'HEADER': (11748, 11756), 'OUT': (11773, 11788), 'IN': (11757, 11772)}
        for num in selected_cells:
            begin_next_cell = r'<!--  Beginning of next cell  -->'
            writer.write('\n\n' + begin_next_cell + '\n')
            header = cell_map[num].get('HEADER', '')
            if header:
                header_range = header[0]
                start = header_range[0]
                end = header_range[1]
                header_block = page_source[start: end]
                for line in header_block:
                    line = line.encode('UTF-8')
                    writer.write(line + '\n')
            input_cell = cell_map[num].get('IN', '')
            if input_cell:
                input_range = input_cell[0]
                start = input_range[0]
                end = input_range[1]
                input_block = page_source[start: end]
                for line in input_block:
                    line = line.encode('UTF-8')
                    writer.write(line + '\n')
            output_cell = cell_map[num].get('OUT', '')
            if output_cell:
                output_range = output_cell[0]
                start = output_range[0]
                end = output_range[1]
                output_block = page_source[start: end]
                for line in output_block:
                    line = line.encode('UTF-8')
                    writer.write(line + '\n')
        writer.write('\n' + html_close)
        writer.close()


def printCheckboxes(cell_nums):
    table_open = """
        <BR><BR>
        <table class="tg">
          <tr>
            <th class="tg-baqh" colspan="%s"><h2>Select cells to export</h2></th>
          </tr>
          <tr>
    """

    table_close = """
          </tr>
        </table>
    """

    table_row_separator = """
          </tr>
          <tr>
    """

    style = """
    <style>
        .tg  {
            border-collapse:collapse;
            border-spacing:3;
            border-color:#aabcfe;
            align: right;
        }
        .tg td {
            padding:10px 5px;
            overflow:hidden;
            word-break:normal;
            border-color:#aabcfe;
            color:#000;
            background-color:#e8edff;
            align: right;
        }
        .tg th {
            overflow:hidden;
            word-break:normal;
            color:#039;
            background-color:#fff;
            align: right;
        }
        .tg .tg-baqh{
            margin-right:3em;
            vertical-align:top;
            color:#000;
            align: right;
        }
        .tg .tg-6k2t {
            background-color:#fff;
            vertical-align:top;
            align: right;
        }
        .tg td:hover {background-color: #D2E4FC;}

    </style>
    """

    select_all_buttons = """
    <FORM name="selected_cells" METHOD=POST ACTION="http://1uslchriston.ad.here.com:90/cgi-bin/interface_cgi.py">
    """

    select_all_buttons_backup = """
            <td>
            <FORM name="selected_cells" METHOD=POST ACTION="http://1uslchriston.ad.here.com:90/cgi-bin/interface_cgi.py">
            <input class="btn" type="button" value="Check All" onclick="javascript:checkAll('selected_cells', true);">
	       </td>
	       <td align="right">
	       <input class="btn" type="button" value="Uncheck All" onclick="javascript:checkAll('selected_cells', false);">
	       </td>
       </tr>
       <tr>
    """

    default_table_cols = 16
    print style
    print select_all_buttons
    print table_open % (default_table_cols)
    row_counter = 1
    for num in cell_nums:
        actual_num = num
        num = int(num)
        if num < 10:
            num = '0' + str(num)
        else:
            num = str(num)
        print '<td class="tg-6k2t">%s<INPUT TYPE=CHECKBOX NAME="selected_cells" VALUE="%s" style="margin-left:1em;margin-right:1em"></td>' % (num, actual_num)
        if row_counter == 16:
            print table_row_separator
            row_counter = 0
        row_counter += 1
    print table_close


def main():
    loadNotebook()
    print_output()
    global page_source

if __name__ == '__main__':
    main()
