from argparse import Namespace
from logging import Logger
from consolebundle.ConsoleCommand import ConsoleCommand
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.container.ContainerInterface import ContainerInterface
from injecta.testing.servicesTester import testServices
from pyfonybundles.loader import testingScopeBundlesLoader
from pyfony.Kernel import Kernel

class ContainerInitTestingCommand(ConsoleCommand):
    """
    Prerequisites:

    * poetry dev dependencies must NOT be installed
    * container is initialized in DEV/PROD environment
    """

    def __init__(
        self,
        logger: Logger,
        container: ContainerInterface,
    ):
        self.__logger = logger
        self.__container = container

    def getCommand(self) -> str:
        return 'container:test-init'

    def getDescription(self):
        return 'Loads all services from the container to test them'

    def run(self, inputArgs: Namespace):
        self.__logger.info('Loading all services...')

        testServices(self.__container)

        self.__logger.info('All services loaded properly')

        testingScopes = testingScopeBundlesLoader.getTestingScopes()

        for testingScope in testingScopes:
            self.__logger.info(f'Loading all services for scope "{testingScope}"...')

            scopedContainer = self._createScopedContainer(testingScope)

            testServices(scopedContainer)

            self.__logger.info(f'All services in scope "{testingScope}" loaded properly')

    def _createScopedContainer(self, testingScope: str):
        parameters = self.__container.getParameters()
        appEnv = parameters.kernel.environment
        configDir = parameters.project.configDir

        bundles = testingScopeBundlesLoader.loadBundles(testingScope)

        kernel = Kernel(
            appEnv,
            configDir,
            bundles,
            YamlConfigReader()
        )
        kernel.setAllowedEnvironments([appEnv])

        return kernel.initContainer()
