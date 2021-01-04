import os
from typing import List
from injecta.config.ConfigReaderInterface import ConfigReaderInterface
from injecta.container.ContainerBuild import ContainerBuild
from injecta.container.ContainerBuilder import ContainerBuilder
from injecta.container.ContainerInitializer import ContainerInitializer
from injecta.container.ContainerInterface import ContainerInterface
from pyfonybundles.Bundle import Bundle
from pyfony.container.PyfonyHook import PyfonyHooks

class Kernel:

    _allowedEnvironments = ['dev', 'test', 'prod']

    def __init__(
        self,
        appEnv: str,
        configDir: str,
        bundles: List[Bundle],
        configReader: ConfigReaderInterface
    ):
        self._appEnv = appEnv
        self._configDir = configDir
        self._bundles = bundles
        self.__configReader = configReader
        self._containerBuilder = ContainerBuilder()

    def setAllowedEnvironments(self, allowedEnvironments: list):
        self._allowedEnvironments = allowedEnvironments

    def initContainer(self) -> ContainerInterface:
        if self._appEnv not in self._allowedEnvironments:
            raise Exception(f'Unexpected environment: {self._appEnv}')

        hooks = self._createPyfonyHooks()
        return self._initContainerFromHooks(hooks)

    def _initContainerFromHooks(self, hooks: PyfonyHooks):
        config = self.__configReader.read(self._getConfigPath())
        containerBuild = self._containerBuilder.build(config, hooks)
        return self._initAndBootContainer(containerBuild)

    def _createPyfonyHooks(self):
        return PyfonyHooks(
            self._bundles,
            self._getConfigPath(),
            self._getProjectBundlesConfigDir(),
            self._appEnv
        )

    def _initAndBootContainer(self, containerBuild: ContainerBuild):
        container = ContainerInitializer().init(containerBuild)
        self._boot(container)

        return container

    def _getConfigPath(self):
        return f'{self._configDir}/config_{self._appEnv}.yaml'

    def _getProjectBundlesConfigDir(self):
        return os.path.dirname(self._getConfigPath()) + '/bundles'

    def _boot(self, container: ContainerInterface):
        for bundle in self._bundles:
            bundle.boot(container)
