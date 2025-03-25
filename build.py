from pybuilder.core import use_plugin, init
import sys
import os

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")

name = "G87.2025.T06.GE2"
default_task = "publish"


@init
def set_properties(project):
    project.set_property("dir_source_main_python", "src/main/python")
    project.set_property("dir_source_unittest_python", "src/unittest/python")
    project.set_property("unittest_module_glob", "test_*")
    project.set_property("coverage_source_paths", ["uc3m_money"])

    # Inject source path for imports
    sys.path.insert(0, os.path.abspath("src/main/python"))
