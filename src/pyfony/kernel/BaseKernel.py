import os
from typing import List
from injecta.config.ConfigReaderInterface import ConfigReaderInterface
from injecta.container.ContainerBuild import ContainerBuild
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
        hooks = self._createPyfonyHooks()
        return self._initContainerFromHooks(hooks)

    def initContainerForTesting(self):
        hooks = self._createPyfonyHooks()
        hooks.enableServicesTestingMode()
        return self._initContainerFromHooks(hooks)

    def _initContainerFromHooks(self, hooks: PyfonyHooks):
        config = self.__configReader.read(self._getConfigPath())
        containerBuild = self._containerBuilder.build(config, hooks)
        return self._initAndBootContainer(containerBuild)

    def _createPyfonyHooks(self):
        return PyfonyHooks(
            self._registerBundles(),
            self._getConfigPath(),
            self._getProjectBundlesConfigDir(),
            self._appEnv
        )

    def _initAndBootContainer(self, containerBuild: ContainerBuild):
        container = ContainerInitializer().init(containerBuild)
        self._boot(container)

        return container

    def _getConfigPath(self):
        return self._configDir + '/config_{}.yaml'.format(self._appEnv)

    def _getProjectBundlesConfigDir(self):
        return os.path.dirname(self._getConfigPath()) + '/bundles'

    def _registerBundles(self) -> List[Bundle]:
        return []

    def _boot(self, container: ContainerInterface):
        for bundle in self._registerBundles():
            bundle.boot(container)
