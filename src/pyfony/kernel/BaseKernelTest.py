import os
import unittest
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.mocks.Bar import Bar
from injecta.mocks.Foo import Foo
from pyfony.kernel.BaseKernel import BaseKernel

class BaseKernelTest(unittest.TestCase):

    def test_basic(self):
        appEnv = 'dev'
        configDir = os.path.dirname(os.path.abspath(__file__)) + '/BaseKernelTest'

        kernel = BaseKernel(
            appEnv,
            configDir,
            YamlConfigReader()
        )

        container = kernel.initContainer()

        foo = container.get(Foo)
        bar = container.get('injecta.mocks.Bar')

        self.assertIsInstance(foo, Foo)
        self.assertIsInstance(bar, Bar)

if __name__ == '__main__':
    unittest.main()
