import os
import sys
import logging
import collections
from typing import List, Dict
from graphviz import Digraph
from util import Util, CodeExtractionError, CodeGraphConstructionError

logger = logging.getLogger(__name__)


class CodeBuilder:

    control_graph = collections.defaultdict(list)
    data_graph = collections.defaultdict(list)
    dot_graph = ""
    report_directory = "report/"

    def __init__(self, directory: str) -> None:
        """
        Generate a report with a graph from AMAHelper annotated java files
        :param str directory: directory that contains java files, or a java file
        :raises ValueError: the input is not a directory of a java file
        """
        try:
            try:
                files = Util.get_all_files(directory)
            except ValueError:
                if directory.endswith(".java"):
                    files = [directory]
                else:
                    raise ValueError
        except ValueError:
            logger.error("Parameter is not a directory or java file!", exc_info=True)
            raise ValueError("Parameter is not a directory or java file!")

        all_marked_code = list()
        for f in files:
            for k, v in self.extract_marked_code(f).items():
                all_marked_code.append((k, f, v))

        html_string = self.create_page(sorted(all_marked_code, key=lambda x: x[0]))
        try:
            os.mkdir(self.report_directory)
        except FileExistsError:
            pass
        with open(self.report_directory + "report.html", "w")as f:
            f.write(html_string)

    def create_page(self, marked_code: List[tuple]) -> str:
        """
        Create an html report page with a graph of dependencies between code blocks
        :param marked_code:
        :return: html page as a string
        """
        modified_method = dict()
        for num, file_name, code in marked_code:
            method_body = self.modify_method_annotations(code, num)
            if num in modified_method:
                raise CodeGraphConstructionError("Multiple code blocks with the same number annotation: " + str(num))
            modified_method[num] = method_body
        self.create_dot_graph()
        html_str = ''' <html><head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>body{ margin:0 100; background:whitesmoke; }</style>
            </head><body>
            <script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js"></script>
            <h1>AMAHelper graph</h1>
            <img src="graph.png" alt="Block graph align="middle""> 
            '''
        for num, file_name, code in marked_code:
            html_str += "<!-- *** method *** --->"
            html_str += "<h2 id=\""+str(num)+"\"> Block " + str(num) + " " + " :</h2>"
            file_name = os.path.abspath(file_name)
            html_str += "<p>" + "file: <a href=" + file_name + ">"+file_name+"</a></p>"
            html_str += "<pre class=\"prettyprint\"><p>" + modified_method[num] + "</p></pre>"
        html_str += "</body></html>"
        return html_str

    def create_dot_graph(self) -> None:
        """
        Generate a dot graph :attr: `dot_graph`
        :return:
        """
        dot = Digraph(comment='AMAHelperGraph')
        for node, edges in self.control_graph.items():
            [dot.edge(str(node), str(e)) for e in edges]
        for node, edges in self.data_graph.items():
            [dot.edge(str(node), str(e), style="dashed") for e in edges]
        dot.render(self.report_directory+"graph", format='png')
        self.dot_graph = dot.source

    def modify_method_annotations(self, code: list, num: int) -> str:
        """
        Modifies AMAHelper annotations to html reference
        :param code: list of lines code block representing a code block with annotations
        :param num: the number of the block
        :return: returns the modified block
        """
        method_body = ""
        for line_number, line in enumerate(code):
            line = line.rstrip()
            # Add control or data flow links:
            for annotation in ["// AMAHelper: control ", "// AMAHelper: data "]:
                if annotation in line:
                    try:
                        target_method = int(line.split(annotation)[1])
                    except (ValueError, IndexError):
                        logger.error("Malformed AMAHelper annotation at line "
                                     + str(line_number+1), exc_info=True)
                        raise CodeGraphConstructionError
                    line = line.replace(annotation, "// Jump to <a style=\"color: #999999\" href=#" +
                                        str(target_method) + ">block </a>")
                    if "control" in annotation:
                        self.control_graph[num].append(target_method)
                    else:
                        self.data_graph[num].append(target_method)
            method_body += line + "\n"
        return method_body

    @staticmethod
    def extract_marked_code(file: str) -> Dict[int, List[str]]:
        """

        :param file: java file to extract code blocks from
        :return: a dictionary of blocks indexed by the block number
        """
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
                        raise CodeExtractionError
                if in_marked_code:
                    marked_code[method_number].append(orig_line)
        return marked_code


if __name__ == "__main__":
    java_directory = sys.argv[1]
    CodeBuilder(java_directory)

