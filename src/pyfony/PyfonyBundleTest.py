import unittest
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.mocks.Bar import Bar
from injecta.mocks.Foo import Foo
from injecta.package.pathResolver import resolvePath
from injecta.testing.servicesTester import testServices
from pyfonybundles.loader import pyfonyBundlesLoader
from pyfony.PyfonyBundle import PyfonyBundle
from pyfony.Kernel import Kernel

class KernelTest(unittest.TestCase):

    def setUp(self):
        bundles = [*pyfonyBundlesLoader.loadBundles(), PyfonyBundle()]

        kernel = Kernel(
            'test',
            resolvePath('pyfony') + '/_config',
            bundles,
            YamlConfigReader()
        )

        self.__container = kernel.initContainer()

    def test_init(self):
        testServices(self.__container)

    def test_basic(self):
        foo = self.__container.get(Foo)
        bar = self.__container.get('injecta.mocks.Bar')

        self.assertIsInstance(foo, Foo)
        self.assertIsInstance(bar, Bar)

if __name__ == '__main__':
    unittest.main()
