from typing import List
from injecta.config.ConfigReaderInterface import ConfigReaderInterface
from injecta.container.ContainerBuilder import ContainerBuilder
from injecta.container.ContainerInitializer import ContainerInitializer
from injecta.container.ContainerInterface import ContainerInterface
from pyfonybundles.Bundle import Bundle
from pyfony.container.PyfonyHook import PyfonyHooks

class BaseKernel:

    _allowedEnvironments = ['dev', 'test', 'prod']

    def __init__(
        self,
        appEnv: str,
        configDir: str,
        configReader: ConfigReaderInterface
    ):
        if appEnv not in self._allowedEnvironments:
            raise Exception('Unexpected environment: {}'.format(appEnv))

        self._appEnv = appEnv
        self._configDir = configDir
        self.__configReader = configReader
        self._containerBuilder = ContainerBuilder()

    def initContainer(self) -> ContainerInterface:
        config = self.__configReader.read(self._getConfigPath())
        hooks = PyfonyHooks(
            self._registerBundles(),
            self._getConfigPath(),
            self._appEnv
        )

        containerBuild = self._containerBuilder.build(config, hooks)

        container = ContainerInitializer().init(containerBuild)

        self._boot(container)

        return container

    def _getConfigPath(self):
        return self._configDir + '/config_{}.yaml'.format(self._appEnv)

    def _registerBundles(self) -> List[Bundle]:
        return []

    def _boot(self, container: ContainerInterface):
        for bundle in self._registerBundles():
            bundle.boot(container)
