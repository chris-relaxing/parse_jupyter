#!C:\Python27\python.exe -u


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

  <script language="JavaScript">
  </script>
<h2>Select Cells to export</h2>

<FORM METHOD=POST ACTION="#">"""

interface_form = """

1<INPUT TYPE=CHECKBOX NAME="cell1" VALUE="1" style='margin-right:3em'>
22<INPUT TYPE=CHECKBOX NAME="cell1" VALUE="1" style='margin-right:3em'>
3<INPUT TYPE=CHECKBOX NAME="cell1" VALUE="1" style='margin-right:3em'>
4<INPUT TYPE=CHECKBOX NAME="cell1" VALUE="1" style='margin-right:3em'>
5<INPUT TYPE=CHECKBOX NAME="cell1" VALUE="1" style='margin-right:3em'>

<BR><BR>
<INPUT TYPE=SUBMIT VALUE="Create HTML" style='margin-right:3em'>
Exclude Headers *<INPUT TYPE=CHECKBOX NAME="cell1" VALUE="Exclude Headers" style='margin-right:3em'>
Exclude Outputs *<INPUT TYPE=CHECKBOX NAME="cell1" VALUE="Exclude Outputs" style='margin-right:3em'>
* Headers and outputs are included by default.
</FORM>
<BR>

<iframe src="/jupyter/sqlalchemy_tutorial.html" scrolling="yes" width="100%" height="800">
"""


interface_bottom = """
</body>
</html>"""


def print_output():
    print "Content-type: text/html\n\n";
    print interface_top
    print interface_form
    print interface_bottom


def main():
    print_output()

if __name__ == '__main__':
    main()
