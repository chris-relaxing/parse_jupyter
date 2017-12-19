# parse_jupyter
Parse Jupyter Notebooks in order to extract only the desired cells for blog postings.

It's easy to save your Jupyter Notebook as a static HTML document. But what if you want to publish a portion of the 
Notebook for demo purposes in your blog? There didn't seem to be any tools that would allow you to easily publish a cell, 
or group of cells from the larger Notebook, keeping the Jupyter Notebook styling in place. The only option I saw was to 
hack out a portion of the HTML that I was interested in and copy all of the css information into a new HTML document. 

Obviously, this isn't the best solution, so I created this tool that would automate the process. This tool takes in as input
the saved notebook.html, reads it, and then provides a list of cell numbers in the form of checkboxes where you can decide
which cell or cells you want to export. At the click of a button, the tool will take your selected cells and create a new HTML 
document for you that you can then use in blog postings or iframes.


