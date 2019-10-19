import os
import sys
import logging
import collections
from functools import reduce
import re
import util

logger = logging.getLogger(__name__)


def create_page(marked_code: list):
    html_str = ''' <html><head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
        </head><body>
        <script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js"></script>
        <h1>AMAHelper graph</h1> '''
    for num, file_name, code in marked_code:
        html_str += "<!-- *** method *** --->"
        html_str += "<h2 id=\""+str(num)+"\"> Block " + str(num) + " " +\
                    "method_name " +\
                    " :</h2>"
        file_name = os.path.abspath(file_name)
        html_str += "<p>" + "file: <a href=" + file_name + ">"+file_name+"</a></p>"
        method_body = ""
        annotation = "// AMAHelper: control "
        for line_number, line in enumerate(code):
            line = line.rstrip()
            # Add control flow links:
            if annotation in line:
                try:
                    target_method = int(line.split(annotation)[1])
                except (ValueError, IndexError):
                    logger.error("Malformed AMAHelper annotation at line "
                                 + str(line_number+1), exc_info=True)
                line = line.replace(annotation, "// Jump to <a style=\"color: #999999\" href=#" + str(target_method) + ">block </a>")
            method_body += line + "\n"
        html_str += "<pre class=\"prettyprint\"><p>" + method_body + "</p></pre>"
        # html_str += "<p id=\""+str(num)+"\">" + method_body + "</p>"
    html_str += "</body></html>"
    # html_str += <a href=\"method1.html\">my link</a>
    return html_str


def extract_marked_code(file: str) -> dict:
    marked_code = collections.defaultdict(list)
    with open(file, "r") as f:
        in_marked_code = False
        for line_number, orig_line in enumerate(f):
            line = orig_line.rstrip().lstrip()
            if line.startswith("//") and "AMAHelper:" in line:
                try:
                    method_number = int(line.split(" ")[2])
                    in_marked_code = not in_marked_code
                except (ValueError, IndexError):
                    logger.error("Malformed AMAHelper annotation at line "
                                 + str(line_number+1)
                                 + " in file " + file, exc_info=True)
            if in_marked_code:
                marked_code[method_number].append(orig_line)
    return marked_code


if __name__ == "__main__":
    java_directory = sys.argv[1]
    try:
        files = util.get_all_files(java_directory)
    except ValueError:
        logger.error("Parameter is not a directory!", exc_info=True)
        exit(0)

    all_marked_code = list()
    for f in files:
        for k, v in extract_marked_code(f).items():
            all_marked_code.append((k, f, v))

    html_string = create_page(sorted(all_marked_code, key=lambda x: x[0]))
    try:
        os.mkdir("report")
    except FileExistsError:
        pass
    with open("report/report.html", "w")as f:
        f.write(html_string)