import pytest
import os
from amahelper.code_builder import CodeBuilder

data_files = dict()
expected_control_graph = {'TestA.java': {1: [2, 3]}}
expected_data_graph = {'TestA.java': {2: [3]}}


@pytest.fixture(scope="module", autouse=True)
def load_test_data():
    test_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    for data_file in os.listdir(test_data_path):
        data_files[data_file] = os.path.join(test_data_path, data_file)


@pytest.fixture
def build_graph(file):
    cb = CodeBuilder(data_files[file])
    yield cb
    os.remove("report/report.html")
    os.remove("report/graph.png")
    os.rmdir("report/")


@pytest.mark.parametrize('file', ['TestA.java'])
def test_graph_builder_test_graph(file, build_graph):
    graph = build_graph
    assert graph.control_graph == expected_control_graph[file], "control graph is not correct"
    assert graph.data_graph == expected_data_graph[file], "data graph is not correct"

