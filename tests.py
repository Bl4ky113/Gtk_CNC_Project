"""
    Test Suite for CNC PLotter Controller. Testing Each Module
"""

from unittest import TextTestRunner, TestLoader, TestSuite

from cnc_gtk_gui.tests import MainAppWindowTests

TEST_LIST = (
    MainAppWindowTests,
)

if __name__ == '__main__':
    CNCPlotterControllerTests = TestSuite()
    test_loader = TestLoader()
    test_runner = TextTestRunner()

    for test in TEST_LIST:
        module_test = test_loader.loadTestsFromTestCase(test)
        CNCPlotterControllerTests.addTest(module_test)

    test_runner.run(CNCPlotterControllerTests)
