import pytest
import os
from amahelper.code_builder import code_builder

data_files = dict()


@pytest.fixture(scope="module", autouse=True)
def load_test_data():
    test_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    for data_file in os.listdir(test_data_path):
        data_files[data_file] = os.path.join(test_data_path, data_file)


def test_graph_builder_TestA():
    cb = code_builder(data_files["TestA.java"])
    assert cb.graph == {1: [2, 3]}, "graph is not correct"
